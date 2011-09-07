# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import os, popen2
from datetime import datetime
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Articolo import Articolo
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.Magazzino import Magazzino
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino
from promogest.modules.VenditaDettaglio.dao.ChiusuraFiscale import ChiusuraFiscale
from promogest.ui.utils import *
from promogest.modules.VenditaDettaglio.ui.VenditaDettaglioUtils import fillComboboxPos
from promogest.modules.VenditaDettaglio.dao.Pos import Pos

class GestioneChiusuraFiscale(GladeWidget):
    """ Classe per la gestione degli scontrini emessi """
    def __init__(self, gladeobj):
        GladeWidget.__init__(self, 'chiusura_dialog',
                fileName='VenditaDettaglio/gui/chiusura_fine_giornata.glade',
                isModule=True)
        self.gladeobj = gladeobj
        self.idMagazzino = None
        self.idPuntoCassa = None
        self.__draw()


    def __draw(self):
        fillComboboxMagazzini(self.chiusura_id_magazzino_combobox)
        if hasattr(Environment.conf, "VenditaDettaglio"):
            if hasattr(Environment.conf.VenditaDettaglio, "magazzino"):
                findComboboxRowFromStr(self.chiusura_id_magazzino_combobox, Environment.conf.VenditaDettaglio.magazzino,2)
        elif setconf("VenditaDettaglio", "magazzino_vendita"):
            findComboboxRowFromId(self.chiusura_id_magazzino_combobox, setconf("VenditaDettaglio", "magazzino_vendita"))
        fillComboboxPos(self.chiusura_id_pos_combobox)
        if hasattr(Environment.conf, "VenditaDettaglio"):
            if hasattr(Environment.conf.VenditaDettaglio, "puntocassa"):
                findComboboxRowFromStr(self.chiusura_id_pos_combobox, Environment.conf.VenditaDettaglio.puntocassa,2)
        elif setconf("VenditaDettaglio", "punto_cassa"):
            findComboboxRowFromId(self.chiusura_id_pos_combobox,setconf("VenditaDettaglio", "punto_cassa"))
        self.chiusura_date_datewidget.setNow()

    def on_ok_chiusura_button_clicked(self, button):
        # controllo se vi e` gia` stata una chiusura
        data = stringToDate(self.chiusura_date_datewidget.get_text())
        self.idPuntoCassa = findIdFromCombobox(self.chiusura_id_pos_combobox)
        self.idMagazzino = findIdFromCombobox(self.chiusura_id_magazzino_combobox)
        chiusure = ChiusuraFiscale().select( dataChiusura = data,
                                            offset = None,
                                            idMagazzino = self.idMagazzino,
                                            idPuntoCassa = self.idPuntoCassa,
                                            batchSize = None)
        if chiusure :
            msg = "ATTENZIONE:\n La chiusura odierna e` gia' stata effettuata"
            messageError(msg=msg, transient =self.getTopLevel())
            return
        self.close_day(self.idMagazzino, data)

    def on_no_chiusura_button_clicked(self, button):
        self.chiusura_dialog.hide()

    def close_day(self, idMagazzino, data):
        # Seleziono scontrini della giornata

        datefirst = data
        OneDay = datetime.timedelta(days=1)
        aData= data+OneDay
        scontrini = TestataScontrino().select(daData = datefirst,
                                            aData = aData,  # Scontrini prodotti nella giornata odierna
                                            idMagazzino = self.idMagazzino,
                                            idPuntoCassa = self.idPuntoCassa,
                                            offset = None,
                                            batchSize = None)
        ##Environment.pg2log.info( "SCONTRINI PRODOTTI IN GIORNATA N° %s dettaglio: %s" ) %(str(len(scontrini)or""), str(scontrini)or"")
        # Creo nuovo movimento
        if self.idMagazzino:
            mag = Magazzino().getRecord(id=self.idMagazzino)
            if mag:
                nomeMagazzino = mag.denominazione
        else:
            nomeMagazzino = " "
        if self.idPuntoCassa:
            pos = Pos().getRecord(id= self.idPuntoCassa)
            if pos:
                nomePuntoCassa = pos.denominazione
        else:
            nomePuntoCassa = " "

        daoMovimento = TestataMovimento()
        #if hasattr(Environment.conf, "VenditaDettaglio"):
            #daoMovimento.operazione = Environment.conf.VenditaDettaglio.operazione
        #else:
        daoMovimento.operazione = setconf("VenditaDettaglio", "operazione")
        daoMovimento.data_movimento = datefirst
        daoMovimento.note_interne = """Movimento chiusura fiscale  magazzino: %s, punto cassa: %s """ %(str(nomeMagazzino),str(nomePuntoCassa))
        righeMovimento = []

        scontiRigheMovimento= []

        dictRigheProv = {}

        for scontrino in scontrini:
            for riga in scontrino.righe:
                cri = str(riga.id_articolo)+"_"+str(riga.prezzo_scontato)
                if  cri in dictRigheProv:
                    daoss = dictRigheProv[cri]
                    daoss.append(riga)
                    dictRigheProv[cri] = daoss
                else:
                    daoss = []
                    daoss.append(riga)
                    dictRigheProv[cri] = daoss

        listRighe = []
        for k,v in dictRigheProv.iteritems():
            if len(v) ==1:
                listRighe.append(v[0])
                #print " QUESTO é SOLO", v[0].quantita
            else:
                listPrezzi = []
                quantita = 0
                for a in v:
                    #print "IN COMPAGNIA", a.id_articolo, a.prezzo_scontato, a.quantita
                    quantita += a.quantita
                v[0].quantita = quantita
                listRighe.append(v[0])

        for riga in listRighe:

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
            daoRiga.id_magazzino = self.idMagazzino
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
        daoChiusura.id_magazzino = self.idMagazzino
        daoChiusura.id_pos = self.idPuntoCassa
        daoChiusura.persist()

        # Creo il file
        filechiusura = self.create_fiscal_close_file()
        # Mando comando alle casse
        #if hasattr(Environment.conf, "VenditaDettaglio"):
            #if not(hasattr(Environment.conf.VenditaDettaglio,'disabilita_stampa_chiusura') and \
                    #Environment.conf.VenditaDettaglio.disabilita_stampa_chiusura == 'yes'):
                #program_launch = Environment.conf.VenditaDettaglio.driver_command
                #program_params = (' ' + filechiusura + ' ' +
                                  #Environment.conf.VenditaDettaglio.serial_device)

                #if os.name == 'nt':
                    #exportingProcessPid = os.spawnl(os.P_NOWAIT, program_launch, program_params)
                    #id, ret_value = os.waitpid(exportingProcessPid, 0)
                    #ret_value = ret_value >> 8
                #else:
                    #command = program_launch + program_params
                    #process = popen2.Popen3(command, True)
                    #message = process.childerr.readlines()
                    #ret_value = process.wait()
            #else:
                #ret_value = 0
        if setconf("VenditaDettaglio", "disabilita_stampa_chiusura"):
            ret_value = 0
        else:
            ret_value = 0

        # Elimino il file
        #os.remove(filechiusura)
        if ret_value != 0:
            string_message = ''
            for s in message:
                string_message = string_message + s + "\n"

            # Mostro messaggio di errore
            messageError(msg=string_message, transient=self.gladeobj.getTopLevel())
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
        self.fineElaborazione()

    def create_fiscal_close_file(self):
        # Genero nome file
        try: # vecchio stile ...adattamento ai dati in setconf
            path = Environment.conf.VenditaDettaglio.export_path
        except: # prendo la cartella temp standard
            path = Environment.tempDir
        filename = path + 'fiscal_close_' + datetime.date.today().strftime('%d_%m_%Y_%H_%M_%S')
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

    def fineElaborazione(self):
        """ Messaggio di fine elaborazione """
        messageInfo(msg="Elaborazione terminata")
