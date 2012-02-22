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

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_gestione_file_filter_table',
                          gladeFile='GestioneFile/gui/_anagrafica_gestione_file_elements.glade',
                          module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry

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
                                denominazione=deno,
                                )
        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return ArticoloImmagine().select(
                                            denominazione = deno,
                                            offset=offset,
                                            batchSize=batchSize)

        self._filterClosure = filterClosure

        valis = self.runFilter()

        self.gestionefile_filter_listore.clear()
        valore = 0
        for i in valis:
            col_valore = None
            col_tipo = None

            if mN(i.totali["totale"]) >0:
                col_valore = "#CCFFAA"
            else:
                col_valore = "#FFD7D7"

            if len(i.righeprimanota) >1:
                denom = i.note
                note = "( Più operazioni )"
                a = [l for l in i.righeprimanota]
                if len(a)==1:
                    tipo = i.righeprimanota[0].tipo
                else:
                    tipo = "misto"
                banca = i.righeprimanota[0].banca[0:15] or ""
            elif len(i.righeprimanota) ==1:
                denom = i.righeprimanota[0].denominazione
                note = i.note
                tipo = i.righeprimanota[0].tipo
                banca = i.righeprimanota[0].banca[0:15] or ""
            else:
                print "ATTENZIONE TESTATA PRIMA NOTA SENZA RIGHE", i, i.note, i.data_inizio
                denom ="SENZARIGHE"
                note = i.note
                banca = ""
            if tipo =="cassa":
                col_tipo = "#FFF2C7"
            elif tipo=="banca":
                col_tipo = "#CFF5FF"
            else:
                col_tipo = ""
            self.primanota_filter_listore.append((i,
                                        col_valore,
                                        (str(i.numero) or ''),
                                        (dateToString(i.data_inizio) or ''),
                                        denom or '',
                                        (str(mNLC(i.totali["totale"],2)) or "0"),
                                        tipo,
                                        banca,
                                        note or "",
                                        col_tipo
                                        ))

