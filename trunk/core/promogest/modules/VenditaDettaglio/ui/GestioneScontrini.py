# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011  by Promotux
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

import gtk
import os, popen2

from promogest.dao.DaoUtils import giacenzaSel
from datetime import datetime, timedelta
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
from promogest.modules.VenditaDettaglio.ui.Distinta import Distinta
from promogest.modules.VenditaDettaglio.dao.TestataScontrinoCliente import TestataScontrinoCliente
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.dao.Inventario import Inventario
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Articolo import Articolo
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.Listino import Listino
from promogest.ui.utils import *
from promogest.ui import utils
from promogest.modules.VenditaDettaglio.ui.VenditaDettaglioUtils import fillComboboxPos

from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML

class GestioneScontrini(GladeWidget):
    """ Classe per la gestione degli scontrini emessi """

    def __init__(self, idArticolo = None,
                       daData = None,
                       aData = None,
                       righe = []):
        self._idArticolo = idArticolo
        self._daData = daData
        self._aData = aData
        self._righe = righe
        self._htmlTemplate = None
        self.dao = None
        self.daoTse = None

        GladeWidget.__init__(self, 'scontrini_emessi',
                fileName="VenditaDettaglio/gui/scontrini_emessi.glade", isModule=True)
        self._window = self.scontrini_emessi

        self.placeWindow(self._window)
        self.draw()

    def draw(self):

        self.filterss = FilterWidget(
                            owner=self,
                            filtersElement=GladeWidget(
                            rootWidget='scontrini_filter_table',
                            fileName="VenditaDettaglio/gui/_scontrini_emessi_elements.glade",
                            isModule=True),
                            #resultsElement="scontrino"
                            )
        self.filters = self.filterss.filtersElement
        self.filterTopLevel = self.filterss.getTopLevel()

        filterElement = self.filterss.filter_frame
        filterElement.unparent()
        self.filter_viewport.add(filterElement)
        self.anagrafica_hpaned.set_position(350)

        resultElement = self.filterss.filter_list_vbox
        resultElement.unparent()
        self.anagrafica_results_viewport.add(resultElement)
        self.detail = createHtmlObj(self)
        self.detail_scrolled.add(self.detail)
        self.filterss.hbox1.destroy()

        self.filters.id_articolo_filter_customcombobox.setId(self._idArticolo)

        if self._daData is None:
            self.filters.da_data_filter_entry.setNow()
        else:
            self.filters.da_data_filter_entry.set_text(self_daData)
        if self._aData is None:
            self.filters.a_data_filter_entry.setNow()
        else:
            self.filters.a_data_filter_entry.set_text(self_aData)
        fillComboboxMagazzini(self.filters.id_magazzino_filter_combobox)
        fillComboboxPos(self.filters.id_pos_filter_combobox)
        if hasattr(Environment.conf, "VenditaDettaglio"):
            if hasattr(Environment.conf.VenditaDettaglio, "magazzino"):
                findComboboxRowFromStr(self.filters.id_magazzino_filter_combobox, Environment.conf.VenditaDettaglio.magazzino,2)
            if hasattr(Environment.conf.VenditaDettaglio, "puntocassa"):
                findComboboxRowFromStr(self.filters.id_pos_filter_combobox, Environment.conf.VenditaDettaglio.puntocassa,2)
        else:
            if setconf("VenditaDettaglio", "magazzino_vendita"):
                findComboboxRowFromId(self.filters.id_magazzino_filter_combobox,setconf("VenditaDettaglio", "magazzino_vendita"))
            if setconf("VenditaDettaglio", "punto_cassa"):
                findComboboxRowFromId(self.filters.id_pos_filter_combobox, setconf("VenditaDettaglio", "punto_cassa"))

        self.refreshHtml()
        self.refresh()

    def _reOrderBy(self, column):
        if column.get_name() == "data_column":
            return self.filterss._changeOrderBy(column,(None,TestataScontrino.data_inserimento))
        if column.get_name() == "totale_column":
            return self.filterss._changeOrderBy(column,(None,TestataScontrino.totale_scontrino))
        if column.get_name() == "contanti_column":
            return self.filterss._changeOrderBy(column,(None,TestataScontrino.totale_contanti))
        if column.get_name() == "assegni_column":
            return self.filterss._changeOrderBy(column,(None,TestataScontrino.totale_assegni))
        if column.get_name() == "cdicredito_column":
            return self.filterss._changeOrderBy(column,(None,TestataScontrino.totale_carta_credito))

    def clear(self):
        # Annullamento filtro
        self.filters.id_articolo_filter_customcombobox.set_active(0)
        self.filters.id_cliente_search_customcombobox.set_active(0)
        if hasattr(Environment.conf, "VenditaDettaglio"):
            if hasattr(Environment.conf.VenditaDettaglio, "magazzino"):
                findComboboxRowFromStr(self.filters.id_magazzino_filter_combobox, Environment.conf.VenditaDettaglio.magazzino,2)
            if hasattr(Environment.conf.VenditaDettaglio, "puntocassa"):
                findComboboxRowFromStr(self.filters.id_pos_filter_combobox, Environment.conf.VenditaDettaglio.puntocassa,2)
        else:
            if setconf("VenditaDettaglio", "magazzino_vendita"):
                findComboboxRowFromId(self.filters.id_magazzino_filter_combobox,setconf("VenditaDettaglio", "magazzino_vendita"))
            if setconf("VenditaDettaglio", "punto_cassa"):
                findComboboxRowFromId(self.filters.id_pos_filter_combobox, setconf("VenditaDettaglio", "punto_cassa"))

        self.filters.da_data_filter_entry.setNow()
        self.filters.a_data_filter_entry.setNow()
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self.filters.id_articolo_filter_customcombobox.getId()
        daData = stringToDate(self.filters.da_data_filter_entry.get_text())
        aData = stringToDateBumped(self.filters.a_data_filter_entry.get_text())
        idPuntoCassa = findIdFromCombobox(self.filters.id_pos_filter_combobox)
        idMagazzino = findIdFromCombobox(self.filters.id_magazzino_filter_combobox)
        idCliente =  self.filters.id_cliente_search_customcombobox.getId()
        self.filterss.numRecords = TestataScontrino().count(idArticolo=idArticolo,
                                                                      daData=daData,
                                                                      aData=aData,
                                                                      idMagazzino = idMagazzino,
                                                                      idPuntoCassa = idPuntoCassa,
                                                                      idCliente = idCliente)
        self.filterss._refreshPageCount()

        scos = TestataScontrino().select( orderBy=self.filterss.orderBy,
                                                     idArticolo=idArticolo,
                                                     daData=daData,
                                                     aData=aData,
                                                     idMagazzino = idMagazzino,
                                                     idPuntoCassa = idPuntoCassa,
                                                     idCliente = idCliente,
                                                     offset=self.filterss.offset,
                                                     batchSize=self.filterss.batchSize)

        #self.filterss._treeViewModel.clear()
        self.rows_listore.clear()
        for s in scos:
            totale = mNLC(s.totale_scontrino,2) or 0
            contanti = mNLC(s.totale_contanti,2) or 0
            assegni = mNLC(s.totale_assegni,2) or 0
            carta = mNLC(s.totale_carta_credito,2) or 0
            self.rows_listore.append((s,
                                    dateTimeToString(s.data_inserimento).replace(" "," Ore: "),
                                    totale,
                                    contanti, assegni, carta,
                                    dateToString(s.data_movimento),
                                    str(s.numero_movimento or '')))

        scos_no_batchSize = TestataScontrino().select( orderBy=self.filterss.orderBy,
                                                     idArticolo=idArticolo,
                                                     idMagazzino = idMagazzino,
                                                     idPuntoCassa = idPuntoCassa,
                                                     daData=daData,
                                                     aData=aData,
                                                     idCliente=idCliente,
                                                     offset=None,
                                                     batchSize=None)
        self.scontrini = scos_no_batchSize
        self.calcolaTotale(scos_no_batchSize)

    def calcolasconto(self, dao):
        if dao.sconti[0].tipo_sconto=="valore":
            return dao.sconti[0].valore
        else:
            #print ((dao.totale_scontrino*100)/dao.sconti[0].valore), (dao.totale_scontrino)
            return (100 * dao.totale_scontrino) / (100 - dao.sconti[0].valore) -(dao.totale_scontrino)
            #totale_scontato = total-totale_sconto

    def calcolaTotale(self, scos_no_batchSize):
        tot=0
        totccr = 0
        totass = 0
        totnum = 0
        totcont = 0
        tot_sconti = 0
        for m in scos_no_batchSize:
            if m.sconti:
                tot_sconti += self.calcolasconto(m)
            tot += m.totale_scontrino
            totccr += m.totale_carta_credito
            totass += m.totale_assegni
            totcont += m.totale_contanti
            totnum += 1
        self.filterss.label1.set_text("")
        stringa = """GENERALE:<b><span foreground="black" size="20000">%s</span></b> - NUM. SCONTRINI:<b><span foreground="black" size="18000">%s</span></b> TOT CARTA:<b>%s</b> - TOT ASSEGNI:<b>%s</b> - TOT CONT.:<b>%s</b> - TOT SCONTI:<b>%s</b> - """ %(mNLC(tot,2), totnum, mNLC(totccr,2), mNLC(totass,2), mNLC(totcont,2), mNLC(tot_sconti,2) )
        self.filterss.info_label.set_markup(str(stringa))


    def on_filter_treeview_cursor_changed(self, treeview):
        sel = self.filterss.resultsElement.get_selection()
        (model, iterator) = sel.get_selected()

        if iterator is None:
            print 'on_filter_treeview_cursor_changed(): FIXME: iterator is None!'
            return

        self.dao = model.get_value(iterator, 0)
        self.refreshHtml(self.dao)

    def on_filter_treeview_row_activated(self, treeview, path, column):
        # Not used here
        pass

    def on_filter_treeview_selection_changed(self, treeSelection):
        (model, iterator) = treeSelection.get_selected()
        if iterator:
            self.crea_fattura_button.set_sensitive(True)
            self.id_cliente_emessi_customcombobox.set_sensitive(True)
            self.operazione_combobox.set_sensitive(True)
            self.daoTse = model.get_value(iterator, 0)
            if model.get_value(iterator, 0).id_cliente_testata_scontrino:
                a = model.get_value(iterator, 0).id_cliente_testata_scontrino
                self.id_cliente_emessi_customcombobox.setId(a)
            else:
                self.id_cliente_emessi_customcombobox.set_active(0)
                self.operazione_combobox.set_active(0)
                #self.crea_fattura_button.set_sensitive(False)
                #self.id_cliente_emessi_customcombobox.set_sensitive(False)
                #self.operazione_combobox.set_sensitive(False)
                #self.daoTse = None
        else:
            self.id_cliente_emessi_customcombobox.set_active(0)
            self.crea_fattura_button.set_sensitive(False)
            self.id_cliente_emessi_customcombobox.set_sensitive(False)
            self.operazione_combobox.set_sensitive(False)
            self.daoTse = None

    def refreshHtml(self, dao=None):
        pageData = {}
        html = '<html></html>'
        if self.dao:
            pageData = {
                    "file": "scontrino.html",
                    "dao" :self.dao,
                    }
            html = renderTemplate(pageData)
        renderHTML(self.detail,html)

    def on_scontrini_window_close(self, widget, event=None):
        self.destroy()
        return None

    def on_rhesus_button_clicked(self, widget):
        if self.dao is not None:
            self._righe.append(self.dao.id)
            self.on_scontrini_window_close(widget)

    def on_delete_button_clicked(self, button):
        if self.dao is not None:
            msg = """ ATTENZIONE!!!!
    Si sta per cancellare uno scontrino, L'operazione
    è irreversibile per cui dovete essere sicuri di
    quel che state facendo. VUOI CANCELLARLO?"""
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   msg)
            response = dialog.run()
            dialog.destroy()
            if response ==  gtk.RESPONSE_YES:
                if self.dao.numero_movimento:
                    messageInfo(msg= """Esiste già un movimento abbinato di chiusura per scarico da cassa,
        l'operazione è comunque impossibile
        Rivolgersi all'assistenza""")
                else:
                    Environment.pg2log.info("CANCELLO UNO SCONTRINO DAL PG2 ")
                    self.dao.delete()
                self.refresh()
            else:
                return

    def on_affluenza_oraria_chart_clicked(self, button):
        if "Statistiche" in Environment.modulesList and \
            hasattr(Environment.conf,"Statistiche") and \
            hasattr(Environment.conf.Statistiche,"affluenza_oraria_giornaliera") and\
            Environment.conf.Statistiche.affluenza_oraria_giornaliera == "yes":
            from promogest.modules.Statistiche.ui.chart import chartViewer
            chartViewer(self._window, func="affluenzaOrariaGiornaliera",scontrini= self.scontrini)
        else:
            fenceDialog()

    def on_affluenza_mensile_chart_clicked(self, button):
        if "Statistiche" in Environment.modulesList and \
            hasattr(Environment.conf,"Statistiche") and \
            hasattr(Environment.conf.Statistiche,"affluenza_giornaliera_mensile") and\
            Environment.conf.Statistiche.affluenza_giornaliera_mensile == "yes":
            from promogest.modules.Statistiche.ui.chart import chartViewer
            chartViewer(self._window, func="affluenzaGiornalieraMensile", scontrini= self.scontrini)
        else:
            fenceDialog()

    def on_affluenza_annuale_chart_clicked(self, button):
        if "Statistiche" in Environment.modulesList and \
            hasattr(Environment.conf,"Statistiche") and \
            hasattr(Environment.conf.Statistiche,"affluenza_mensile_annuale") and\
            Environment.conf.Statistiche.affluenza_mensile_annuale == "yes":
            from promogest.modules.Statistiche.ui.chart import chartViewer
            chartViewer(self._window, func="affluenzaMensileAnnuale", scontrini= self.scontrini)
        else:
            fenceDialog()

    def on_esporta_affluenza_csv_clicked(self, button):
        print "esport to csv"

    def on_aggiorna_inve_activate(self, item):
        """ Questa funzione serve a ricalibrare le giacenze di inventario con
            gli articoli venduti al dettaglio """
        msg = """ ATTENZIONE!!!!
            QUESTA OPERAZIONE È PERICOLOSSIMA!!!!
            è stata aggiunta per corprire una casistica specifica
            di "aggiornamento della tabella inventario
            rispetto al venduto al dettaglio vuoi farlo??"""
        dialog = gtk.MessageDialog(self.getTopLevel(),
                               gtk.DIALOG_MODAL
                               | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                               msg)
        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            if posso("IN"):
                idMagazzinosel = Magazzino().select(denominazione = Environment.conf.VenditaDettaglio.magazzino)
                if Environment.conf.VenditaDettaglio.jolly:
                    idArticoloGenericoSel = Articolo().select(codiceEM = Environment.conf.VenditaDettaglio.jolly)
                    if idArticoloGenericoSel:
                        idArticoloGenerico = idArticoloGenericoSel[0].id
                    else:
                        idArticoloGenerico = None
                if idMagazzinosel:
                    idMagazzino = idMagazzinosel[0].id
                else:
                    print "ERRORE NELLA DEFINIZIONE DEL MAGAZZINO"
                    return
                for scontrino in self.scontrini:
                    for riga in scontrino.righe:
                        daoInv = Inventario().select(idArticolo=riga.id_articolo, idMagazzino = idMagazzino)
                        if daoInv and idArticoloGenerico!=riga.id_articolo:
                            if daoInv[0].data_aggiornamento is None or scontrino.data_inserimento < daoInv[0].data_aggiornamento:
                                quantitaprecedente = daoInv[0].quantita or 0
                                quantitavenduta = riga.quantita
                                nuovaquantita = quantitaprecedente+quantitavenduta
                                print "OPERAZIONE DA EFFETTUARE", quantitaprecedente,quantitavenduta, nuovaquantita
                                daoInv[0].quantita= nuovaquantita
                                daoInv[0].persist()
            else:
                print "IL MODULO INVENTARIO NON e' ATTIVO "

    def on_distinta_button_clicked(self, button):
        gest = Distinta(righe = self.scontrini)
        gestWnd = gest.getTopLevel()
        showAnagraficaRichiamata(self.getTopLevel(), gestWnd, None, None)

    def ricercaListino(self):
        """ check if there is a priceList like setted on configure file
        """
        if hasattr(Environment.conf, "VenditaDettaglio"):
            if hasattr(Environment.conf.VenditaDettaglio,"listino"):
                pricelist = Listino().select(denominazione = Environment.conf.VenditaDettaglio.listino,
                                        offset = None,
                                        batchSize = None)
            else:
                pricelist = Listino().select(id=setconf("VenditaDettaglio", "listino_vendita"))

        else:
            pricelist = Listino().select(id=setconf("VenditaDettaglio", "listino_vendita"))
        if pricelist:
            id_listino = pricelist[0].id
        else:
            id_listino = None
        return id_listino

    def on_crea_fattura_button_clicked(self, button):
        """ RIGA DOCUMENTO:
            id, valore_unitario_netto, valore_unitario_lordo,
            quantita, moltiplicatore, applicazione_sconti,
            percentuale_iva, descrizione, id_articolo, id_magazzino,
            id_multiplo, id_listino, id_iva, id_riga_padre

            RIGA SCONTRINO:
            id, prezzo, prezzo_scontato, quantita,
            descrizione, id_testata_scontrino, id_articolo
            TODO: Vanno gestiti gli sconti
            """
        if not self.daoTse:
            messageInfo(msg="Nessuno scontrino selezionato")
            return
        if self.daoTse and not self.daoTse.id_cliente_testata_scontrino:
            if self.id_cliente_emessi_customcombobox.getId():
                a = TestataScontrinoCliente()
                a.id_cliente =  self.id_cliente_emessi_customcombobox.getId()
                a.id_testata_scontrino = self.daoTse.id
                a.persist()
            else:
                messageInfo(msg="Scontrino selezionato, ma nessun cliente assegnato")
            return
        if not findStrFromCombobox(self.operazione_combobox,0):
            obligatoryField(self.getTopLevel(), self.operazione_combobox, msg="SELEZIONA IL TIPO DOCUMENTO")
        one_day = datetime.timedelta(days=1)
        proviamo = datetime.datetime(self.daoTse.data_inserimento.year,self.daoTse.data_inserimento.month,
        self.daoTse.data_inserimento.day)
        listascontrini = TestataScontrino().select(daData=proviamo, aData=proviamo+one_day, batchSize=None, orderBy="data_inserimento")
        a = [i for i,x in enumerate(listascontrini) if x == self.daoTse]
        if a:
            a = a[0]
        else:
            a=0
        posizione= a + 1
        note = "Rif. Scontrino" + " n. " + str(posizione) + " del " + dateToString(self.daoTse.data_inserimento)

        newDao = TestataDocumento()
        newDao.data_documento = stringToDate(self.daoTse.data_inserimento)
        newDao.operazione = findStrFromCombobox(self.operazione_combobox,0)
        newDao.id_cliente = self.id_cliente_emessi_customcombobox.getId()
        newDao.note_pie_pagina = note
        #newDao.applicazione_sconti = self.dao.applicazione_sconti
        #sconti = []
        #sco = self.dao.sconti or []
        scontiRigaDocumento=[]
        scontiSuTotale=[]
        righeDocumento=[]
        #for s in sco:
            #daoSconto = ScontoTestataDocumento()
            #daoSconto.valore = s.valore
            #daoSconto.tipo_sconto = s.tipo_sconto
            #scontiSuTotale.append(daoSconto)
        newDao.scontiSuTotale = scontiSuTotale
        #righe = []
        rig = self.daoTse.righe
        for r in rig:
            daoRiga = RigaDocumento()
            daoRiga.id_testata_documento = newDao.id
            daoRiga.id_articolo = r.id_articolo
            daoRiga.id_magazzino = self.daoTse.id_magazzino
            daoRiga.descrizione = r.descrizione
            # Copia il campo iva
            arto = leggiArticolo(r.id_articolo)
            daoRiga.id_iva = arto["idAliquotaIva"]
            #ricalcola prezzi
            daoRiga.id_listino = self.ricercaListino()
            imponibile = float(r.prezzo)/(1+float(arto["percentualeAliquotaIva"])/100)
            imponibile_scontato = float(r.prezzo_scontato)/(1+float(arto["percentualeAliquotaIva"])/100)
            daoRiga.valore_unitario_lordo = imponibile or 0
            daoRiga.valore_unitario_netto =  imponibile_scontato

            daoRiga.percentuale_iva = arto["percentualeAliquotaIva"]

            #daoRiga.applicazione_sconti = r.applicazione_sconti
            daoRiga.quantita = r.quantita
            daoRiga.id_multiplo = None
            daoRiga.moltiplicatore = 1
            #sconti = []
            scontiRigaDocumento = []
            #sco = r.sconti
            #for s in sco:
                #daoSconto = ScontoRigaDocumento()
                #daoSconto.valore = s.valore
                #daoSconto.tipo_sconto = s.tipo_sconto
                #scontiRigaDocumento.append(daoSconto)
            daoRiga.scontiRigaDocumento = scontiRigaDocumento
            righeDocumento.append(daoRiga)

        newDao.righeDocumento = righeDocumento

        tipoid = findStrFromCombobox(self.operazione_combobox,0)
        #tipo = Operazione().getRecord(id=tipoid)
        #if not newDao.numero:
        valori = numeroRegistroGet(tipo=tipoid, date=self.daoTse.data_inserimento)
        newDao.numero = valori[0]
        newDao.registro_numerazione= valori[1]
        newDao.persist()

        res = TestataDocumento().getRecord(id=newDao.id)

        msg = "Documento creato da scontrino !\n\nIl nuovo documento e' il n. " + str(res.numero) + " del " + dateToString(res.data_documento) + " (" + newDao.operazione + ")\n" + "Lo vuoi modificare?"
        if YesNoDialog(msg=msg, transient=self.getTopLevel()):
            from promogest.ui.AnagraficaDocumenti import AnagraficaDocumenti
            anag = AnagraficaDocumenti()
            anagWindow = anag.getTopLevel()
            anagWindow.show_all()
            anag.editElement.setVisible(True)
            anag.editElement.setDao(newDao)
            anag.editElement.id_persona_giuridica_customcombobox.set_sensitive(True)
            anag.editElement.setFocus()
        self.destroy()
