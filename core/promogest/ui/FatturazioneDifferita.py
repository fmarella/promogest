# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
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
#!/usr/local/bin/python
# coding: UTF-8

import gobject, gtk
from utils import *

from GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.TestataDocumento
from promogest.dao.TestataDocumento import TestataDocumento


def newSingleDoc(data, operazione, note, daoDocumento, newDao = None):
    """
    Make a new document from existing one
    """
    import promogest.dao.InformazioniFatturazioneDocumento
    from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento

    import promogest.dao.ScontoRigaDocumento
    from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
    import promogest.dao.ScontoTestataDocumento
    from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento

    fattura = False

    if operazione == "Fattura vendita" or operazione == "Fattura differita vendita":
        fattura = True
        fatturato = controllaInfoFatturazione(daoDocumento.id)
        if fatturato != True:
            daoFattura = TestataDocumento(Environment.connection, fatturato[0].id_fattura)
            daoDdt = TestataDocumento(Environment.connection, fatturato[0].id_ddt)
            msg = "Il documento " + str(daoDdt.numero) + msg + " e' gia' stato elaborato nel documento " + str(daoFattura.numero) + "\nPertanto non verra' elaborato in questa sessione"
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                      gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            response = dialog.run()
            dialog.destroy()
            return None

    if newDao is None:
        newDao = TestataDocumento(Environment.connection)
    newDao.data_documento = stringToDate(data)
    newDao.operazione = operazione
    newDao.id_cliente = daoDocumento.id_cliente
    newDao.id_fornitore = daoDocumento.id_fornitore
    newDao.id_destinazione_merce = daoDocumento.id_destinazione_merce
    newDao.id_pagamento = daoDocumento.id_pagamento
    newDao.id_banca = daoDocumento.id_banca
    newDao.id_aliquota_iva_esenzione = daoDocumento.id_aliquota_iva_esenzione
    newDao.protocollo = daoDocumento.protocollo
    newDao.causale_trasporto = daoDocumento.causale_trasporto
    newDao.aspetto_esteriore_beni = daoDocumento.aspetto_esteriore_beni
    newDao.inizio_trasporto = daoDocumento.inizio_trasporto
    newDao.fine_trasporto = daoDocumento.fine_trasporto
    newDao.id_vettore =daoDocumento.id_vettore
    newDao.incaricato_trasporto = daoDocumento.incaricato_trasporto
    newDao.totale_colli = daoDocumento.totale_colli
    newDao.totale_peso = daoDocumento.totale_peso
    newDao.note_interne = daoDocumento.note_interne
    newDao.note_pie_pagina = daoDocumento.note_pie_pagina  + " "  + note
    newDao.applicazione_sconti = daoDocumento.applicazione_sconti
    sconti = []
    sco = daoDocumento.sconti or []
    for s in sco:
        daoSconto = ScontoTestataDocumento(Environment.connection)
        daoSconto.valore = s.valore
        daoSconto.tipo_sconto = s.tipo_sconto
        sconti.append(daoSconto)
    newDao.sconti = sconti
    if Environment.conf.hasPagamenti == True:
        newDao.totale_pagato = daoDocumento.totale_pagato
        newDao.totale_sospeso = daoDocumento.totale_sospeso
        newDao.documento_saldato = daoDocumento.documento_saldato
        newDao.id_primo_riferimento = daoDocumento.id_primo_riferimento
        newDao.id_secondo_riferimento = daoDocumento.id_secondo_riferimento

    newDao.ripartire_importo = daoDocumento.ripartire_importo
    newDao.costo_da_ripartire = daoDocumento.costo_da_ripartire

    return newDao

def registraInfoFatturazione(idFattura, idDdt):
    """
    Registra le informazioni relative alla fatturazione di un documento
    """
    import promogest.dao.InformazioniFatturazioneDocumento
    from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento

    info = InformazioniFatturazioneDocumento(Environment.connection)
    info.id_fattura = idFattura
    info.id_ddt = idDdt
    info.persist(Environment.connection)

def controllaInfoFatturazione(idDocumento):
    import promogest.dao.InformazioniFatturazioneDocumento
    from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento

    res = promogest.dao.InformazioniFatturazioneDocumento.select(
        Environment.connection, None, idDocumento, immediate=True)
    if res != []:
        return res
    return True

def registraRigheDocumento(riferimento, rig, newDao, vecchierighe):
    import promogest.dao.RigaDocumento
    from promogest.dao.RigaDocumento import RigaDocumento
    from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento

    righe = []
    for i in vecchierighe:
        daoRiga = RigaDocumento(Environment.connection)
        daoRiga.id_testata_documento = newDao.id
        daoRiga.id_articolo = i.id_articolo
        daoRiga.id_magazzino = i.id_magazzino
        daoRiga.descrizione = i.descrizione
        daoRiga.id_listino = i.id_listino
        daoRiga.percentuale_iva = i.percentuale_iva
        daoRiga.applicazione_sconti = i.applicazione_sconti
        daoRiga.quantita = i.quantita
        daoRiga.id_multiplo = i.id_multiplo
        daoRiga.moltiplicatore = i.moltiplicatore
        daoRiga.valore_unitario_lordo = i.valore_unitario_lordo
        daoRiga.valore_unitario_netto = i.valore_unitario_netto
        daoRiga.misura_pezzo = i.misura_pezzo
        sconti = []
        sco = i.sconti
        for s in sco:
            daoSconto = ScontoRigaDocumento(Environment.connection)
            daoSconto.valore = s.valore
            daoSconto.tipo_sconto = s.tipo_sconto
            sconti.append(daoSconto)
        daoRiga.sconti = sconti
        righe.append(daoRiga)

    daoRiga = RigaDocumento(Environment.connection)
    daoRiga.id_testata_documento = newDao.id
    daoRiga.descrizione = riferimento
    daoRiga.quantita = 0.0
    daoRiga.valore_unitario_lordo = 0.0
    daoRiga.percentuale_iva = 0.0
    daoRiga.moltiplicatore = 0.0
    daoRiga.valore_unitario_netto = 0.0
    righe.append(daoRiga)

    for r in rig:
        daoRiga = RigaDocumento(Environment.connection)
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
            daoSconto = ScontoRigaDocumento(Environment.connection)
            daoSconto.valore = s.valore
            daoSconto.tipo_sconto = s.tipo_sconto
            sconti.append(daoSconto)
        daoRiga.sconti = sconti
        righe.append(daoRiga)
    return righe

class FatturazioneDifferita(GladeWidget):

    def __init__(self, selection=None):
        GladeWidget.__init__(self, 'fatturazione_differita_window', 'fatturazione_differita.glade')
        if selection is None:
            print """Errore. Nessuna selezione su cui fare la fatturazione
                    Complimenti, hai trovato un bug !"""
            return
        self.listdoc = self.findDoc(selection)
        self.nomi  = self.getNames(self.listdoc)
        
        self.draw()
        self.listdoc = self.sortDoc(self.nomi, self.listdoc)

    def draw(self):
        queryString = ("SELECT * FROM promogest.operazione " +
        "WHERE (tipo_operazione = 'documento') AND " +
        "tipo_persona_giuridica = 'cliente' AND segno IS NULL")
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
        self.data_documento_entry.set_text(dateToString(datetime.datetime.today()))
        self.data_documento_entry.grab_focus()


    def on_confirm_button_clicked(self, button=None):
        if (self.data_documento_entry.get_text() == ''):
            obligatoryField(self.getTopLevel(), self.data_documento_entry)

        operazione = findIdFromCombobox(self.id_operazione_combobox)
        if operazione is None:
            obligatoryField(self.getTopLevel(), self.id_operazione_combobox)

        # self.listdoc e': listdoc[cliente1][doc1...n] e cosi' via
        #                  listdoc[cliente2][doc1...n] e cosi' via
        # dove doc1...n sono cosi gestiti:
        # ...[cliente1][0]
        # ...[cliente1][1] e cosi' via.. ( che sono le gtkTreeRow che contengono i documenti;
        # ogni gtkTreeRow e' composta da TestataDocumento + i campi che ci sono nel
        # filter ( numero, data...ecc)
        fattura = None
        for i in range(0, len(self.nomi)):
            # self.nomi[i] contiene il cliente di cui voglio fatturare
            # attualmente.. tutto va fatto in questo for
            ok = False
            k = 0

            while(ok!=True and k < len(self.listdoc[self.nomi[i]]) ):
                fattura = newSingleDoc(
                    self.data_documento_entry.get_text(), operazione, "",
                    self.listdoc[self.nomi[i]][k][0])
                if fattura is not None:
                    fattura.persist()
                    ok = True
                else:
                    k = k+1

            if k >= len(self.listdoc[self.nomi[i]]):
                continue

            righe = []
            for j in range(0, len(self.listdoc[self.nomi[i]])):
                # Ok, ora posso registrare le righe dei documenti

                daoDaFatt = self.listdoc[self.nomi[i]][j][0]
                # Inserisco il riferimento:
                rifer = "Rif. " + str(daoDaFatt.operazione) + " n. " + str(
                    daoDaFatt.numero) + " del " + dateToString(
                        daoDaFatt.data_documento)
                argList = []

                fatturato = controllaInfoFatturazione(daoDaFatt.id)
                if fatturato == True:
                    righe = registraRigheDocumento(
                            rifer, daoDaFatt.righe, fattura, righe)
                    registraInfoFatturazione(fattura.id, daoDaFatt.id)
                else:
                    daoFattura = TestataDocumento(Environment.connection, fatturato[0].id_fattura)
                    daoDdt = TestataDocumento(Environment.connection, fatturato[0].id_ddt)
                    msg = "Il documento " + str(daoDdt.numero)
                    msg = msg + " e' gia' stato elaborato nel documento " + str(daoFattura.numero)+' ('+str(daoFattura.operazione)+').'
                    msg = msg + "\nPertanto non verra' elaborato in questa sessione"
                    dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
                    response = dialog.run()
                    dialog.destroy()

        if len(righe) == 0:
            self.getTopLevel().destroy()
            msg = u"Non � stato creato alcun documento in quanto non sono state trovate righe da inserire.\n\n)"
            dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                      gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            response = dialog.run()
            dialog.destroy()
            
            return
        else:
            fattura.righe = righe
            fattura.persist()
        if fattura is not None:
           msg = "Nuovi documenti creati !\n\n)"
           dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                      gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
           response = dialog.run()
           dialog.destroy()

        self.getTopLevel().destroy()

    def findDoc(self, selection):
        """
        Restituisce solo i DDT vendita da una selezione
        scremando gli altri.
        """

        newmodel = []
        (model, iterator) = selection.get_selected_rows()

        for i in iterator:
            if model[i][3] == "DDT vendita":
                newmodel.append(model[i])

        return newmodel


    def getNames(self, list):
        """
        Restituisce la lista dei nomi dei clienti.
        """

        nomi = []
        print len(list), 'list'
        for i in range(0, len(list)):
            print i, 'indice'
            print list[i][4], 'list[i][4]'
            if i == 0:
                nomi.append(list[i][4])
            else:
                print nomi
                if list[i][4] in nomi:
                    continue
                else:
                    nomi.append(list[i][4])
        return nomi

    def sortDoc(self, nomi, lista):
        """
        """
        newlist = { }

        for i in range(0, len(nomi)):
            newlist[nomi[i]] = []

        for i in range(0, len(lista)):
            for j in range(0, len(nomi)):
                if (lista[i][4] == nomi[j]):
                    newlist[nomi[j]].append(lista[i])

        return newlist




