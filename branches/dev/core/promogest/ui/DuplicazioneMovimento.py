# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import os
import gtk, gobject
import gtk
from GladeWidget import GladeWidget

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.TestataMovimento
from promogest.dao.TestataMovimento import TestataMovimento
import promogest.dao.RigaMovimento
from promogest.dao.RigaMovimento import RigaMovimento
import promogest.dao.ScontoRigaMovimento
from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento

from utils import *



class DuplicazioneMovimento(GladeWidget):

    def __init__(self, daoMovimento):

        self.dao = daoMovimento

        GladeWidget.__init__(self, 'duplicazione_movimento_window')
        self.placeWindow(self.getTopLevel())
        self.draw()


    def draw(self):
        # seleziona i tipi movimento compatibili
        operazione = leggiOperazione(self.dao.operazione)
        queryString = ("SELECT * FROM promogest.operazione WHERE (tipo_operazione IS NULL OR tipo_operazione = 'movimento')")
        if operazione['tipoPersonaGiuridica'] == '':
            queryString += " AND tipo_persona_giuridica IS NULL"
        else:
            queryString += " AND tipo_persona_giuridica = '" + operazione['tipoPersonaGiuridica'] + "'"


        argList = []
        Environment.connection._cursor.execute(queryString, argList)
        res = Environment.connection._cursor.fetchall()
        model = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str)
        for o in res:
            model.append((o, o['denominazione'], (o['denominazione'] or '')[0:30]))

        self.id_operazione_combobox.clear()
        renderer = gtk.CellRendererText()
        self.id_operazione_combobox.pack_start(renderer, True)
        self.id_operazione_combobox.add_attribute(renderer, 'text', 2)
        self.id_operazione_combobox.set_model(model)

        self.data_movimento_entry.set_text(dateToString(datetime.datetime.today()))
        self.data_movimento_entry.grab_focus()
        self.getTopLevel().show_all()


    def on_confirm_button_clicked(self, button=None):

        if (self.data_movimento_entry.get_text() == ''):
            obligatoryField(self.getTopLevel(), self.data_movimento_entry)

        if (findIdFromCombobox(self.id_operazione_combobox) is None):
            obligatoryField(self.getTopLevel(), self.id_operazione_combobox)

        note = "Rif. " + self.dao.operazione + " n. " + str(self.dao.numero) + " del " + dateToString(self.dao.data_movimento)

        newDao = TestataMovimento(Environment.connection)
        newDao.data_movimento = stringToDate(self.data_movimento_entry.get_text())
        newDao.numero = self.dao.numero
        newDao.parte = self.dao.parte
        newDao.registro_numerazione = self.dao.registro_numerazione
        newDao.operazione = findIdFromCombobox(self.id_operazione_combobox)
        newDao.note_interne = self.dao.note_interne
        newDao.note_pie_pagina = self.dao.note_pie_pagina
        newDao.id_testata_documento = self.dao.id_testata_documento
        newDao.id_cliente = self.dao.id_cliente
        newDao.id_fornitore = self.dao.id_fornitore
        righe = []
        rig = self.dao.righe
        for r in rig:
            daoRiga = RigaMovimento(Environment.connection)
            daoRiga.id_testata_movimento = newDao.id
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
            daoRiga.misura_pezzo = r.misura_pezzo
            sconti = []
            sco = r.sconti
            for s in sco:
                daoSconto = ScontoRigaMovimento(Environment.connection)
                daoSconto.valore = s.valore
                daoSconto.tipo_sconto = s.tipo_sconto
                sconti.append(daoSconto)
            daoRiga.sconti = sconti
            righe.append(daoRiga)

        newDao.righe = righe
        newDao.totale_pagato = self.dao.totale_pagato
        newDao.totale_sospeso = self.dao.totale_sospeso
        newDao.documento_saldato = self.dao.documento_saldato
        newDao.id_primo_riferimento = self.dao.id_primo_riferimento
        newDao.id_secondo_riferimento = self.dao.id_secondo_riferimento
        scadenze = []
        scad = self.dao.scadenze
        for s in scad:
            daoTestataDocumentoScadenza = TestataDocumentoScadenza(Environment.connection)
            daoTestataDocumentoScadenza.id_testata_documento = newDao.id
            daoTestataDocumentoScadenza.data = s.data
            daoTestataDocumentoScadenza.importo = s.importo
            daoTestataDocumentoScadenza.pagamento = s.pagamento
            daoTestataDocumentoScadenza.data_pagamento= s.data_pagamento
            daoTestataDocumentoScadenza.numero_scadenza = s.numero_scadenza
            scadenze.append(daoTestataDocumentoScadenza)
        newDao.scadenze = scadenze
        newDao.persist()

        res = TestataMovimento(Environment.connection, newDao.id)

        msg = "Nuovo movimento creato !\n\nIl nuovo movimento e' il n. " + str(res.numero) + " del " + dateToString(res.data_movimento) + " (" + newDao.operazione + ")"
        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
        response = dialog.run()
        dialog.destroy()

        self.destroy()


    def on_duplicazione_movimento_window_close(self, widget, event=None):
        self.destroy()
        return None
