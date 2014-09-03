# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
from promogest.dao.Operazione import Operazione
from promogest.dao.Fornitura import Fornitura
from promogest.dao.DaoUtils import numeroRegistroGet
from promogest.ui.anagDocumenti.AnagraficaDocumenti import *
import promogest.modules.Pagamenti.dao.TestataDocumentoScadenza
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *

import datetime
from promogest.dao.StoricoDocumento import add_relazione


class DuplicazioneDocumento(GladeWidget):

    def __init__(self, daoDocumento, anagraficaDocumenti):

        self.dao = daoDocumento
        self.anagrafica_documenti = anagraficaDocumenti
        self.personaGiuridicaCambiata = False
        GladeWidget.__init__(self, root='duplicazione_documento_window',
                                    path='duplicazione_documento.glade')
        self.placeWindow(self.getTopLevel())
        self.draw()

    def draw(self):
        # seleziona i tipi documento compatibili
        operazione = leggiOperazione(self.dao.operazione)
        self.tipoPersonaGiuridica = operazione['tipoPersonaGiuridica']
        self.persona_label.set_text(self.tipoPersonaGiuridica.capitalize())

        self.id_persona_giuridica_customcombobox.setType(self.tipoPersonaGiuridica)

        res = Environment.params['session'].query(Operazione).filter(Operazione.tipo_persona_giuridica != '').all()

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

        listini = Listino().select(batchSize=None)
        model = gtk.ListStore(object, int, str)
        model.append((None, 0, '<Invariato>'))
        model.append((None, 1, '<Azzera>'))
        model.append((None, 2, '<Prezzo d\'acquisto>'))
        indice_prezzo = 3;
        for l in listini:
            model.append((l, indice_prezzo, (l.denominazione or '')[0:30]))
            indice_prezzo += 1
        self.id_prezzo_combobox.clear()
        renderer = gtk.CellRendererText()
        self.id_prezzo_combobox.pack_start(renderer, True)
        self.id_prezzo_combobox.add_attribute(renderer, 'text', 2)
        self.id_prezzo_combobox.set_model(model)
        self.id_prezzo_combobox.set_active(0)

        #controlla che nel documento ci sia un solo magazzino
        if self.dao.numeroMagazzini == 1:
            fillComboboxMagazzini(self.id_magazzino_combobox)
        else:
            #disabilito il cambio di magazzino
            self.id_magazzino_combobox.set_sensitive(False)

        self.mantieni_pagamenti_checkbutton.set_active(True)

    def on_confirm_button_clicked(self, button=None):

        if (self.data_documento_entry.get_text() == ''):
            obligatoryField(self.getTopLevel(), self.data_documento_entry)

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            obligatoryField(self.getTopLevel(), self.id_operazione_combobox)
        if self.note_check.get_active():
            note = "Rif. " + self.dao.operazione + " n. " + str(self.dao.numero) + " del " + dateToString(self.dao.data_documento)
        else:
            note = ""

        mantieni_pagamenti = self.mantieni_pagamenti_checkbutton.get_active()
        associa_doc_padre_figlio = self.associa_doc_padre_figlio_checkbutton.get_active()

        newDao = TestataDocumento()
        newDao.data_documento = stringToDate(self.data_documento_entry.get_text())
        newDao.operazione = findIdFromCombobox(self.id_operazione_combobox)
        if self.personaGiuridicaCambiata:
            if not self.id_persona_giuridica_customcombobox.getId():
                obligatoryField(self.getTopLevel(), self.id_persona_giuridica_customcombobox)
            if self.id_persona_giuridica_customcombobox.getType() == "cliente":
                newDao.id_cliente = self.id_persona_giuridica_customcombobox.getId()
                newDao.id_fornitore = None
            else:
                newDao.id_fornitore = self.id_persona_giuridica_customcombobox.getId()
                newDao.id_cliente = None
        else:
            if not self.id_persona_giuridica_customcombobox.getId():
                newDao.id_fornitore = self.dao.id_fornitore
                newDao.id_cliente = self.dao.id_cliente
            else:
                if self.id_persona_giuridica_customcombobox.getType() == "cliente":
                    newDao.id_cliente = self.id_persona_giuridica_customcombobox.getId()
                    newDao.id_fornitore = None
                else:
                    newDao.id_fornitore = self.id_persona_giuridica_customcombobox.getId()
                    newDao.id_cliente = None

        newDao.id_destinazione_merce = self.dao.id_destinazione_merce
        newDao.id_pagamento = self.dao.id_pagamento
        newDao.id_banca = self.dao.id_banca
        newDao.numero = self.dao.numero
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

        tipoid = findIdFromCombobox(self.id_operazione_combobox)
        tipo = Operazione().getRecord(id=tipoid)
        #if not newDao.numero:
        valori = numeroRegistroGet(tipo=tipo.denominazione, date=stringToDate(self.data_documento_entry.get_text()))
        newDao.numero = valori[0]
        newDao.registro_numerazione= valori[1]


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

        #operazione = leggiOperazione(tipo)
        if tipo.segno != '' and tipo.segno is not None:
            tipoDOC = "MOV"
        else:
            tipoDOC = "DOC"

        scontiRigaMovimento =[]
        scontiRigaDocumento =[]
        for r in rig:

            if (tipoDOC == "MOV" and r.id_articolo == None) or tipoDOC == "DOC":
                daoRiga = RigaDocumento()
                sconti = []
                sco = r.sconti
                if self.mantieni_sconti_checkbutton.get_active() :
                    for s in sco:
                        daoSconto = ScontoRigaDocumento()
                        daoSconto.valore = s.valore
                        daoSconto.tipo_sconto = s.tipo_sconto
                        scontiRigaDocumento.append(daoSconto)
                daoRiga.scontiRigaDocumento = scontiRigaDocumento
                scontiRigaDocumento =[]
            else:
                daoRiga = RigaMovimento()
                sconti =[]
                sco = r.sconti
                if self.mantieni_sconti_checkbutton.get_active() :
                    for s in sco:
                        daoSconto = ScontoRigaMovimento()
                        daoSconto.valore = s.valore
                        daoSconto.tipo_sconto = s.tipo_sconto
                        scontiRigaMovimento.append(daoSconto)
                daoRiga.scontiRigheMovimento = scontiRigaMovimento
                scontiRigaMovimento =[]

            #daoRiga.id_testata_documento = newDao.id
            daoRiga.id_articolo = r.id_articolo
            if self.id_magazzino_combobox.get_active() != -1 and r.id_magazzino !=None:
                iddi = findIdFromCombobox(self.id_magazzino_combobox)
                daoRiga.id_magazzino = iddi
            else:
                daoRiga.id_magazzino = r.id_magazzino
            daoRiga.descrizione = r.descrizione
            # Copia il campo iva
            daoRiga.id_iva = r.id_iva
            #ricalcola prezzi
            indice_prezzo_combobox = self.id_prezzo_combobox.get_model()[self.id_prezzo_combobox.get_active()][1]
            if  indice_prezzo_combobox == 0:
              daoRiga.id_listino = r.id_listino
              daoRiga.valore_unitario_lordo = r.valore_unitario_lordo or 0
              daoRiga.valore_unitario_netto = r.valore_unitario_netto or 0
            elif indice_prezzo_combobox == 1:
              daoRiga.id_listino = r.id_listino
              daoRiga.valore_unitario_lordo = 0
              daoRiga.valore_unitario_netto = 0
            elif indice_prezzo_combobox == 2:
              fornitura = Environment.params['session'].query(Fornitura).filter(Fornitura.id_articolo == r.id_articolo).order_by(Fornitura.data_prezzo.asc()).all()
              if fornitura:
                fornitura = fornitura[0]
                daoRiga.valore_unitario_lordo = fornitura.prezzo_lordo
                daoRiga.valore_unitario_netto = fornitura.prezzo_netto
              daoRiga.id_listino = r.id_listino

            else:
              #ricalcola prezzi
              listino = self.id_prezzo_combobox.get_model()[indice_prezzo_combobox][0]
              listinoArticolo = Environment.params['session'].query(ListinoArticolo).filter(ListinoArticolo.id_listino == listino.id and r.id_articolo == ListinoArticolo.id_articolo).all()
              if len(listinoArticolo) > 0:
                daoRiga.id_listino = listinoArticolo[0].id_listino
                daoRiga.valore_unitario_lordo = listinoArticolo[0].prezzo_dettaglio
                daoRiga.valore_unitario_netto = listinoArticolo[0].prezzo_ingrosso
              else:
                daoRiga.id_listino = r.id_listino
                daoRiga.valore_unitario_lordo = r.valore_unitario_lordo
                daoRiga.valore_unitario_netto = r.valore_unitario_netto

            daoRiga.percentuale_iva = r.percentuale_iva
            daoRiga.applicazione_sconti = r.applicazione_sconti
            daoRiga.quantita = r.quantita
            daoRiga.id_multiplo = r.id_multiplo
            daoRiga.moltiplicatore = r.moltiplicatore
            if posso("SM"):
                from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
                #try:
                daoMisuraPezzo = MisuraPezzo()
                if r.misura_pezzo:
                    daoMisuraPezzo.altezza = r.misura_pezzo[0].altezza
                    daoMisuraPezzo.larghezza = r.misura_pezzo[0].larghezza
                    daoMisuraPezzo.moltiplicatore = r.misura_pezzo[0].moltiplicatore
                else:
                    daoMisuraPezzo.altezza = 0
                    daoMisuraPezzo.larghezza = 0
                    daoMisuraPezzo.moltiplicatore = 0
                daoRiga.misura_pezzo = [daoMisuraPezzo]
                #except :
                    #pass

            righeDocumento.append(daoRiga)
        #return
        newDao.righeDocumento = righeDocumento
        scadenze = []

        if mantieni_pagamenti:
            scad = self.dao.scadenze
            for s in scad:
                daoTestataDocumentoScadenza = TestataDocumentoScadenza()
                daoTestataDocumentoScadenza.id_testata_documento = newDao.id
                daoTestataDocumentoScadenza.data = s.data
                daoTestataDocumentoScadenza.importo = s.importo
                daoTestataDocumentoScadenza.pagamento = s.pagamento
                daoTestataDocumentoScadenza.id_banca = s.id_banca
                daoTestataDocumentoScadenza.data_pagamento= s.data_pagamento
                daoTestataDocumentoScadenza.note_per_primanota = s.note_per_primanota
                daoTestataDocumentoScadenza.numero_scadenza = s.numero_scadenza
                scadenze.append(daoTestataDocumentoScadenza)
            newDao.scadenze = scadenze
            newDao.totale_pagato = 0
            newDao.totale_sospeso = 0
            newDao.documento_saldato = False
            #newDao.id_primo_riferimento = self.dao.id_primo_riferimento
            #newDao.id_secondo_riferimento = self.dao.id_secondo_riferimento
        else:
            newDao.totale_pagato = Decimal(0)
            newDao.totale_sospeso = self.dao._totaleScontato
            newDao.documento_saldato = False

        newDao.persist()

        if associa_doc_padre_figlio:
            add_relazione(self.dao.id, newDao.id)

        if posso("GN"):
            if self.dao.data_inizio_noleggio or self.dao.data_fine_noleggio:

                from promogest.modules.GestioneNoleggio.dao.TestataGestioneNoleggio import TestataGestioneNoleggio
                newTestataGestioneNoleggio = TestataGestioneNoleggio()
                newTestataGestioneNoleggio.data_inizio_noleggio = self.dao.data_inizio_noleggio
                newTestataGestioneNoleggio.data_fine_noleggio = self.dao.data_fine_noleggio
                newTestataGestioneNoleggio.id_testata_documento = newDao.id
                newTestataGestioneNoleggio.persist()

        #se il segno dell'operazione non è cambiato duplico il documento, altrimenti duplico ma apro la finestra di new/modifica documento

        msg = "Nuovo documento creato !\n\nIl nuovo documento e' il n. " + str(newDao.numero) + " del " + dateToString(newDao.data_documento) + " (" + newDao.operazione + ")\n" + "Lo vuoi modificare?"
        if YesNoDialog(msg=msg, transient=self.getTopLevel()):
          self.anagrafica_documenti.editElement.setVisible(True)
          self.anagrafica_documenti.editElement.setDao(newDao)
          self.anagrafica_documenti.editElement.id_persona_giuridica_customcombobox.set_sensitive(True)
          self.anagrafica_documenti.editElement.setFocus()

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

    def on_duplicazione_documento_window_close(self, widget, event=None):
        self.destroy()
        return None
