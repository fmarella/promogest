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
from promogest.ui.utils import *
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
#from promogest.dao.Dao import Dao
#import promogest.dao.TestataDocumento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.Operazione import Operazione
from promogest.dao.InformazioniFatturazioneDocumento import InformazioniFatturazioneDocumento
from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento


class FatturazioneDifferita(GladeWidget):

    def __init__(self, selection=None):
        GladeWidget.__init__(self, 'fatturazione_differita_window',
                                         'fatturazione_differita.glade')
        if selection is None:
            print """Errore. Nessuna selezione su cui fare la fatturazione
                    Complimenti, hai trovato un bug !"""
            return
        self.listdoc = self.findDoc(selection)
        self.nomi  = self.getNames(self.listdoc)
        self.draw()
        self.listdoc = self.sortDoc(self.nomi, self.listdoc)

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

    def daoGiaPresente(self, dao):
        if dao!=[]:
            daoFattura = TestataDocumento().getRecord(id=dao[0].id_fattura)
            daoDdt = TestataDocumento().getRecord(id=dao[0].id_ddt)
            msg = "Il documento N." + str(daoDdt.numero) +" e' gia' stato elaborato nel documento " + str(daoFattura.numero) + "\nPertanto non verra' elaborato in questa sessione"
            messageInfo(msg)
            return False
        else:
            return True

    def newSingleDoc(self, data, operazione, note, daoDocumento, newDao = None):
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
        if posso("PA"):
            newDao.totale_pagato = daoDocumento.totale_pagato
            newDao.totale_sospeso = daoDocumento.totale_sospeso
            newDao.documento_saldato = daoDocumento.documento_saldato
            newDao.id_primo_riferimento = daoDocumento.id_primo_riferimento
            newDao.id_secondo_riferimento = daoDocumento.id_secondo_riferimento

        newDao.ripartire_importo = daoDocumento.ripartire_importo
        newDao.costo_da_ripartire = daoDocumento.costo_da_ripartire
        return newDao

    def on_confirm_button_clicked(self, button=None):
        """ COSA CAVOLO DOBBIAMO FARE QUI ....porca miseria ... commentare..."""
        #Verifichiamo che ci sia una data documento
        if self.data_documento_entry.get_text() == '':
            obligatoryField(self.getTopLevel(), self.data_documento_entry)

        #verifichiamo che ci sia un tipo documento
        operazione = findIdFromCombobox(self.id_operazione_combobox)
        if operazione is None:
            obligatoryField(self.getTopLevel(), self.id_operazione_combobox)

        fattura = None
        for ragsoc in self.nomi:  # in self.nomi ci sono le ragioni sociali dei clienti
            # self.listdoc contiene un dizionario che ha come chiave il cliente
            #e come valore una lista di gtkTreeiter a lui riferiti
            for ddt in self.listdoc[ragsoc]:
                if self.daoGiaPresente(InformazioniFatturazioneDocumento()\
                                                    .select(id_fattura=ddt[0].id)) and \
                    operazione in ["Fattura vendita","Fattura differita vendita"]:
                    #ok il ddt non è già presente in nessuna fatturato
                    # usiamo i suoi dati per fare una fattura
                    fattura = self.newSingleDoc(self.data_documento_entry.get_text(),
                                            operazione,
                                            "",
                                            ddt[0])
            if fattura:
                righe = []
                ddt_id = []
                for ddt in self.listdoc[ragsoc]:
                    if self.daoGiaPresente(InformazioniFatturazioneDocumento()\
                                                        .select(id_ddt=ddt[0].id)):
                        # Ok, ora posso registrare le righe dei documenti
                        dao_da_fatturare = ddt[0]
                        # Inserisco il riferimento:
                        riga_riferimento = "Rif. " + str(dao_da_fatturare.operazione) + " n. " + str(
                                            dao_da_fatturare.numero) + " del " + dateToString(
                                            dao_da_fatturare.data_documento )
                        if self.data_consegna_check.get_active() and  dao_da_fatturare.inizio_trasporto:
                             riga_riferimento = riga_riferimento + "\nIn.Tr. il "+ dateToString(
                                            dao_da_fatturare.inizio_trasporto)
                        if self.note_check.get_active() and dao_da_fatturare.note_pie_pagina != "":
                            riga_riferimento = riga_riferimento+ "\n"+ dao_da_fatturare.note_pie_pagina
                        if self.no_row_check.get_active():
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
                    fattura.righeDocumento = righe
                    if not fattura.numero:
                        valori = numeroRegistroGet(tipo=operazione,
                                date=self.data_documento_entry.get_text())
                        fattura.numero = valori[0]
                        fattura.registro_numerazione= valori[1]
                    fattura.persist()
                    for d in ddt_id:
                        info = InformazioniFatturazioneDocumento()
                        info.id_fattura = fattura.id
                        info.id_ddt = d
                        info.persist()
                else:
                    messageInfo(msg= "NON CI SONO RIGHE NON CREO NIENTE")
        if fattura:
            msg = "Nuovi documenti creati !\n\n"
            messageInfo(msg)
            self.getTopLevel().destroy()
        else:
            self.getTopLevel().destroy()
            msg = "Non è stato creato alcun documento in quanto non sono state trovate righe da inserire.\n\n)"
            messageInfo(msg)
            return


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
        newmodel.reverse()
        return newmodel


    def getNames(self,lista):
        """
        Restituisce la lista dei nomi dei clienti.
        """
        nomi = []
        for i in lista:
            if i[4] not in nomi:
                nomi.append(i[4])
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
