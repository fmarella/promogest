# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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
from promogest.ui.utils import obligatoryField, prepareFilterString, mN
from promogest.ui.utils import on_id_aliquota_iva_customcombobox_clicked
from promogest.ui.utilsCombobox import fillComboboxAliquoteIva, findComboboxRowFromStr
from promogest.ui.utilsCombobox import findComboboxRowFromId, findIdFromCombobox
from promogest.dao.Pagamento import Pagamento


class AnagraficaPagamenti(Anagrafica):
    """ Anagrafica pagamenti """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica pagamenti',
                            recordMenuLabel='_Pagamenti',
                            filterElement=AnagraficaPagamentiFilter(self),
                            htmlHandler=AnagraficaPagamentiHtml(self),
                            reportHandler=AnagraficaPagamentiReport(self),
                            editElement=AnagraficaPagamentiEdit(self))

class AnagraficaPagamentiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei pagamenti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_pagamenti_filter_table',
                                  gladeFile='_anagrafica_pagamenti_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def draw(self):
        self._treeViewModel = self.filter_listore
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "denominazione_column":
            return self._changeOrderBy(column, (None, Pagamento.denominazione))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        pagamento = Pagamento()
        def filterCountClosure():
            return pagamento.count(denominazione=denominazione)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return pagamento.select(orderBy=self.orderBy,
                                denominazione=denominazione,
                                offset=offset,
                                batchSize=batchSize)

        self._filterClosure = filterClosure

        pagamenti = self.runFilter()

        self._treeViewModel.clear()

        for p in pagamenti:
            self._treeViewModel.append((p,
                                        (p.denominazione or ''),
                                        (p.tipo or ''),
                                        (mN(p.spese, 2)),
                                        (p.aliquota_iva)))

        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

class AnagraficaPagamentiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'pagamento',
                                'Informazioni sul pagamento')

class AnagraficaPagamentiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei pagamenti',
                                  defaultFileName='pagamenti',
                                  htmlTemplate='pagamenti',
                                  sxwTemplate='pagamenti')

class AnagraficaPagamentiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei pagamenti """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_pagamenti_detail_table',
                                'Dati pagamento',
                                gladeFile='_anagrafica_pagamenti_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry

    def draw(self, cplx=False):
        #Popola combobox
        fillComboboxAliquoteIva(self.id_aliquota_iva_ccb.combobox)
        self.id_aliquota_iva_ccb.connect('clicked',
                                         on_id_aliquota_iva_customcombobox_clicked)

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Pagamento()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Pagamento().getRecord(id=dao.id)
        self._refresh()

    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.spese_entry.set_text(str(self.dao.spese or 0))
        findComboboxRowFromStr(self.tipo_combobox, self.dao.tipo, 0)
        findComboboxRowFromId(self.id_aliquota_iva_ccb.combobox,
                              self.dao.id_aliquota_iva)

    def saveDao(self, tipo=None):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.denominazione_entry,
                            msg='Inserire la denominazione!')

        if (self.tipo_combobox.get_active_text() == ''):
            obligatoryField(self.dialogTopLevel,
                            self.tipo_combobox,
                            msg='Inserire il tipo di pagamento!')

        self.dao.id_aliquota_iva = findIdFromCombobox(self.id_aliquota_iva_ccb.combobox)
        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.spese = float(self.spese_entry.get_text())
        self.dao.tipo = self.tipo_combobox.get_active_text()

        self.dao.persist()
