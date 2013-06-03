# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

from promogest.ui.AnagraficaSemplice import \
                        Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest.dao.CategoriaCliente import CategoriaCliente
from promogest.lib.utils import *


class AnagraficaCategorieClienti(Anagrafica):
    """ Anagrafica categorie clienti """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica categorie clienti',
                            '_Categorie clienti',
                            AnagraficaCategorieClientiFilter(self),
                            AnagraficaCategorieClientiDetail(self))



    def refresh(self):

        denominazione = prepareFilterString(
                        self.filter.denominazione_filter_entry.get_text())
        self.numRecords = CategoriaCliente().count(denominazione=denominazione)

        self._refreshPageCount()


        def filterClosure(offset, batchSize):
            return CategoriaCliente().select(denominazione=denominazione,
                                            orderBy=self.orderBy,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        self._filterClosure = filterClosure
        cats = self.runFilter()
        self._treeViewModel.clear()
        for c in cats:
            self._treeViewModel.append((c,
                                        (c.denominazione or '')))


class AnagraficaCategorieClientiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle categorie clienti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self, anagrafica)
        self._widgetFirstFocus = self.denominazione_filter_entry

    def _reOrderBy(self, column):
        if column.get_name() == "denominazione_column":
            return self._anagrafica._changeOrderBy(
                    column, (None, CategoriaCliente.denominazione))



class AnagraficaCategorieClientiDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle categorie clienti """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self, anagrafica,)

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            self.dao = CategoriaCliente()
            self._anagrafica._newRow((self.dao, ''))
        return self.dao

    def updateDao(self):
        self.dao = CategoriaCliente().getRecord(id=self.dao.id)
        self._refresh()


    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        denominazione = model.get_value(iterator, 1) or ''
        if (denominazione == ''):
            obligatoryField(self._anagrafica.getTopLevel(),
                                self._anagrafica.anagrafica_treeview)
        self.dao.denominazione = denominazione
        self.dao.persist()
