# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Andrea Argiolas <andrea@promotux.it>
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
# Author: Dr astico <zoccolodignu@gmail.com>
# Author: Francesco Meloni <francesco@promotux.it>

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


from promogest.ui.gtk_compat import *
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.lib.utils import *
from promogest.dao.TestataDocumento import TestataDocumento
import datetime
from promogest.ui.utilsCombobox import *
from promogest import Environment

class AnagraficaDocumentiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nei documenti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                anagrafica,
                                root='anagrafica_documenti_filter_table',
                                path='_ricerca_semplice_documenti.glade')
        self._widgetFirstFocus = self.da_data_filter_entry
        if not posso("GN"):
            self.noleggio_expander.destroy()
        self.orderBy = 'data_documento'
        self.xptDaoList = None
        self.id_clienti_abbinati = None

    def draw(self):
        """
        Disegna colonne della Treeview per il filtro
        """
        treeselection = self.anagrafica_filter_treeview.get_selection()
        treeselection.set_mode(GTK_SELECTIONMODE_MULTIPLE)

        fillComboboxPagamenti(self.id_pagamento_filter_combobox)
        fillComboboxOperazioni(self.id_operazione_filter_combobox, 'documento',True)
        self.id_operazione_filter_combobox.set_active(0)
        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
        self._anagrafica.info_anag_complessa_label.destroy()
        self.id_operazione_filter_combobox.set_wrap_width(setconf("Numbers", "combo_column"))

        self.cliente_filter_radiobutton.connect('toggled',
                                                self.on_filter_radiobutton_toggled)
        self.fornitore_filter_radiobutton.connect('toggled',
                                                  self.on_filter_radiobutton_toggled)
        self.cliente_filter_radiobutton.set_active(True)
        self.on_filter_radiobutton_toggled()
        idHandler = self.id_agente_filter_customcombobox.connect('changed',
                                                                 on_combobox_agente_search_clicked)
        self.id_agente_filter_customcombobox.setChangedHandler(idHandler)
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "numero_column":
            return self._changeOrderBy(column,(None,TestataDocumento.numero))
        if column.get_name() == "data_column":
            return self._changeOrderBy(column,(None,"data_documento"))
        if column.get_name() == "tipo_documento_column":
            return self._changeOrderBy(column,(None,TestataDocumento.operazione))

    def clear(self):
        """
        Annullamento filtro
         """

        self.da_data_filter_entry.set_text('01/01/' + Environment.workingYear)
        self.a_data_filter_entry.set_text('')
        self.da_numero_filter_entry.set_text('')
        self.a_numero_filter_entry.set_text('')
        self.protocollo_entry.set_text('')
        self.id_pagamento_filter_combobox.set_active(-1)
        self.id_operazione_filter_combobox.set_active(0)
        if not self._anagrafica._magazzinoFissato:
            fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
            self.id_magazzino_filter_combobox.set_active(0)
        else:
            findComboboxRowFromId(self.id_magazzino_filter_combobox,
                                  self._anagrafica._idMagazzino)
        self.id_cliente_filter_customcombobox.set_active(0)
        self.id_fornitore_filter_customcombobox.set_active(0)
        self.id_agente_filter_customcombobox.set_active(0)
        if posso("PA"):
            self.tutto_radio.set_active(1)
        if posso("GN"):
            self.a_data_inizio_noleggio_filter_entry.set_text('')
            self.da_data_inizio_noleggio_filter_entry.set_text('')
            self.a_data_fine_noleggio_filter_entry.set_text('')
            self.da_data_fine_noleggio_filter_entry.set_text('')
        self.id_articolo_filter_customcombobox.set_active(0)
        self.refresh()

    @timeit
    def refresh(self):
        """
        Aggiornamento TreeView
        """
        daData = stringToDate(self.da_data_filter_entry.get_text())
        if Environment.tipodb == "sqlite":
            aData = stringToDateBumped(self.a_data_filter_entry.get_text())
        else:
            aData = stringToDate(self.a_data_filter_entry.get_text())
        daNumero = prepareFilterString(self.da_numero_filter_entry.get_text())
        aNumero = prepareFilterString(self.a_numero_filter_entry.get_text())
        protocollo = prepareFilterString(self.protocollo_entry.get_text())
        idOperazione = prepareFilterString(findIdFromCombobox(self.id_operazione_filter_combobox))
        idMagazzino = findIdFromCombobox(self.id_magazzino_filter_combobox)
        idCliente = self.id_cliente_filter_customcombobox.getId()
        idFornitore = self.id_fornitore_filter_customcombobox.getId()
        idPagamento = findIdFromCombobox(self.id_pagamento_filter_combobox)
        idAgente = self.id_agente_filter_customcombobox._id
        if self.tutto_radio.get_active():
            statoDocumento = None
        elif self.saldato_radio.get_active():
            statoDocumento = bool(True)
        else:
            statoDocumento = bool(False)

        if self.solo_contabili_check.get_active():
            soloContabili = bool(True)
        else:
            soloContabili=None
        if self.id_clienti_abbinati:
            idCliente = self.id_clienti_abbinati
        idArticolo = self.id_articolo_filter_customcombobox.getId()
        #genero il dizionario dei filtri
        self.filterDict = {"daNumero":daNumero,
                            "aNumero":aNumero,
                            "daData":daData,
                            "aData":aData,
                            "daParte":None,
                            "aParte":None,
                            "protocollo":protocollo,
                            "idPagamento": idPagamento,
                            "idOperazione":idOperazione,
                            "idMagazzino":idMagazzino,
                            "idCliente":idCliente,
                            "idFornitore":idFornitore,
                            "idAgente":idAgente,
                            "statoDocumento":statoDocumento,
                            "soloContabili":soloContabili}

        if posso("GN"):
            daDataInizioNoleggio = stringToDate(self.da_data_inizio_noleggio_filter_entry.get_text())
            aDataInizioNoleggio = stringToDate(self.a_data_inizio_noleggio_filter_entry.get_text())
            daDataFineNoleggio = stringToDate(self.da_data_fine_noleggio_filter_entry.get_text())
            aDataFineNoleggio = stringToDateBumped(self.a_data_fine_noleggio_filter_entry.get_text())
            self.filterDict.update(daDataInizioNoleggio = daDataInizioNoleggio,
                                    aDataInizioNoleggio = aDataInizioNoleggio,
                                    daDataFineNoleggio = daDataFineNoleggio,
                                    aDataFineNoleggio = aDataFineNoleggio)

        def filterCountClosure():
            if idArticolo:
                a = TestataDocumento().count(filterDict = self.filterDict, idArticoloMov=idArticolo) or 0
                b = TestataDocumento().count(filterDict = self.filterDict, idArticoloDoc=idArticolo) or 0
                return a+b
            return TestataDocumento().count(filterDict = self.filterDict)

        self._filterCountClosure = filterCountClosure
        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            """ questo trucchetto su idArticolo è stato necessario perchè
            l'articolo puà essere sia in righe documento che in righe movimento
            e la query "percorre strade" diverse che unite in una sola query
            con "OR_" anche se con i join diventava molto lenta,
            così invece sembra non perdere in velocità """
            if idArticolo:
                a = TestataDocumento().select(orderBy=self.orderBy,
                                                offset=offset,
                                                idArticoloMov=idArticolo,
                                                batchSize=batchSize,
                                                filterDict = self.filterDict) or []
                b = TestataDocumento().select(orderBy=self.orderBy,
                                                offset=offset,
                                                idArticoloDoc=idArticolo,
                                                batchSize=batchSize,
                                                filterDict = self.filterDict) or []
                return a+b
            return TestataDocumento().select(orderBy=self.orderBy,
                                                offset=offset,
                                                batchSize=batchSize,
                                                filterDict = self.filterDict)
        self._filterClosure = filterClosure
        tdos = self.runFilter()
        self.filter_listore.clear()
        pa = posso("PA")
        for t in tdos:
            totali = t.totali
            totaleImponibile = mNLC(t._totaleImponibileScontato,2) or 0
            totaleImposta = mNLC(t._totaleImpostaScontata,2) or 0
            totale = mNLC(t._totaleScontato,2) or 0
            col = None
            if pa and t.documento_saldato == 1:
                documento_saldato_filter = "Si"
                if t.operazione in Environment.hapag:
                    col = "#CCFFAA"
                else:
                    col = None
            elif pa and t.documento_saldato == 0:
                documento_saldato_filter = "No"
                if t.operazione in Environment.hapag:
                    col = "#FFD7D7"
                else:
                    col = None
            else:
                documento_saldato_filter = ''
            self.filter_listore.append((t,
                                    dateTimeToString(t.data_documento),
                                    (str(t.numero) or 0),
                                    (t.operazione or ''),
                                    (t.intestatario or ''),
                                    (t.protocollo or ''),
                                    str(totaleImponibile),
                                    str(totaleImposta),
                                    str(totale),
                                    (t.note_interne or ''),
                                    col,
                                    (str(documento_saldato_filter) or '')
                                    ))


    def on_filter_radiobutton_toggled(self, widget=None):
        if self.cliente_filter_radiobutton.get_active():
            self.id_cliente_filter_customcombobox.set_sensitive(True)
            self.id_cliente_filter_customcombobox.grab_focus()
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
        elif self.fornitore_filter_radiobutton.get_active():
            self.id_fornitore_filter_customcombobox.set_sensitive(True)
            self.id_fornitore_filter_customcombobox.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
