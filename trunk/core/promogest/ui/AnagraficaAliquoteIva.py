# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
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
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaAliquoteIva(Anagrafica):
    """ Anagrafica aliquote IVA """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica aliquote IVA',
                            recordMenuLabel='_Aliquote IVA',
                            filterElement=AnagraficaAliquoteIvaFilter(self),
                            htmlHandler=AnagraficaAliquoteIvaHtml(self),
                            reportHandler=AnagraficaAliquoteIvaReport(self),
                            editElement=AnagraficaAliquoteIvaEdit(self),
                            aziendaStr=aziendaStr)


class AnagraficaAliquoteIvaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle aliquote IVA """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_aliquote_iva_filter_table',
                          gladeFile='_anagrafica_aliquote_iva_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def draw(self):
        """ Disegno la treeview e gli altri oggetti della gui """
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "descrizione_column":
            return self._changeOrderBy(column,(None,AliquotaIva.denominazione))
        if column.get_name() == "descrizione_breve_column":
            return self._changeOrderBy(column,(None,AliquotaIva.denominazione_breve))


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        aliquota_iva = AliquotaIva()

        def filterCountClosure():
            return aliquota_iva.count(denominazione=denominazione)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return aliquota_iva.select(denominazione=denominazione,
                                        orderBy=self.orderBy,
                                        offset=offset,
                                        batchSize=batchSize)

        self._filterClosure = filterClosure

        ivas = self.runFilter()

        self.filter_listore.clear()
        for i in ivas:
            self.filter_listore.append((i,
                                        (i.denominazione or ''),
                                        (i.denominazione_breve or ''),
                                        (('%5.2f') % (i.percentuale or 0))))


class AnagraficaAliquoteIvaHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'aliquota_iva',
                                'Dettaglio aliquota IVA')


class AnagraficaAliquoteIvaReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle aliquote I.V.A.',
                                  defaultFileName='aliquote_iva',
                                  htmlTemplate='aliquote_iva',
                                  sxwTemplate='aliquote_iva')


class AnagraficaAliquoteIvaEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle aliquote IVA """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_aliquote_iva_detail_table',
                                'Dati aliquota I.V.A.',
                                gladeFile='_anagrafica_aliquote_iva_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry

    def draw(self, cplx=False):
        #Popola combobox tipi aliquote iva
        fillComboboxTipiAliquoteIva(self.id_tipo_combobox)

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = AliquotaIva()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = AliquotaIva().getRecord(id=dao.id)
        self._refresh()

    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.denominazione_breve_entry.set_text(self.dao.denominazione_breve or '')
        percentuale = self.dao.percentuale or 0
        self.percentuale_entry.set_text(('%-5.2f') % percentuale)
        percentuale_detrazione = self.dao.percentuale_detrazione or 0
        self.percentuale_detrazione_entry.set_text(('%-5.2f') % percentuale_detrazione)
        self.descrizione_detrazione_entry.set_text(self.dao.descrizione_detrazione or '')
        findComboboxRowFromId(self.id_tipo_combobox, self.dao.id_tipo)

    def saveDao(self, tipo=None):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        if (self.denominazione_breve_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_breve_entry)

        if (self.percentuale_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.percentuale_entry)

        if (findIdFromCombobox(self.id_tipo_combobox) is None):
            obligatoryField(self.dialogTopLevel, self.id_tipo_combobox)

        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.denominazione_breve = self.denominazione_breve_entry.get_text()
        self.dao.percentuale = float(self.percentuale_entry.get_text())
        self.dao.percentuale_detrazione = float(self.percentuale_detrazione_entry.get_text())
        self.dao.descrizione_detrazione = self.descrizione_detrazione_entry.get_text()
        self.dao.id_tipo = findIdFromCombobox(self.id_tipo_combobox)
        self.dao.persist()
