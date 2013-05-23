# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.modules.CSA.dao.ServCSA import ServCSA
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaServCSAFilter(AnagraficaFilter):
    """ Filtro per la ricerca nei file """

    def __init__(self, anagrafica, daoFrom=None, tipo="Cliente"):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  root='anagrafica_serv_csa_filter_table',
                                  path='CSA/gui/_anagrafica_serv_csa_elements.glade',
                                  isModule=True)
        self._widgetFirstFocus = self.seriale_filter_entry
        self.daoFrom = daoFrom
        self.tipo = tipo

    def draw(self):
        """ """
        self.refresh()

    #def _reOrderBy(self, column):
        #if column.get_name() == "numero":
            #return self._changeOrderBy(column,(None,GestioneFile.numero))
        #if column.get_name() == "data_inizio":
            #return self._changeOrderBy(column,(None,TestataPrimaNota.data_inizio))

    def clear(self):
        self.seriale_filter_entry.set_text('')
        self.id_cliente_filter_customcombobox.clean_entry()
        self.id_articolo_filter_customcombobox.clean_entry()
        self.data_avviamento_filter_datewidget.set_text("")

        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        #deno = prepareFilterString(self.denominazione_filter_entry.get_text())
        idCliente = self.id_cliente_filter_customcombobox.getId()
        idArticolo = self.id_articolo_filter_customcombobox.getId()
        idPg = None
        numeroSerie = self.seriale_filter_entry.get_text()
        manutenzione = None
        dataAvviamento = stringToDate(self.data_avviamento_filter_datewidget.get_text())

        def filterCountClosure():
            return ServCSA().count(
                        idArticolo = idArticolo,
                        idCliente = idCliente,
                        numeroSerie = numeroSerie,
                        batchSize = None
                        )
        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return ServCSA().select(
                            idArticolo = idArticolo,
                            idCliente = idCliente,
                            numeroSerie=numeroSerie,
                            offset=offset,
                            batchSize=batchSize)

        self._filterClosure = filterClosure

        valis = self.runFilter()

        self.anagrafica_serv_csa_filter_listore.clear()
        valore = 0
        for i in valis:
            self.anagrafica_serv_csa_filter_listore.append((i,
                                                        str(i.CLI.ragione_sociale or (i.CLI.cognome+" "+i.CLI.nome)),
                                                        str(dateToString(i.data_avviamento)),
                                                        str(i.arti.denominazione),
                                                        str(""),
                                                        str(i.numero_serie or ""),
                                                        str(i.manutenzione or ""),

                                                        ))
