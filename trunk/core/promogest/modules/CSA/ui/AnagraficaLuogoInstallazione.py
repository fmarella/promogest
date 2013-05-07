# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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
from promogest.modules.CSA.dao.TipoApparecchio import TipoApparecchio
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaTipoApparecchio(Anagrafica):
    """ Anagrafica categorie clienti """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica tipo apparecchio',
                            '_Tipo apparecchio',
                            AnagraficaTipoApparecchioFilter(self),
                            AnagraficaTipoApparecchioDetail(self))

    def draw(self):
        """ Facoltativo ma suggerito per indicare la lunghezza
        massima della cella di testo
        """
        self.filter.denominazione_column.get_cells()[0].set_data(
                                                        'max_length', 50)

        self._treeViewModel = self.filter.filter_listore
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(
                        self.filter.denominazione_filter_entry.get_text())
        self.numRecords = TipoApparecchio().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return TipoApparecchio().select(denominazione=denominazione,
                                            orderBy=self.orderBy,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        self._filterClosure = filterClosure
        cats = self.runFilter()
        self._treeViewModel.clear()
        for c in cats:
            self._treeViewModel.append((c,
                                        (c.denominazione or '')))


class AnagraficaTipoApparecchioFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle tipi apparecchio """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                      anagrafica,
                      root='anagrafica_tipo_apparecchio_filter_table',
                      path='CSA/gui/_anagrafica_tipo_apparecchio_elements.glade',
                      isModule=True)
        self._widgetFirstFocus = self.denominazione_filter_entry

    def _reOrderBy(self, column):
        if column.get_name() == "denominazione_column":
            return self._anagrafica._changeOrderBy(
                    column, (None, TipoApparecchio.denominazione))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaTipoApparecchioDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle tipo apparecchio
    """
    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                      anagrafica,
                      path='CSA/gui/_anagrafica_categorie_clienti_elements.glade',
                      isModule=True)

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            self.dao = TipoApparecchio()
            self._anagrafica._newRow((self.dao, ''))
            #self._refresh()
        return self.dao

    def updateDao(self):
        self.dao = TipoApparecchio().getRecord(id=self.dao.id)
        self._refresh()

    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator and self.dao:
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