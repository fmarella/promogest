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
import promogest.dao.TestataDocumento
from promogest.dao.TestataDocumento import TestataDocumento
import promogest.dao.RigaDocumento
from promogest.dao.RigaDocumento import RigaDocumento
import promogest.dao.ScontoRigaDocumento
from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
import promogest.dao.ScontoTestataDocumento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
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
        queryString = ("SELECT * FROM promogest.operazione " +
                       "WHERE (tipo_operazione IS NULL OR tipo_operazione = 'documento') AND " +
                       "fonte_valore = '" + operazione["fonteValore"] + "' AND " +
                       "tipo_persona_giuridica = '" + operazione["tipoPersonaGiuridica"] + "'")
        argList = []
        Environment.connection._cursor.execute(queryString, argList)
        res = Environment.connection._cursor.fetchall()
        model = gtk.ListStore(object, str, str)
        for o in res:
            model.append((o, o['denominazione'], (o['denominazione'] or '')[0:30]))

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

        newDao = TestataDocumento().getRecord()
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
        sconti = []
        sco = self.dao.sconti or []
        for s in sco:
            daoSconto = ScontoTestataDocumento().getRecord()
            daoSconto.valore = s.valore
            daoSconto.tipo_sconto = s.tipo_sconto
            sconti.append(daoSconto)
        newDao.sconti = sconti
        righe = []
        rig = self.dao.righe
        for r in rig:
            daoRiga = RigaDocumento().getRecord()
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
            daoRiga.misura_pezzo = r.misura_pezzo
            sconti = []
            sco = r.sconti
            for s in sco:
                daoSconto = ScontoRigaDocumento().getRecord()
                daoSconto.valore = s.valore
                daoSconto.tipo_sconto = s.tipo_sconto
                sconti.append(daoSconto)
            daoRiga.sconti = sconti
            righe.append(daoRiga)
        newDao.righe = righe
        scadenze = []
        if Environment.conf.hasPagamenti == True:
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

        res = TestataDocumento(Environment.connection, newDao.id)

        msg = "Nuovo documento creato !\n\nIl nuovo documento e' il n. " + str(res.numero) + " del " + dateToString(res.data_documento) + " (" + newDao.operazione + ")"
        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
        response = dialog.run()
        dialog.destroy()

        self.destroy()


    def on_duplicazione_documento_window_close(self, widget, event=None):
        self.destroy()
        return None
