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
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.dao.Operazione import Operazione
from AnagraficaDocumenti import *
if Environment.conf.hasPagamenti == True:
    import promogest.modules.Pagamenti.dao.TestataDocumentoScadenza
    from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from utils import *



class DuplicazioneMovimento(GladeWidget):

    def __init__(self, daoMovimento, anagraficaMovimenti):

        self.dao = daoMovimento
        self.anagrafica_movimenti = anagraficaMovimenti

        GladeWidget.__init__(self, 'duplicazione_movimento_window', 'duplicazione_movimento.glade')
        self.placeWindow(self.getTopLevel())
        self.draw()


    def draw(self):
        
        operazione = leggiOperazione(self.dao.operazione)
        self.tipoPersonaGiuridica = operazione['tipoPersonaGiuridica']
        self.persona_label.set_text(self.tipoPersonaGiuridica.capitalize())
        self.id_persona_giuridica_customcombobox.setType(self.tipoPersonaGiuridica)
        
        res = Environment.params['session'].query(Operazione).all()
        
        model = gtk.ListStore(object, str, str)
        for o in res:
            model.append((o, o.denominazione, (o.denominazione or '')[0:30]))

        self.id_operazione_combobox.clear()
        renderer = gtk.CellRendererText()
        self.id_operazione_combobox.pack_start(renderer, True)
        self.id_operazione_combobox.add_attribute(renderer, 'text', 2)
        self.id_operazione_combobox.set_model(model)

        self.data_movimento_entry.set_text(dateToString(datetime.datetime.today()))
        self.data_movimento_entry.grab_focus()
        #self.getTopLevel().show_all()
        #self.show_all()

        listini = Environment.params['session'].query(Listino)
        model = gtk.ListStore(object, str)
        model.append((None, '<Invariato>'))
        for l in listini:
            model.append((l, (l.denominazione or '')[0:30]))                
        self.id_prezzo_combobox.clear()
        renderer = gtk.CellRendererText()
        self.id_prezzo_combobox.pack_start(renderer, True)
        self.id_prezzo_combobox.add_attribute(renderer, 'text', 1)
        self.id_prezzo_combobox.set_model(model)
        self.id_prezzo_combobox.set_active(0)
        
        #controlla che nel documento ci sia un solo magazzino
        nMags = Environment.params['session'].query(Magazzino).count()
        if nMags > 1:
          if self.dao.numeroMagazzini == 1:
            mags = Environment.params['session'].query(Magazzino)#.filter(Magazzino.id != self.dao.righe[0].id_magazzino)
            model = gtk.ListStore(object, str)
            for m in mags:
                model.append((m, (m.denominazione or '')[0:30]))                
            self.id_magazzino_combobox.clear()
            renderer = gtk.CellRendererText()
            self.id_magazzino_combobox.pack_start(renderer, True)
            self.id_magazzino_combobox.add_attribute(renderer, 'text', 1)
            self.id_magazzino_combobox.set_model(model)
          else:
            #disabilito il cambio di magazzino
            self.id_magazzino_combobox.set_sensitive(False)
        else:
          #disabilito il cambio di magazzino
          self.id_magazzino_combobox.set_sensitive(False)
    
    def on_confirm_button_clicked(self, button=None):
        
        if (self.data_movimento_entry.get_text() == ''):
            obligatoryField(self.getTopLevel(), self.data_movimento_entry)

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            obligatoryField(self.getTopLevel(), self.id_operazione_combobox)

        note = "Rif. " + self.dao.operazione + " n. " + str(self.dao.numero) + " del " + dateToString(self.dao.data_movimento)

        newDao = TestataMovimento()
        newDao.data_movimento = stringToDate(self.data_movimento_entry.get_text())
        newDao.numero = self.dao.numero
        newDao.parte = self.dao.parte
        newDao.registro_numerazione = self.dao.registro_numerazione
        newDao.operazione = findIdFromCombobox(self.id_operazione_combobox)
        newDao.note_interne = self.dao.note_interne
        newDao.note_pie_pagina = self.dao.note_pie_pagina
        newDao.id_testata_documento = self.dao.id_testata_documento
        if  self.personaGiuridicaCambiata:
            if (self.id_persona_giuridica_customcombobox.getId() is None):
              obligatoryField(self.getTopLevel(), self.id_persona_giuridica_customcombobox)
            if self.id_persona_giuridica_customcombobox.getType() == "cliente":
              newDao.id_cliente = self.id_persona_giuridica_customcombobox.getId()
              newDao.id_fornitore = None
            else:
              newDao.id_fornitore = self.id_persona_giuridica_customcombobox.getId()
              newDao.id_cliente = None  
        elif not self.persona_giuridica_sensitive:
          newDao.id_fornitore = None
          newDao.id_cliente = None
        else:
          newDao.id_fornitore = self.dao.id_fornitore
          newDao.id_cliente = self.dao.id_cliente
        righe = []
        righeMovimento = []
        rig = self.dao.righe
        for r in rig:
            daoRiga = RigaMovimento(Environment.connection)
            daoRiga.id_testata_movimento = newDao.id
            daoRiga.id_articolo = r.id_articolo
            if self.id_magazzino_combobox.get_active() != -1:
                magazzino_model = self.id_magazzino_combobox.get_model()
                magazzino_active = self.id_magazzino_combobox.get_active()
                daoRiga.id_magazzino = magazzino_model[magazzino_active][0].id
            else:
                daoRiga.id_magazzino = r.id_magazzino
            daoRiga.descrizione = r.descrizione
            daoRiga.id_listino = r.id_listino
            daoRiga.percentuale_iva = r.percentuale_iva
            daoRiga.applicazione_sconti = r.applicazione_sconti
            daoRiga.quantita = r.quantita
            daoRiga.id_multiplo = r.id_multiplo
            daoRiga.moltiplicatore = r.moltiplicatore
            #ricalcola prezzi
            listino = self.id_prezzo_combobox.get_model()[self.id_prezzo_combobox.get_active()][0]
            if  listino is None:
              daoRiga.id_listino = r.id_listino
              daoRiga.valore_unitario_lordo = r.valore_unitario_lordo
              daoRiga.valore_unitario_netto = r.valore_unitario_netto
            else:
              #ricalcola prezzi
              listinoArticolo = Environment.params['session'].query(ListinoArticolo).filter(ListinoArticolo.id_listino == listino.id and r.id_articolo == ListinoArticolo.id_articolo).all()
              if len(listinoArticolo) > 0:
                daoRiga.id_listino = listinoArticolo[0].id_listino
                daoRiga.valore_unitario_lordo = listinoArticolo[0].prezzo_dettaglio
                daoRiga.valore_unitario_netto = listinoArticolo[0].prezzo_ingrosso
              else:
                daoRiga.id_listino = r.id_listino
                daoRiga.valore_unitario_lordo = r.valore_unitario_lordo
                daoRiga.valore_unitario_netto = r.valore_unitario_netto
            sconti = []
            scontiRigaMovimento = []
            sco = r.sconti
            if self.mantieni_sconti_checkbutton.get_active() :
              for s in sco:
                  daoSconto = ScontoRigaMovimento()
                  daoSconto.valore = s.valore
                  daoSconto.tipo_sconto = s.tipo_sconto
                  scontiRigaMovimento.append(daoSconto)
            daoRiga.scontiRigheMovimento = scontiRigaMovimento
            righeMovimento.append(daoRiga)

        newDao.righeMovimento = righeMovimento
        #newDao.totale_pagato = self.dao.totale_pagato
        #newDao.totale_sospeso = self.dao.totale_sospeso
        #newDao.documento_saldato = self.dao.documento_saldato
        #newDao.id_secondo_riferimento = self.dao.id_secondo_riferimento
        #scadenze = []
        #scad = self.dao.scadenze
        #for s in scad:
            #daoTestataDocumentoScadenza = TestataDocumentoScadenza()
            #daoTestataDocumentoScadenza.id_testata_documento = newDao.id
            #daoTestataDocumentoScadenza.data = s.data
            #daoTestataDocumentoScadenza.importo = s.importo
            #daoTestataDocumentoScadenza.pagamento = s.pagamento
            #daoTestataDocumentoScadenza.data_pagamento= s.data_pagamento
            #daoTestataDocumentoScadenza.numero_scadenza = s.numero_scadenza
            #scadenze.append(daoTestataDocumentoScadenza)
        #newDao.scadenze = scadenze
        
        newDao.persist()

        res = TestataMovimento(newDao.id)

        msg = "Nuovo movimento creato !\n\nIl nuovo movimento e' il n. " + str(res.numero) + " del " + dateToString(res.data_movimento) + " (" + newDao.operazione + ")"
        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
        response = dialog.run()
        dialog.destroy()

        self.destroy()

    def on_id_operazione_combobox_changed(self, widget, event=None):
        tipoPersonaGiuridica = self.id_operazione_combobox.get_model()[self.id_operazione_combobox.get_active()][0].tipo_persona_giuridica
        
        if self.tipoPersonaGiuridica == tipoPersonaGiuridica:
          self.personaGiuridicaCambiata = False
        else:
          self.personaGiuridicaCambiata = True
          
        if self.id_persona_giuridica_customcombobox.getType() == "fornitore" and tipoPersonaGiuridica == 'cliente':
          self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=True)
        if self.id_persona_giuridica_customcombobox.getType() == "cliente" and tipoPersonaGiuridica == 'fornitore':
          self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=True)
        
        self.persona_label.set_text(tipoPersonaGiuridica.capitalize())
        self.id_persona_giuridica_customcombobox.setType(tipoPersonaGiuridica)
        
        
    def on_id_operazione_combobox_changed(self, widget, event=None):
        tipoPersonaGiuridica = self.id_operazione_combobox.get_model()[self.id_operazione_combobox.get_active()][0].tipo_persona_giuridica
        if tipoPersonaGiuridica is not None:
          self.id_persona_giuridica_customcombobox.set_sensitive(True)
          self.persona_giuridica_sensitive = True
          if self.tipoPersonaGiuridica == tipoPersonaGiuridica:
            self.personaGiuridicaCambiata = False 
          else:
            self.personaGiuridicaCambiata = True
            
          if self.id_persona_giuridica_customcombobox.getType() == "fornitore" and tipoPersonaGiuridica == 'cliente':
            self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=True)
          if self.id_persona_giuridica_customcombobox.getType() == "cliente" and tipoPersonaGiuridica == 'fornitore':
            self.id_persona_giuridica_customcombobox.refresh(clear=True, filter=True)
          
          self.persona_label.set_text(tipoPersonaGiuridica.capitalize())
          self.id_persona_giuridica_customcombobox.setType(tipoPersonaGiuridica)

        else:
          self.id_persona_giuridica_customcombobox.set_sensitive(False)
          self.persona_giuridica_sensitive = False
          self.personaGiuridicaCambiata = False       
        
    def on_duplicazione_documento_window_close(self, widget, event=None):
        self.destroy()
        return None
