# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

from decimal import *
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.modules.GestioneFile.dao.ArticoloImmagine import ArticoloImmagine
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaFilesFilter(AnagraficaFilter):
    """ Filtro per la ricerca nei file """

    def __init__(self, anagrafica, daoArticolo=None):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_gestione_file_filter_table',
                          gladeFile='GestioneFile/gui/_anagrafica_gestione_file_elements.glade',
                          module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.daoArticolo = daoArticolo


    def draw(self):
        """ """
        self.refresh()

    #def _reOrderBy(self, column):
        #if column.get_name() == "numero":
            #return self._changeOrderBy(column,(None,GestioneFile.numero))
        #if column.get_name() == "data_inizio":
            #return self._changeOrderBy(column,(None,TestataPrimaNota.data_inizio))


    def clear(self):
        self.denominazione_filter_entry.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        deno = prepareFilterString(self.denominazione_filter_entry.get_text())

        def filterCountClosure():
            return ArticoloImmagine().count(
                                idArticolo = self.daoArticolo.id,
                                denominazione=deno,
                                )
        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return ArticoloImmagine().select(
                                            idArticolo = self.daoArticolo.id,
                                            denominazione = deno,
                                            offset=offset,
                                            batchSize=batchSize)

        self._filterClosure = filterClosure

        valis = self.runFilter()

        self.gestionefile_filter_listore.clear()
        valore = 0
        for i in valis:

            self.gestionefile_filter_listore.append((i,
                                        i.immagine.denominazione,
                                        i.immagine.denominazione,
                                        i.immagine.denominazione
                                        ))

