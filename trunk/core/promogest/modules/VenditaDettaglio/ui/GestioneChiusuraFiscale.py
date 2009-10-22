# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import gtk
import os, popen2
from datetime import datetime, timedelta
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Articolo import Articolo
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
from promogest.modules.VenditaDettaglio.dao.ChiusuraFiscale import ChiusuraFiscale
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.ui.utils import *

class GestioneChiusuraFiscale(object):
    """ Classe per la gestione degli scontrini emessi """
    def __init__(self,gladeobj):
        self.gladeobj = gladeobj

    def chiusuraDialog(self, widget, idMagazzino):
        dialog = gtk.MessageDialog(self.gladeobj.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO)
        dialog.set_markup("""<b>ATTENZIONE</b>: Chiusura fiscale!
    Confermi la data?
    Se non sai cosa stai facendo lascia la data odierna impostata
    e contatta la Promotux""")
        hbox = gtk.HBox()
        entry = self.gladeobj.data_chiusura
        entry.setNow()
        hbox.pack_start(entry, False, False, 0)
        dialog.vbox.pack_start(hbox, False, False, 0)
        dialog.show_all()
        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            # controllo se vi e` gia` stata una chiusura
            data = stringToDate(entry.get_text())
            chiusure = ChiusuraFiscale().select( dataChiusura = data,
                                                offset = None,
                                                batchSize = None)
            if len(chiusure) != 0:
                dialog = gtk.MessageDialog(self.gladeobj.getTopLevel(),
                                           gtk.DIALOG_MODAL
                                           | gtk.DIALOG_DESTROY_WITH_PARENT,
                                           gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
                dialog.set_markup("<b>ATTENZIONE:\n La chiusura odierna e` gia' stata effettuata</b>")
                response = dialog.run()
                dialog.destroy()
                return
            self.close_day(idMagazzino, data)
        else:
            return

    def close_day(self, idMagazzino, data):
        # Seleziono scontrini della giornata

        datefirst = data
        OneDay = datetime.timedelta(days=1)
        aData= data+OneDay
        scontrini = TestataScontrino().select(daData = datefirst,
                                            aData = aData,  # Scontrini prodotti nella giornata odierna
                                            offset = None,
                                            batchSize = None)
        Environment.pg2log.info( "SCONTRINI PRODOTTI IN GIORNATA N° %s dettaglio: %s" ) %(str(len(scontrini)), str(scontrini))
        # Creo nuovo movimento
        daoMovimento = TestataMovimento()
        daoMovimento.operazione = Environment.conf.VenditaDettaglio.operazione
        daoMovimento.data_movimento = datefirst
        daoMovimento.note_interne = 'Movimento chiusura fiscale'
        righeMovimento = []

        scontiRigheMovimento= []
        for scontrino in scontrini:
            for riga in scontrino.righe:
                # Istanzio articolo
                art = Articolo().getRecord(id=riga.id_articolo)
                # Cerco IVA
                iva = AliquotaIva().getRecord(id=art.id_aliquota_iva)

                daoRiga = RigaMovimento()
                daoRiga.valore_unitario_lordo = riga.prezzo
                daoRiga.valore_unitario_netto = riga.prezzo_scontato
                daoRiga.quantita = riga.quantita
                daoRiga.moltiplicatore = 1
                daoRiga.descrizione = riga.descrizione
                daoRiga.id_magazzino = idMagazzino
                daoRiga.id_articolo = riga.id_articolo
                daoRiga.percentuale_iva = iva.percentuale
                scontiRigheMovimento= []
                if riga.sconti:
                    for s in riga.sconti:
                        daoScontoRigaMovimento = ScontoRigaMovimento()
                        daoScontoRigaMovimento.valore = s.valore
                        daoScontoRigaMovimento.tipo_sconto = s.tipo_sconto
                        scontiRigheMovimento.append(daoScontoRigaMovimento)
                daoRiga.scontiRigheMovimento = scontiRigheMovimento
                scontiRigheMovimento= []
                righeMovimento.append(daoRiga)

        daoMovimento.righeMovimento = righeMovimento
        daoMovimento.persist()

        # Creo nuova chiusura
        daoChiusura = ChiusuraFiscale()
        daoChiusura.data_chiusura = datefirst
        daoChiusura.persist()
        #daoChiusura.update()

        # Creo il file
        filechiusura = self.create_fiscal_close_file()
        # Mando comando alle casse
        if not(hasattr(Environment.conf.VenditaDettaglio,'disabilita_stampa_chiusura') and Environment.conf.VenditaDettaglio.disabilita_stampa_chiusura == 'yes'):
            program_launch = Environment.conf.VenditaDettaglio.driver_command
            program_params = (' ' + filechiusura + ' ' +
                              Environment.conf.VenditaDettaglio.serial_device)

            if os.name == 'nt':
                exportingProcessPid = os.spawnl(os.P_NOWAIT, program_launch, program_params)
                id, ret_value = os.waitpid(exportingProcessPid, 0)
                ret_value = ret_value >> 8
            else:
                command = program_launch + program_params
                process = popen2.Popen3(command, True)
                message = process.childerr.readlines()
                ret_value = process.wait()
        else:
            ret_value = 0

        # Elimino il file
        #os.remove(filechiusura)
        if ret_value != 0:
            string_message = ''
            for s in message:
                string_message = string_message + s + "\n"

            # Mostro messaggio di errore
            dialog = gtk.MessageDialog(self.gladeobj.getTopLevel(),
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                       string_message)
            response = dialog.run()
            dialog.destroy()
            # Elimino il movimento e la chiusura
            daoChiusura.delete()
            daoChiusura = None
            daoMovimento.delete()
            daoMovimento = None

        if daoMovimento is not None:
            # Associo movimento agli scontrini
            for scontrino in scontrini:
                daoScontrino = TestataScontrino().getRecord(id=scontrino.id)
                daoScontrino.id_testata_movimento = daoMovimento.id
                daoScontrino.persist(chiusura= True)

        # Svuoto transazione
        self.on_empty_button_clicked(self.gladeobj.empty_button)

    def create_fiscal_close_file(self):
        # Genero nome file
        filename = Environment.conf.VenditaDettaglio.export_path + 'fiscal_close_' + datetime.date.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename,'w')
        stringa = '51                00000000002..\r\n'
        f.write(stringa)
        f.close()
        return filename

    def on_empty_button_clicked(self, button):
        self.gladeobj.scontrino_treeview.get_model().clear()
        #self.empty_current_row()
        self.gladeobj.label_totale.set_markup('<b><span size="xx-large">0.00</span></b>')
        self.gladeobj.label_resto.set_markup('<b><span size="xx-large">0.00</span></b>')
        self.gladeobj.empty_button.set_sensitive(False)
        self.gladeobj.total_button.set_sensitive(False)
        #self.setPagamento(enabled = False)
        self.gladeobj.codice_a_barre_entry.grab_focus()
