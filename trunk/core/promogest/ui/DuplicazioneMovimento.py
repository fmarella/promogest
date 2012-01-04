# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Alceste Scalas <alceste@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni <francesco@promotux.it
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

from promogest import Environment
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
from promogest.dao.Operazione import Operazione
from promogest.ui.anagDocumenti.AnagraficaDocumenti import *
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.ui.gtk_compat import *

if posso("PA"):
    import promogest.modules.Pagamenti.dao.TestataDocumentoScadenza
    from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza


class DuplicazioneMovimento(GladeWidget):

    def __init__(self, daoMovimento, anagraficaMovimenti):

        self.dao = daoMovimento
        self.anagrafica_movimenti = anagraficaMovimenti

        GladeWidget.__init__(self, 'duplicazione_movimento_window',
                                            'duplicazione_movimento.glade')
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

        listini = Listino().select(batchSize=None)
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
        if self.dao.numeroMagazzini == 1:
            fillComboboxMagazzini(self.id_magazzino_combobox)
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
#        newDao.numero = self.dao.numero
        newDao.parte = self.dao.parte
        newDao.registro_numerazione = self.dao.registro_numerazione
        newDao.operazione = findIdFromCombobox(self.id_operazione_combobox)
        newDao.note_interne = self.dao.note_interne
        newDao.note_pie_pagina = self.dao.note_pie_pagina
        newDao.id_testata_documento = self.dao.id_testata_documento
        if  self.personaGiuridicaCambiata:
            if not self.id_persona_giuridica_customcombobox.getId():
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
            daoRiga = RigaMovimento()
            daoRiga.id_testata_movimento = newDao.id
            daoRiga.id_articolo = r.id_articolo
            if self.id_magazzino_combobox.get_active() != -1:
                iddi = findIdFromCombobox(self.id_magazzino_combobox)
                daoRiga.id_magazzino = iddi
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
        newDao.persist()

#        res = TestataMovimento(newDao.id)

        msg = "Nuovo movimento creato !\n\nIl nuovo movimento e' il n. " + str(newDao.numero) + " del " + dateToString(newDao.data_movimento) + " (" + newDao.operazione + ")"
        messageInfo(msg=msg, transient=self.getTopLevel())
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
