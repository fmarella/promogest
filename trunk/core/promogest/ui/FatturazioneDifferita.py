# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

from promogest.ui.gtk_compat import *
from promogest.lib.utils import *
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.Operazione import Operazione
from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento
from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.DaoUtils import numeroRegistroGet


def findDoc(selection):
    """
    Restituisce solo i DDT vendita da una selezione
    scremando gli altri.
    """
    newmodel = []
    (model, iterator) = selection.get_selected_rows()
    for i in iterator:
        if model[i][3] == "DDT vendita":
            newmodel.append(model[i])
    newmodel.reverse()
    return newmodel


def getNames(lista):
    """
    Restituisce la lista dei nomi dei clienti.
    """
    nomi = []
    for i in lista:
        if i[4] not in nomi:
            nomi.append(i[4])
    return nomi

def sortDoc(nomi, lista):
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

def daoGiaPresente(dao):
    if dao!=[]:
        daoFattura = TestataDocumento().getRecord(id=dao[0].id_fattura)
        daoDdt = TestataDocumento().getRecord(id=dao[0].id_ddt)
        return (True, "Il documento N." + str(daoDdt.numero) +" e' gia' stato elaborato nel documento " + str(daoFattura.numero) + "\n")
    else:
        return (False, '')

def newSingleDoc(data, operazione, note, daoDocumento, newDao=None):
    """
    Make a new document from existing one
    """
    if newDao is None:
        newDao = TestataDocumento()
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
        daoSconto = ScontoTestataDocumento()
        daoSconto.valore = s.valore
        daoSconto.tipo_sconto = s.tipo_sconto
        sconti.append(daoSconto)
    newDao.scontiSuTotale = sconti

    newDao.totale_pagato = daoDocumento.totale_pagato
    newDao.totale_sospeso = daoDocumento.totale_sospeso
    newDao.documento_saldato = daoDocumento.documento_saldato
    newDao.id_primo_riferimento = daoDocumento.id_primo_riferimento
    newDao.id_secondo_riferimento = daoDocumento.id_secondo_riferimento

    newDao.ripartire_importo = daoDocumento.ripartire_importo
    newDao.costo_da_ripartire = daoDocumento.costo_da_ripartire
    return newDao

def do_fatt_diff(lista_documenti, data_documento, operazione, no_rif_righe_cumul=False, note=False, data_consegna=False, no_row=False):
    fattura = None
    logfattdiff = ''
    nomi = getNames(lista_documenti)
    lista_documenti = sortDoc(nomi, lista_documenti)
    for ragsoc in nomi:
        # in nomi ci sono le ragioni sociali dei clienti
        # self.listdoc contiene un dizionario che ha come chiave il cliente
        #e come valore una lista di gtkTreeiter a lui riferiti
        for ddt in lista_documenti[ragsoc]:
            esiste, msg = daoGiaPresente(InformazioniFatturazioneDocumento()\
                                                .select(id_fattura=ddt[0].id))

            if esiste and operazione in ["Fattura vendita","Fattura differita vendita"]:
                logfattdiff += msg
            else:
                #ok il ddt non è già presente in nessuna fatturato
                # usiamo i suoi dati per fare una fattura
                fattura = newSingleDoc(data_documento, operazione, "", ddt[0])
        if fattura:
            righe = []
            ddt_id = []
            for ddt in lista_documenti[ragsoc]:
                esiste, msg = daoGiaPresente(InformazioniFatturazioneDocumento()\
                                                    .select(id_ddt=ddt[0].id))
                if esiste:
                    logfattdiff += msg
                else:
                    # Ok, ora posso registrare le righe dei documenti
                    dao_da_fatturare = ddt[0]
                    # Inserisco il riferimento:
                    if no_rif_righe_cumul:
                        righe += dao_da_fatturare.righe[:]
                    else:
                        riga_riferimento = "Rif. " + str(dao_da_fatturare.operazione) + " n. " + str(
                                            dao_da_fatturare.numero) + " del " + dateToString(
                                            dao_da_fatturare.data_documento )
                        if data_consegna and dao_da_fatturare.inizio_trasporto:
                             riga_riferimento = riga_riferimento + "\nIn.Tr. il "+ dateToString(
                                            dao_da_fatturare.inizio_trasporto)
                        if note and dao_da_fatturare.note_pie_pagina != "":
                            riga_riferimento = riga_riferimento + "\n" + dao_da_fatturare.note_pie_pagina
                        if no_row:
                            daoRiga = RigaDocumento()
                            daoRiga.descrizione = riga_riferimento
                            daoRiga.quantita = 0.0
                            daoRiga.valore_unitario_lordo = 0.0
                            daoRiga.percentuale_iva = 0.0
                            daoRiga.moltiplicatore = 0.0
                            daoRiga.valore_unitario_netto = 0.0
                            daoRiga.scontiRigaDocumento = []
                            righe.append(daoRiga)

                            for r in dao_da_fatturare.righe:
                                daoRiga = RigaDocumento()
                                daoRiga.id_articolo = r.id_articolo
                                daoRiga.id_magazzino = r.id_magazzino
                                daoRiga.descrizione = ".    "+ r.descrizione
                                daoRiga.id_listino = r.id_listino
                                daoRiga.id_iva = r.id_iva
                                daoRiga.percentuale_iva = r.percentuale_iva
                                daoRiga.applicazione_sconti = r.applicazione_sconti
                                daoRiga.quantita = r.quantita
                                daoRiga.id_multiplo = r.id_multiplo
                                daoRiga.moltiplicatore = r.moltiplicatore
                                daoRiga.valore_unitario_lordo = r.valore_unitario_lordo
                                daoRiga.valore_unitario_netto = r.valore_unitario_netto
#                                daoRiga.misura_pezzo = r.misura_pezzo
                                sconti = []
                                for s in r.sconti:
                                    daoSconto = ScontoRigaDocumento()
                                    daoSconto.valore = s.valore
                                    daoSconto.tipo_sconto = s.tipo_sconto
                                    sconti.append(daoSconto)
                                daoRiga.scontiRigaDocumento = sconti
                                righe.append(daoRiga)
                        else:
                            #percentuale_iva = (dao_da_fatturare._totaleScontato - dao_da_fatturare._totaleImponibileScontato) *100 / dao_da_fatturare._totaleScontato
                            dao_da_fatturare.totali
                            daoRiga = RigaDocumento()
                            daoRiga.descrizione = riga_riferimento
                            daoRiga.quantita = 0
                            daoRiga.valore_unitario_lordo = 0
                            daoRiga.percentuale_iva = 0
                            daoRiga.moltiplicatore = 0
                            daoRiga.valore_unitario_netto = 0
                            daoRiga.scontiRigaDocumento = []
                            righe.append(daoRiga)
                            for t in dao_da_fatturare._castellettoIva:
                                daoRiga = RigaDocumento()
                                daoRiga.descrizione = ".       Articoli con aliquota IVA: "+str(mN(t["percentuale"],1))+"%"
                                daoRiga.quantita = 1
                                daoRiga.valore_unitario_lordo = t["totale"]
                                daoRiga.percentuale_iva = t["percentuale"]
                                daoRiga.moltiplicatore = 0
                                daoRiga.valore_unitario_netto = t["imponibile"]
                                daoRiga.scontiRigaDocumento = []
                                righe.append(daoRiga)
                        ddt_id.append(dao_da_fatturare.id)
            if righe:
                if no_rif_righe_cumul:
                    righeDict = {}
                    rrighe = []
                    for r in righe:
                        if r.id_articolo:
                            if r.id_articolo in righeDict:
                                a = righeDict[r.id_articolo]
                                a.append(r)
                                righeDict[r.id_articolo] = a
                            else:
                                righeDict[r.id_articolo] = [r]
                        else:
                            rrighe.append(r)
                    #print "OKOKOK", righeDict, rrighe
                    righe = []
                    for r in rrighe:
                        daoRiga = RigaDocumento()
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
#                                daoRiga.misura_pezzo = r.misura_pezzo
                        sconti = []
                        for s in r.sconti:
                            daoSconto = ScontoRigaDocumento()
                            daoSconto.valore = s.valore
                            daoSconto.tipo_sconto = s.tipo_sconto
                            sconti.append(daoSconto)
                        daoRiga.scontiRigaDocumento = sconti
                        righe.insert(0, daoRiga)
                    for k,v in righeDict.iteritems():
                        if len(v) ==1:
                            r = v[0]
                            daoRiga = RigaDocumento()
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
#                                daoRiga.misura_pezzo = r.misura_pezzo
                            sconti = []
                            for s in r.sconti:
                                daoSconto = ScontoRigaDocumento()
                                daoSconto.valore = s.valore
                                daoSconto.tipo_sconto = s.tipo_sconto
                                sconti.append(daoSconto)
                            daoRiga.scontiRigaDocumento = sconti
                            righe.insert(0, daoRiga)
                        else:
                            # Questa è la situazione di più righe da accorpare
                            quantita = 0
                            vul = 0
                            vun = 0
                            for a in v:
                                if a.sconti:
                                    daoRiga = RigaDocumento()
                                    daoRiga.id_articolo = a.id_articolo
                                    daoRiga.id_magazzino = a.id_magazzino
                                    daoRiga.descrizione = a.descrizione
                                    daoRiga.id_listino = a.id_listino
                                    daoRiga.percentuale_iva = a.percentuale_iva
                                    daoRiga.applicazione_sconti = a.applicazione_sconti
                                    daoRiga.quantita = a.quantita
                                    daoRiga.id_multiplo = a.id_multiplo
                                    daoRiga.moltiplicatore = a.moltiplicatore
                                    daoRiga.valore_unitario_lordo = a.valore_unitario_lordo
                                    daoRiga.valore_unitario_netto = a.valore_unitario_netto
    #                                daoRiga.misura_pezzo = r.misura_pezzo
                                    sconti = []
                                    for s in a.sconti:
                                        daoSconto = ScontoRigaDocumento()
                                        daoSconto.valore = s.valore
                                        daoSconto.tipo_sconto = s.tipo_sconto
                                        sconti.append(daoSconto)
                                    daoRiga.scontiRigaDocumento = sconti
                                    righe.insert(0, daoRiga)
                                    continue
                                else:
                                    quantita += a.quantita
                                    #vul = a.valore_unitario_lordo
                                    #vun = a.valore_unitario_netto
                            daoRiga = RigaDocumento()
                            daoRiga.id_articolo = a.id_articolo
                            daoRiga.id_magazzino = a.id_magazzino
                            daoRiga.descrizione = a.descrizione
                            daoRiga.id_listino = a.id_listino
                            daoRiga.percentuale_iva = a.percentuale_iva
                            daoRiga.applicazione_sconti = a.applicazione_sconti
                            daoRiga.quantita = quantita
                            daoRiga.id_multiplo = a.id_multiplo
                            daoRiga.moltiplicatore = a.moltiplicatore
                            daoRiga.valore_unitario_lordo = a.valore_unitario_lordo
                            daoRiga.valore_unitario_netto = a.valore_unitario_netto
#                                daoRiga.misura_pezzo = r.misura_pezzo
                            sconti = []
                            for s in a.sconti:
                                daoSconto = ScontoRigaDocumento()
                                daoSconto.valore = s.valore
                                daoSconto.tipo_sconto = s.tipo_sconto
                                sconti.append(daoSconto)
                            daoRiga.scontiRigaDocumento = sconti
                            righe.insert(0, daoRiga)
                    #return
                fattura.righeDocumento = righe
                if not fattura.numero:
                    valori = numeroRegistroGet(tipo=operazione,
                            date=stringToDate(data_documento))
                    fattura.numero = valori[0]
                    fattura.registro_numerazione= valori[1]
                fattura.persist()

                # calcolo i totali, quindi assegno come importo
                # dell'unica scadenza, l'importo del documento
                fattura.totali
                if posso('PA'):
                    scad = fattura.scadenze
                    if scad:
                        scad[0].importo = fattura._totaleScontato

                for d in ddt_id:
                    info = InformazioniFatturazioneDocumento()
                    info.id_fattura = fattura.id
                    info.id_ddt = d
                    info.persist()
            else:
                messageInfo(msg= "NON CI SONO RIGHE NON CREO NIENTE")
    if logfattdiff:
        messageInfo('I seguenti documenti non sono stati elaborati:\n' + logfattdiff)
    if fattura:
        messageInfo("Nuovo documento creato!")
    else:
        messageInfo("Non è stato creato alcun documento in quanto non sono state trovate righe da inserire.")

class FatturazioneDifferita(GladeWidget):

    def __init__(self, selection=None):
        GladeWidget.__init__(self, root='fatturazione_differita_window',
                                        path='fatturazione_differita.glade')
        if selection is None:
            return
        self.listdoc = findDoc(selection)
        self.draw()

    def draw(self):
        #queryString = ("SELECT * FROM promogest.operazione " +
        #"WHERE (tipo_operazione = 'documento') AND " +
        #"tipo_persona_giuridica = 'cliente' AND segno IS NULL")
        #argList = []
        #Environment.connection._cursor.execute(queryString, argList)
        #res = Environment.connection._cursor.fetchall()
        res = Operazione().select(tipoOperazione = 'documento',
                                    tipoPersonaGiuridica = 'cliente',
                                    segno=None)
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

    def on_confirm_button_clicked(self, button=None):
        # Verifichiamo che ci sia una data documento
        if self.data_documento_entry.get_text() == '':
            obligatoryField(self.getTopLevel(), self.data_documento_entry)
        data_documento = self.data_documento_entry.get_text()

        # Verifichiamo che ci sia un tipo documento
        operazione = findIdFromCombobox(self.id_operazione_combobox)
        if operazione is None:
            obligatoryField(self.getTopLevel(), self.id_operazione_combobox)

        # Opzioni di creazione fattura
        no_rif_righe_cumul = self.no_rif_righe_cumul_check.get_active()
        note = self.note_check.get_active()
        data_consegna = self.data_consegna_check.get_active()
        no_row = self.no_row_check.get_active()

        do_fatt_diff(self.listdoc, data_documento, operazione, no_rif_righe_cumul, note, data_consegna, no_row)
        self.getTopLevel().destroy()
