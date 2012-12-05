# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from decimal import Decimal
from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.dao.BancheAzienda import BancheAzienda
from promogest.lib.utils import prepareFilterString, obligatoryField, \
                    dateToString, stringToDate, fillComboboxBanche,\
                    on_id_banca_customcombobox_clicked, \
findComboboxRowFromId, findIdFromCombobox


class AnagraficaBancheAzienda(Anagrafica):
    """ Anagrafica banche azienda """

    def __init__(self, idAzienda=None, aziendaStr=None):
        self._aziendaFissata = (idAzienda != None)
        self._idAzienda = idAzienda
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica banche azienda',
                            recordMenuLabel='_Banche azienda',
                            filterElement=AnagraficaBancheAziendaFilter(self),
                            htmlHandler=AnagraficaBancheAziendaHtml(self),
                            reportHandler=AnagraficaBancheAziendaReport(self),
                            editElement=AnagraficaBancheAziendaEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)


class AnagraficaBancheAziendaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle banche azienda """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
              anagrafica,
              root='anagrafica_banche_azienda_filter_table',
              path='_anagrafica_banche_azienda_elements.glade')
        self._widgetFirstFocus = self.numero_conto_filter_entry
        self.orderBy = 'numero_conto'

    def draw(self, cplx=False):
        self._treeViewModel = self.filter_listore
        self.refresh()

    def _reOrderBy(self, column):
        if column.get_name() == "numero_conto_column":
            return self._changeOrderBy(
                column, (None, BancheAzienda.numero_conto))

    def clear(self):
        # Annullamento filtro
        self.numero_conto_filter_entry.set_text('')
        self.numero_conto_filter_entry.grab_focus()

    def refresh(self):
        # Aggiornamento TreeView
        idAzienda = self._anagrafica._idAzienda
        numero_conto = prepareFilterString(
                self.numero_conto_filter_entry.get_text())

        def filterCountClosure():
            return BancheAzienda().count(idAzienda=idAzienda,
                                           numeroConto=numero_conto)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return BancheAzienda().select(orderBy=self.orderBy,
                                          idAzienda=idAzienda,
                                          numeroConto=numero_conto,
                                          offset=offset,
                                          batchSize=batchSize)

        self._filterClosure = filterClosure

        daos = self.runFilter()

        self._treeViewModel.clear()

        for dao in daos:
            self._treeViewModel.append((dao,
                                        (dao.denominazione_banca),
                                        (dao.numero_conto or ''),
                                        (dateToString(dao.data_riporto) or ''),
                                        (str(dao.valore_riporto) or ''),
                                        (dao.codice_sia or ''),
                                        (dao.banca_predefinita or False)))


class AnagraficaBancheAziendaHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'banca_azienda',
                                'Dettaglio della banca azienda')


class AnagraficaBancheAziendaReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle banche azienda',
                                  defaultFileName='banche_azienda',
                                  htmlTemplate='banche_azienda',
                                  sxwTemplate='banche_azienda')


class AnagraficaBancheAziendaEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle banche azienda """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
            anagrafica,
            'Dati banche azienda',
            root='anagrafica_banche_azienda_detail_table',
            path='_anagrafica_banche_azienda_elements.glade')
        self._widgetFirstFocus = self.numero_conto_entry
        fillComboboxBanche(self.id_banca_ccb.combobox, short=20)
        self.id_banca_ccb.connect('clicked',
                                   on_id_banca_customcombobox_clicked)

    def draw(self, cplx=False):
        pass

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = BancheAzienda()
        self._refresh()
        return self.dao

    def _refresh(self):
        findComboboxRowFromId(self.id_banca_ccb.combobox, self.dao.id_banca)
        self.numero_conto_entry.set_text(self.dao.numero_conto or '')
        self.data_widget.set_text(dateToString(self.dao.data_riporto) or '')
        self.valore_smentry.set_text(str(self.dao.valore_riporto or Decimal(0)))
        self.codice_sia_entry.set_text(self.dao.codice_sia or '')
        self.banca_pref_check.set_active(self.dao.banca_predefinita or False)

    def saveDao(self, tipo=None):
        id_banca = findIdFromCombobox(self.id_banca_ccb.combobox)
        if id_banca is None:
            obligatoryField(self.dialogTopLevel, self.id_banca_ccb.combobox)
        self.dao.id_banca = id_banca
        self.dao.numero_conto = self.numero_conto_entry.get_text()
        self.dao.data_riporto = stringToDate(self.data_widget.get_text())
        self.dao.valore_riporto = self.valore_smentry.get_text() or Decimal(0)
        self.dao.codice_sia = self.codice_sia_entry.get_text()
        self.dao.banca_predefinita = self.banca_pref_check.get_active()
        self.dao.id_azienda = self._anagrafica._idAzienda
        self.dao.persist()
