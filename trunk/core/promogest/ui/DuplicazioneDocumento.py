# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

import os
import gtk, gobject
import gtk
from GladeWidget import GladeWidget

from promogest import Environment
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
from promogest.dao.Operazione import Operazione
if Environment.conf.hasPagamenti == True:
    import promogest.modules.Pagamenti.dao.TestataDocumentoScadenza
    from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from utils import *



class DuplicazioneDocumento(GladeWidget):

    def __init__(self, daoDocumento):

        self.dao = daoDocumento

        GladeWidget.__init__(self, 'duplicazione_documento_window', 'duplicazione_documento.glade')
        self.placeWindow(self.getTopLevel())
        self.draw()


    def draw(self):
        # seleziona i tipi documento compatibili
        operazione = leggiOperazione(self.dao.operazione)
        res = Environment.params['session'].query(Operazione).filter(and_(or_(Operazione.tipo_operazione==None,
                                                                    Operazione.tipo_operazione =="documento"),
                                                                    (Operazione.fonte_valore == operazione["fonteValore"]),
                                                                    (Operazione.tipo_persona_giuridica == operazione["tipoPersonaGiuridica"]))).all()
        model = gtk.ListStore(object, str, str)
        for o in res:
            model.append((o, o.denominazione, (o.denominazione or '')[0:30]))

        self.id_operazione_combobox.clear()
        renderer = gtk.CellRendererText()
        self.id_operazione_combobox.pack_start(renderer, True)
        self.id_operazione_combobox.add_attribute(renderer, 'text', 2)
        self.id_operazione_combobox.set_model(model)

        self.data_documento_entry.set_text(dateToString(datetime.datetime.today()))
        self.data_documento_entry.grab_focus()
        self.getTopLevel().show_all()


    def on_confirm_button_clicked(self, button=None):

        if (self.data_documento_entry.get_text() == ''):
            obligatoryField(self.getTopLevel(), self.data_documento_entry)

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            obligatoryField(self.getTopLevel(), self.id_operazione_combobox)

        note = "Rif. " + self.dao.operazione + " n. " + str(self.dao.numero) + " del " + dateToString(self.dao.data_documento)

        newDao = TestataDocumento()
        newDao.data_documento = stringToDate(self.data_documento_entry.get_text())
        newDao.operazione = findIdFromCombobox(self.id_operazione_combobox)
        newDao.id_cliente = self.dao.id_cliente
        newDao.id_fornitore = self.dao.id_fornitore
        newDao.id_destinazione_merce = self.dao.id_destinazione_merce
        newDao.id_pagamento = self.dao.id_pagamento
        newDao.id_banca = self.dao.id_banca
        newDao.id_aliquota_iva_esenzione = self.dao.id_aliquota_iva_esenzione
        newDao.protocollo = self.dao.protocollo
        newDao.causale_trasporto = self.dao.causale_trasporto
        newDao.aspetto_esteriore_beni = self.dao.aspetto_esteriore_beni
        newDao.inizio_trasporto = self.dao.inizio_trasporto
        newDao.fine_trasporto = self.dao.fine_trasporto
        newDao.id_vettore =self.dao.id_vettore
        newDao.incaricato_trasporto = self.dao.incaricato_trasporto
        newDao.totale_colli = self.dao.totale_colli
        newDao.totale_peso = self.dao.totale_peso
        newDao.note_interne = self.dao.note_interne
        newDao.note_pie_pagina = self.dao.note_pie_pagina + " " + note
        newDao.applicazione_sconti = self.dao.applicazione_sconti
        newDao.ripartire_importo = self.dao.ripartire_importo
        newDao.costo_da_ripartire = self.dao.costo_da_ripartire
        #sconti = []
        sco = self.dao.sconti or []
        scontiRigaDocumento=[]
        scontiSuTotale=[]
        righeDocumento=[]
        for s in sco:
            daoSconto = ScontoTestataDocumento()
            daoSconto.valore = s.valore
            daoSconto.tipo_sconto = s.tipo_sconto
            scontiSuTotale.append(daoSconto)
        newDao.scontiSuTotale = scontiSuTotale
        #righe = []
        rig = self.dao.righe
        for r in rig:
            daoRiga = RigaDocumento()
            daoRiga.id_testata_documento = newDao.id
            daoRiga.id_articolo = r.id_articolo
            daoRiga.id_magazzino = r.id_magazzino
            daoRiga.descrizione = r.descrizione
            daoRiga.id_listino = r.id_listino
            daoRiga.percentuale_iva = r.percentuale_iva
            daoRiga.applicazione_sconti = r.applicazione_sconti
            daoRiga.quantita = r.quantita
            daoRiga.id_multiplo = r.id_multiplo
            daoRiga.moltiplicatore = r.moltiplicatore
            daoRiga.valore_unitario_lordo = r.valore_unitario_lordo
            daoRiga.valore_unitario_netto = r.valore_unitario_netto
            if "SuMisura" in Environment.modulesList:
                from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
                daoMisuraPezzo = MisuraPezzo()
                daoMisuraPezzo.altezza = r.misura_pezzo[0].altezza
                daoMisuraPezzo.larghezza = r.misura_pezzo[0].larghezza
                daoMisuraPezzo.moltiplicatore = r.misura_pezzo[0].moltiplicatore
                daoRiga.misura_pezzo = daoMisuraPezzo
            sconti = []
            scontiRigaDocumento = []
            sco = r.sconti
            for s in sco:
                daoSconto = ScontoRigaDocumento()
                daoSconto.valore = s.valore
                daoSconto.tipo_sconto = s.tipo_sconto
                scontiRigaDocumento.append(daoSconto)
            daoRiga.scontiRigaDocumento = scontiRigaDocumento
            righeDocumento.append(daoRiga)
        newDao.righeDocumento = righeDocumento
        scadenze = []
        if Environment.conf.hasPagamenti == True:
            scad = self.dao.scadenze
            for s in scad:
                daoTestataDocumentoScadenza = TestataDocumentoScadenza()
                daoTestataDocumentoScadenza.id_testata_documento = newDao.id
                daoTestataDocumentoScadenza.data = s.data
                daoTestataDocumentoScadenza.importo = s.importo
                daoTestataDocumentoScadenza.pagamento = s.pagamento
                daoTestataDocumentoScadenza.data_pagamento= s.data_pagamento
                daoTestataDocumentoScadenza.numero_scadenza = s.numero_scadenza
                scadenze.append(daoTestataDocumentoScadenza)
            newDao.scadenze = scadenze
            newDao.totale_pagato = self.dao.totale_pagato
            newDao.totale_sospeso = self.dao.totale_sospeso
            newDao.documento_saldato = self.dao.documento_saldato
            newDao.id_primo_riferimento = self.dao.id_primo_riferimento
            newDao.id_secondo_riferimento = self.dao.id_secondo_riferimento
        newDao.totale_pagato = self.dao.totale_pagato
        newDao.totale_sospeso = self.dao.totale_sospeso
        newDao.documento_saldato = self.dao.documento_saldato
        newDao.id_primo_riferimento = self.dao.id_primo_riferimento
        newDao.id_secondo_riferimento = self.dao.id_secondo_riferimento
        scadenze = []
        scad = self.dao.scadenze
        for s in scad:
            daoTestataDocumentoScadenza = TestataDocumentoScadenza()
            daoTestataDocumentoScadenza.id_testata_documento = newDao.id
            daoTestataDocumentoScadenza.data = s.data
            daoTestataDocumentoScadenza.importo = s.importo
            daoTestataDocumentoScadenza.pagamento = s.pagamento
            daoTestataDocumentoScadenza.data_pagamento= s.data_pagamento
            daoTestataDocumentoScadenza.numero_scadenza = s.numero_scadenza
            scadenze.append(daoTestataDocumentoScadenza)
        newDao.scadenze = scadenze
        tipoid = findIdFromCombobox(self.id_operazione_combobox)
        tipo = Operazione().getRecord(id=tipoid)
        if not newDao.numero:
            valori = numeroRegistroGet(tipo=tipo.denominazione, date=self.data_documento_entry.get_text())
            newDao.numero = valori[0]
            newDao.registro_numerazione= valori[1]

        newDao.persist()

        res = TestataDocumento().getRecord(id=newDao.id)

        msg = "Nuovo documento creato !\n\nIl nuovo documento e' il n. " + str(res.numero) + " del " + dateToString(res.data_documento) + " (" + newDao.operazione + ")"
        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
        response = dialog.run()
        dialog.destroy()

        self.destroy()


    def on_duplicazione_documento_window_close(self, widget, event=None):
        self.destroy()
        return None
