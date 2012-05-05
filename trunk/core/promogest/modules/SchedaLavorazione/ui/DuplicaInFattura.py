# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Dr astico  (Marco Pinna)<marco@promotux.it>
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

from promogest.Environment import *
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.DestinazioneMerce import DestinazioneMerce
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento


class DuplicaInFattura(object):

    def __init__(self, dao=None, ui=None):
        self.dao = dao
        self.ui = ui


    def checkField(self, tipo="fattura", operazione=None):
        if tipo =="fattura" and not self.dao.id_cliente:
            obligatoryField(None, msg='scegliere prima un cliente da associare al documento')
            return
        else:
            if self.dao.id is None:
                msg = "Prima di poter generare la fattura di questa scheda e' necessario salvarla .\n Salvare ?"
                response = self.advertise(msg)
                if tipo=="fattura" and response == GTK_RESPONSE_YES:
                    if not self.dao.fattura:
                        self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, -10)
                        idFattura = self.creaFatturaDaScheda()
                        self.dao.ricevuta_associata = TestataDocumento().getRecord(id=idFattura).numero
                        self.ui.n_documento_entry.set_text(str(self.dao.ricevuta_associata))
                        self.dao.fattura = True
                        self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, -10)
                        self.ui._refresh()
                    else:
                        if self.dao.ricevuta_associata is not None:
                            ricevuta_num = self.dao.ricevuta_associata
                            self.advertise("La presente scheda ha gia' generato una fattura (numero "+ricevuta_num+").")
                    return
                elif tipo=="movimento" and response == GTK_RESPONSE_YES:
                    if not self.dao.fattura:
                        self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, -10)
                        idMovimento = self.creaMovimentoDaScheda(operazione=operazione)
                        self.dao.ricevuta_associata = TestataMovimento().getRecord(id=idMovimento).numero
                        self.ui.n_documento_entry.set_text(str(self.dao.ricevuta_associata))
                        self.dao.fattura = True
                        self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, -10)
                        self.ui._refresh()
                    else:
                        #TODO: check this part
                        if self.dao.ricevuta_associata is not None:
                            ricevuta_num = self.dao.ricevuta_associata
                            self.advertise("La presente scheda ha gia' generato una fattura (numero "+ricevuta_num+").")
                else:
                    return
            else:
                if tipo=="fattura" and not self.dao.fattura:
                    self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, -10)
                    idFattura = self.creaFatturaDaScheda()
                    self.dao.ricevuta_associata = TestataDocumento().getRecord(id=idFattura).numero
                    self.ui.n_documento_entry.set_text(str(self.dao.ricevuta_associata))
                    self.dao.fattura = True
                    self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, -10)
                    self.ui._refresh()
                    return
                elif tipo=="movimento":
                    if not self.dao.fattura:
                        self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, -10)
                        idMovimento = self.creaMovimentoDaScheda(operazione=operazione)
                        self.dao.ricevuta_associata = TestataMovimento().getRecord(id=idMovimento).numero
                        self.ui.n_documento_entry.set_text(str(self.dao.ricevuta_associata))
                        self.dao.fattura = True
                        self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, -10)
                        self.ui._refresh()
                    else:
                        #TODO: check this part
                        if self.dao.ricevuta_associata is not None:
                            ricevuta_num = self.dao.ricevuta_associata
                            self.advertise("La presente scheda ha gia' generato una fattura (numero "+ricevuta_num+").")
                else:
                    if self.dao.ricevuta_associata is not None:
                        ricevuta_num = self.dao.ricevuta_associata
                        msg = "La presente scheda ha gia' generato una fattura (numero "+ricevuta_num+")."
                    else:
                        msg = "La presente scheda ha gia' generato una fattura,\nma non è possibile stabilire il numero del documento."
                    self.advertise(msg)
                    return

    def creaMovimentoDaScheda(self, operazione=None):
        daoTestataMovimento = TestataMovimento()
        daoTestataMovimento.data_documento = datetime.datetime.today()
        if self.dao.id_magazzino is None:
            obligatoryField(None, msg='Selezionare un magazzino per generare il movimento.')
        daoTestataMovimento.note_interne = 'Movimento associato a scheda lavorazione numero '+str(self.dao.numero)
        daoTestataMovimento.note_pie_pagina = None
        daoTestataMovimento.registro_numerazione = 'registro_movimenti'
        daoTestataMovimento.operazione = operazione

        righe_testata = []

        for riga in self.dao.righe:
            riga_testata = RigaMovimento()
            riga_testata.id_articolo = riga.id_articolo
            riga_testata.id_magazzino = riga.id_magazzino
            riga_testata.descrizione = riga.descrizione
            riga_testata.id_listino = riga.id_listino
            riga_testata.percentuale_iva = riga.percentuale_iva
            riga_testata.applicazione_sconti = riga.applicazione_sconti
            riga_testata.quantita = riga.quantita
            riga_testata.id_multiplo = riga.id_multiplo
            riga_testata.moltiplicatore = riga.moltiplicatore
            if riga.scontiRiga:
                for sconto in riga.scontiRiga:
                    self.ui.setScontiRiga(riga_testata, 'movimento')
            try:
                riga_testata.scontiRigheMovimento = riga_testata.scontiRiga
            except:
                riga_testata.scontiRigheMovimento = []

            riga_testata.valore_unitario_lordo = calcolaPrezzoIva(riga.valore_unitario_lordo, (-1*riga.percentuale_iva))
            riga_testata.valore_unitario_netto =calcolaPrezzoIva(riga.valore_unitario_netto, (-1*riga.percentuale_iva))
            righe_testata.append(riga_testata)
        daoTestataMovimento.righeMovimento = righe_testata

        daoTestataMovimento.scontiSuTotale = []
        if not daoTestataMovimento.numero:
            valori = numeroRegistroGet(tipo="Movimento", date=daoTestataMovimento.data_documento)
            daoTestataMovimento.numero = valori[0]
            #self.dao.registro_numerazione= valori[1]
        daoTestataMovimento.persist()
        messageInfo(msg="Duplicazione in movimento correttamente effettuato")
        return daoTestataMovimento.id


    def creaFatturaDaScheda(self):
        """
        Genera una testata documento come Fattura di vendita per la fatturazione
        degli articoli nella scheda ordinazione.
        """

        daoTestataFattura = TestataDocumento()
        daoTestataFattura.data_documento = datetime.datetime.today()
        daoTestataFattura.id_cliente = self.dao.id_cliente
        #controlla la creazione della destinazione merce secondo la scheda
        if self.dao.presso or self.dao.via_piazza or self.dao.num_civ or\
            self.dao.localita or self.dao.provincia:
            dmt = DestinazioneMerce().select(idCliente=self.dao.id_cliente)
            if dmt:
                daoTestataFattura.id_destinazione_merce = dmt[0].id
            else:
                destinazione_merce_testata = DestinazioneMerce()
                destinazione_merce_testata.denominazione = self.dao.presso or self.dao.referente
                destinazione_merce_testata.indirizzo = 'Via '+self.dao.via_piazza+' '+self.dao.num_civ
                destinazione_merce_testata.localita = self.dao.localita
                destinazione_merce_testata.cap = self.dao.zip
                destinazione_merce_testata.provincia = self.dao.provincia
                destinazione_merce_testata.id_cliente = self.dao.id_cliente
                destinazione_merce_testata.persist()
                daoTestataFattura.id_destinazione_merce = destinazione_merce_testata.id
        if self.dao.id_magazzino is None:
            obligatoryField(None, msg='Selezionare un magazzino per la generazione della fattura.')
        daoTestataFattura.id_aliquota_iva_esenzione = None
        daoTestataFattura.causale_trasporto = None
        daoTestataFattura.aspetto_esteriore_beni = None
        daoTestataFattura.totale_colli = 1
        daoTestataFattura.note_interne = 'Fattura associata a scheda lavorazione numero '+str(self.dao.numero)
        daoTestataFattura.note_pie_pagina = None
        daoTestataFattura.documento_saldato = self.dao.documento_saldato or False
##        daoTestataFattura.sconti = self.dao.sconti
        daoTestataFattura.registro_numerazione = 'registro_fattura_vendita'
        daoTestataFattura.operazione = 'Fattura vendita'
        daoTestataFattura.protocollo = ''
        daoTestataFattura.inizio_trasporto =None
        daoTestataFattura.fine_trasporto = None
        daoTestataFattura.incaricato_trasporto = 'mittente'
        daoTestataFattura.totale_peso = None
        daoTestataFattura.applicazione_sconti = self.dao.applicazione_sconti
        daoTestataFattura.porto = 'franco'
        daoTestataFattura.ripartire_importo = False
        if daoTestataFattura.documento_saldato:
            daoTestataFattura.totale_pagato = float(self.ui.tot_scontato_entry.get_text()) or 0
            daoTestataFattura.totale_sospeso = 0
        else:
            daoTestataFattura.totale_pagato = 0
            daoTestataFattura.totale_sospeso = float(self.ui.tot_scontato_entry.get_text()) or 0
        daoTestataFattura.id_banca = None
        righe_testata = []

        #TODO: Da fare con urgenza
        for riga in self.dao.righe:
            riga_testata = RigaDocumento()
            riga_testata.id_articolo = riga.id_articolo
            riga_testata.id_magazzino = riga.id_magazzino
            riga_testata.descrizione = riga.descrizione
            riga_testata.id_listino = riga.id_listino
            riga_testata.percentuale_iva = riga.percentuale_iva
            riga_testata.applicazione_sconti = riga.applicazione_sconti
            riga_testata.quantita = riga.quantita
            riga_testata.id_multiplo = riga.id_multiplo
            riga_testata.moltiplicatore = riga.moltiplicatore
            if riga.scontiRiga:
                for sconto in riga.scontiRiga:
                    self.ui.setScontiRiga(riga_testata, 'documento')
            try:
                riga_testata.scontiRigaDocumento = riga_testata.scontiRiga
            except:
                riga_testata.scontiRigaDocumento = []

            riga_testata.valore_unitario_lordo = calcolaPrezzoIva(riga.valore_unitario_lordo, (-1*riga.percentuale_iva))
            riga_testata.valore_unitario_netto =calcolaPrezzoIva(riga.valore_unitario_netto, (-1*riga.percentuale_iva))
            righe_testata.append(riga_testata)
        daoTestataFattura.righeDocumento = righe_testata

        daoTestataFattura.scontiSuTotale = []
        if not daoTestataFattura.numero:
            valori = numeroRegistroGet(tipo=daoTestataFattura.operazione, date=daoTestataFattura.data_documento)
            daoTestataFattura.numero = valori[0]
            #self.dao.registro_numerazione= valori[1]
        daoTestataFattura.persist()
        messageInfo(msg="Duplicazione in fattura  correttamente effettuato")
        return daoTestataFattura.id

    def advertise(self, msg):
        return YesNoDialog(msg=msg, transient=self.ui.dialogTopLevel)
