# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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

from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.dao.DestinazioneMerce import DestinazioneMerce
from promogest.lib.utils import *


class AnagraficaDestinazioniMerce(Anagrafica):
    """ Anagrafica destinazioni merce """

    def __init__(self, idCliente = None, aziendaStr=None):
        self._clienteFissato = (idCliente <> None)
        self._idCliente=idCliente
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica destinazioni merce',
                            recordMenuLabel='_Destinazioni',
                            filterElement=AnagraficaDestinazioniMerceFilter(self),
                            htmlHandler=AnagraficaDestinazioniMerceHtml(self),
                            reportHandler=AnagraficaDestinazioniMerceReport(self),
                            editElement=AnagraficaDestinazioniMerceEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)


class AnagraficaDestinazioniMerceFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle destinazioni merce """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  root='anagrafica_destinazioni_merce_filter_table',
                                  path='_anagrafica_destinazioni_merce_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.orderBy = 'denominazione'


    def draw(self, cplx=False):
        self._treeViewModel = self.filter_listore
        self.refresh()

    def _reOrderBy(self, column):
        if column.get_name() == "denominazione_column":
            return self._changeOrderBy(column, (None, DestinazioneMerce.denominazione))
        elif column.get_name() == "indirizzo_column":
            return self._changeOrderBy(column, (None, DestinazioneMerce.indirizzo))
        elif column.get_name() == "localita_column":
            return self._changeOrderBy(column, (None, DestinazioneMerce.localita))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.indirizzo_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()


    def refresh(self):
        # Aggiornamento TreeView
        idCliente = self._anagrafica._idCliente
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        indirizzo = prepareFilterString(self.indirizzo_filter_entry.get_text())
        localita = prepareFilterString(self.localita_filter_entry.get_text())
        provincia = prepareFilterString(self.provincia_filter_entry.get_text())

        def filterCountClosure():
            return DestinazioneMerce().count(idCliente=idCliente,
                                                         denominazione=denominazione,
                                                         indirizzo=indirizzo,
                                                         localita=localita,
                                                         provincia=provincia)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return DestinazioneMerce().select(orderBy=self.orderBy,
                                                          idCliente=idCliente,
                                                          denominazione=denominazione,
                                                          indirizzo=indirizzo,
                                                          localita=localita,
                                                          provincia=provincia,
                                                          offset=offset,
                                                          batchSize=batchSize)

        self._filterClosure = filterClosure

        dems = self.runFilter()

        self._treeViewModel.clear()

        for d in dems:
            self._treeViewModel.append((d,
                                        (d.denominazione or ''),
                                        (d.indirizzo or ''),
                                        (d.localita or '')))



class AnagraficaDestinazioniMerceHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'destinazione_merce',
                                'Dettaglio della destinazione merce')



class AnagraficaDestinazioniMerceReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei destinazioni merce',
                                  defaultFileName='destinazioni_merce',
                                  htmlTemplate='destinazioni_merce',
                                  sxwTemplate='destinazioni_merce')



class AnagraficaDestinazioniMerceEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle destinazioni merce """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'Dati destinazione merce',
                                root='anagrafica_destinazioni_merce_detail_table',
                                path='_anagrafica_destinazioni_merce_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry


    def draw(self, cplx=False):
        pass


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = DestinazioneMerce()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = DestinazioneMerce().getRecord(id= dao.id)
        self._refresh()
        return self.dao

    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.indirizzo_entry.set_text(self.dao.indirizzo or '')
        self.localita_entry.set_text(self.dao.localita or '')
        self.cap_entry.set_text(self.dao.cap or '')
        self.provincia_entry.set_text(self.dao.provincia or '')
        self.codice_entry.set_text(self.dao.codice or '')


    def saveDao(self, tipo=None):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        self.dao.id_cliente = self._anagrafica._idCliente
        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.indirizzo = self.indirizzo_entry.get_text()
        self.dao.localita = self.localita_entry.get_text()
        self.dao.cap = self.cap_entry.get_text()
        self.dao.provincia = self.provincia_entry.get_text()
        self.dao.codice = self.codice_entry.get_text()
        self.dao.persist()
