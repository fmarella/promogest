# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author: Francesco <francesco@promotux.it>

from promogest.dao.Dao import Dao
from promogest.dao.Listino import Listino
from promogest.Environment import *
from promogest.ui.utils import *
from promogest.modules.SchedaLavorazione.dao.RigaSchedaOrdinazione import RigaSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.ScontoRigaScheda import ScontoRigaScheda
from promogest.modules.SchedaLavorazione.dao.ScontoSchedaOrdinazione import ScontoSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.ColoreStampa import ColoreStampa
from promogest.modules.SchedaLavorazione.dao.CarattereStampa import CarattereStampa
from promogest.modules.SchedaLavorazione.dao.PromemoriaSchedaOrdinazione import PromemoriaSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.Datario import Datario
from promogest.modules.SchedaLavorazione.dao.ContattoScheda import ContattoScheda
from promogest.modules.SchedaLavorazione.dao.NotaScheda import NotaScheda
from promogest.modules.SchedaLavorazione.dao.RecapitoSpedizione import RecapitoSpedizione
from promogest.dao.Cliente import Cliente
from promogest.dao.Magazzino import Magazzino
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
from promogest.dao.DestinazioneMerce import DestinazioneMerce



class DuplicaInFattura(object):

    def __init__(self, dao=None, ui=None):
        self.dao = dao
        self.ui = ui
        pass


    def checkField(self):
        if self.dao.id_cliente == None:
            obligatoryField(None, msg='scegliere prima un cliente da associare al documento')
            return
            if self.dao.id is None:
                msg = "Prima di poter generare la fattura di questa scheda e' necessario salvarla .\n Salvare ?"
                response = self.advertise(msg)
                if response == gtk.RESPONSE_YES:
                    if not self.dao.fattura:
                        self.ui.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                        idFattura = self.creaFatturaDaScheda()
                        self.dao.ricevuta_associata = TestataDocumento().getRecord(id=idFattura).numero
                        self.ui.n_documento_entry.set_text(str(self.dao.ricevuta_associata))
                        self.dao.fattura = True
                        self.ui.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
                        self._refresh()
                    else:
                        if self.dao.ricevuta_associata is not None:
                            ricevuta_num = self.dao.ricevuta_associata
                            self.advertise("La presente scheda ha gia' generato una fattura (numero "+ricevuta_num+").")
                    return
                else:
                    return
            else:
                if not self.dao.fattura:
                    self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, gtk.RESPONSE_APPLY)
                    #idFattura = self.creaFatturaDaScheda()
                    self.dao.ricevuta_associata = TestataDocumento().getRecord(id=idFattura).numero
                    self.ui.n_documento_entry.set_text(str(self.dao.ricevuta_associata))
                    self.dao.fattura = True
                    self.ui.on_anagrafica_complessa_detail_dialog_response(self.ui.dialogTopLevel, gtk.RESPONSE_APPLY)
                    self._refresh()
                    return
                else:
                    if self.dao.ricevuta_associata is not None:
                        ricevuta_num = self.dao.ricevuta_associata
                        msg = "La presente scheda ha gia' generato una fattura (numero "+ricevuta_num+")."
                    else:
                        msg = "La presente scheda ha gia' generato una fattura,\nma non è possibile stabilire il numero del documento."
                    self.advertise(msg)
                    return

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
            daoTestataFattura.totale_sospeso =  float(self.ui.tot_scontato_entry.get_text()) or 0
        daoTestataFattura.id_banca = None
        righe_testata = []

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
            riga_testata.scontiRigaDocumento = []
            if len(riga.sconti) > 0:
                for sconto in riga.sconti:
                    self.setScontiRiga(riga_testata, 'documento')

            riga_testata.valore_unitario_lordo = calcolaPrezzoIva(riga.valore_unitario_lordo, (-1*riga.percentuale_iva))
            riga_testata.valore_unitario_netto =calcolaPrezzoIva(riga.valore_unitario_netto, (-1*riga.percentuale_iva))
            righe_testata.append(riga_testata)
        daoTestataFattura.righeDocumento = righe_testata

##        scontiTestata = []
##        scontoTestata = None
##        for sconto in self.dao.sconti:
##            scontoTestata = ScontoTestataDocumento(Environment.connection)
##            scontoTestata.tipo_sconto =sconto.tipo_sconto
##            scontoTestata.valore = sconto.valore
##            scontiTestata.append(scontoTestata)
        scontiSuTotale = []
        res = self.ui.sconti_scheda_widget.getSconti()
        if res is not None:
            for k in range(0, len(res)):
                daoSconto = ScontoSchedaOrdinazione()
                daoSconto.valore = float(res[k]["valore"])
                daoSconto.tipo_sconto = res[k]["tipo"]
                scontiSuTotale.append(daoSconto)

        daoTestataFattura.scontiSuTotale = scontiSuTotale
        if not daoTestataFattura.numero:
            valori = numeroRegistroGet(tipo=daoTestataFattura.operazione, date=daoTestataFattura.data_documento)
            daoTestataFattura.numero = valori[0]
            #self.dao.registro_numerazione= valori[1]
        daoTestataFattura.persist()
        return daoTestataFattura.id

    def advertise(self, msg):
        dialog = gtk.MessageDialog(self.ui.dialogTopLevel,
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION,
                                   gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        return response