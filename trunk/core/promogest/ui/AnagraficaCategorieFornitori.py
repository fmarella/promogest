# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas   <andrea@promotux.it>
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

from AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest.dao.CategoriaFornitore import CategoriaFornitore
from promogest.lib.utils import *


class AnagraficaCategorieFornitori(Anagrafica):
    """ Anagrafica categorie fornitori """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica categorie fornitori',
                            '_Categorie fornitori',
                            AnagraficaCategorieFornitoriFilter(self),
                            AnagraficaCategorieFornitoriDetail(self))

    def draw(self):
        """ Facoltativo ma suggerito per indicare la lunghezza
        massima della cella di testo
        """
        self.filter.descrizione_column.get_cells()[0].set_data(
                                                            'max_length', 200)
        self._treeViewModel = self.filter.filter_listore
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(
                        self.filter.denominazione_filter_entry.get_text())
        self.numRecords = CategoriaFornitore().count(
                                       denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return CategoriaFornitore().select(denominazione=denominazione,
                                            orderBy=self.orderBy,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        self._filterClosure = filterClosure

        cats = self.runFilter()

        self._treeViewModel.clear()

        for c in cats:
            self._treeViewModel.append((c,
                                        (c.denominazione or '')))


class AnagraficaCategorieFornitoriFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle categorie fornitori """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                  anagrafica,
                  'anagrafica_categorie_fornitori_filter_table',
                  gladeFile='_anagrafica_categorie_fornitori_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def _reOrderBy(self, column):
        if column.get_name() == "descrizione_column":
            return self._anagrafica._changeOrderBy(
                            column, (None, CategoriaFornitore.denominazione))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaCategorieFornitoriDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle categorie fornitori """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                    anagrafica,
                    gladeFile='_anagrafica_categorie_fornitori_elements.glade')

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            self.dao = CategoriaFornitore()
            self._anagrafica._newRow((self.dao, ''))
            self._refresh()
        return self.dao

    def updateDao(self):
        self.dao = CategoriaFornitore().getRecord(id=self.dao.id)
        self._refresh()

    def _refresh(self):
        if not self.dao:
            return
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if not iterator:
            return
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)

    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        denominazione = model.get_value(iterator, 1) or ''
        if (denominazione == ''):
            obligatoryField(self._anagrafica.getTopLevel(),
                                    self._anagrafica.anagrafica_treeview)
        self.dao.denominazione = denominazione
        self.dao.persist()

    def deleteDao(self):
        self.dao.delete()
