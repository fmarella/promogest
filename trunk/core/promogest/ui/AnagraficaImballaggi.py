# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
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
from promogest import Environment
from promogest.dao.Imballaggio import Imballaggio
from promogest.lib.utils import *


class AnagraficaImballaggi(Anagrafica):
    """ Anagrafica imballaggi """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica imballaggi',
                            '_Imballaggi',
                            AnagraficaImballaggiFilter(self),
                            AnagraficaImballaggiDetail(self))

    def draw(self):
        """ Facoltativo ma suggerito per indicare la lunghezza
        massima della cella di testo
        """
        self.filter.descrizione_column.get_cells()[0].set_data('max_length', 200)
        self._treeViewModel = self.filter.filter_listore
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())

        self.numRecords = Imballaggio().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Imballaggio().select(denominazione=denominazione,
                                                    orderBy=self.orderBy,
                                                    offset=self.offset,
                                                    batchSize=self.batchSize)

        self._filterClosure = filterClosure

        imbs = self.runFilter()

        self._treeViewModel.clear()

        for i in imbs:
            self._treeViewModel.append((i,
                                        (i.denominazione or '')))


class AnagraficaImballaggiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli imballaggi """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  root='anagrafica_imballaggi_filter_table',
                                  path='_anagrafica_imballaggi_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def _reOrderBy(self, column):
        if column.get_name() == "descrizione_column":
            return self._anagrafica._changeOrderBy(column,(None,Imballaggio.denominazione))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaImballaggiDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica degli imballaggi """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                        anagrafica,
                        path='_anagrafica_imballaggi_elements.glade')

    def setDao(self, dao):
        if dao is None:
            self.dao = Imballaggio()
            #self.dao = self.imb.record
            self._anagrafica._newRow((self.dao, ''))
            self._refresh()
        else:
            self.dao = dao
        return self.dao

    def updateDao(self):
        self.dao = Imballaggio().getRecord(id=self.dao.id)
        #self.dao = self.imb.record
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
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        self.dao.denominazione = denominazione
        self.dao.persist()

    def deleteDao(self):
        self.dao.delete()
