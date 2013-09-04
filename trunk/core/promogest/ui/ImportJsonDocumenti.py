# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>
#    Author: Francesco Meloni  <francesco@promotux.it>

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

#from promogest import Environment as env
from promogest.ui.GladeWidget import GladeWidget
from promogest.dao.Articolo import Articolo, t_articolo
from promogest.dao.Listino import Listino
from promogest.dao.Cliente import Cliente
#from promogest.dao.Fornitore import Fornitore
#from promogest.dao.Vettore import Vettore
#from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.DaoUtils import numeroRegistroGet
from promogest.dao.Fornitura import Fornitura
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.Multiplo import Multiplo
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaDocumento import RigaDocumento
from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
from promogest.lib.utils import *

from datetime import datetime
from decimal import Decimal
from promogest.ui.gtk_compat import *
import simplejson as json

class ImportJsonDocumenti(GladeWidget):
    '''
    Classe di gestione della finestra di import json ordine da Cliente per Rudolf
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        GladeWidget.__init__(self, root='importa_json_window',
                             path='import_ordine_json_window.glade',
                             isModule=False)
        self.__parent = parent
        self.placeWindow(self.getTopLevel())
        #self.__setup_webview()
        self.draw()
        #self.show_all()

    def draw(self):
        return

    def on_annulla_button_clicked(self, button):
        self.destroy()

    def on_importa_json_button_clicked(self, button):
        a = """{
    "data":"2013-07-21 06:14:48",
    "promogest_id":"130",
    "utente":"Mario Rossi",
    "email":"mario@rossi.com",
    "prodotti":{
        "CALS5500LTAM35":"32",
        "COPZ21TASBI":"1",
        "COPZ21TAS23":"2",
        "COPZ21TAS45":"3",
        "COPZ21TASN":"4",
        "COPZ21TAGS37":"5",
        "COPZ21TAGS19":"6",
        "COPZ21TAGS63":"67",
        "COPZ21TAGS20":"8",
        "COPZ21TAGSR":"9",
        "COPZ21TAGSV":"10"
    }
}"""
        text_buffer = self.importa_json_textview.get_buffer()
        note = text_buffer.get_text(text_buffer.get_start_iter(),
                                            text_buffer.get_end_iter(), True)
        print "NOTE", note
        try:
            dati = json.loads(note)
        except:
            print "ERRORE DATI DELLA TEXTVIEW NON JSON"
            messageError("ERRORE DATI NELLA TEXTVIEW NON JSON")
            return
        print type(dati["prodotti"]), dati["utente"]
        #data_ordine = dati["data"] # datetime.datetime.now()'Jun 1 2005  1:33PM'
        data_ordine = datetime.strptime(dati["data"], '%Y-%m-%d %H:%M:%S')
        daoCliente = Cliente().getRecord(id=int(dati["promogest_id"]))

        pricelist = Listino().select(id=daoCliente.id_listino)
        newDao = TestataDocumento()
        newDao.data_documento = data_ordine
        newDao.data_inserimento = data_ordine
        newDao.operazione = "Ordine da cliente"
        newDao.id_cliente = daoCliente.id
        newDao.id_fornitore = None
        if daoCliente.dm:
            newDao.id_destinazione_merce = daoCliente.dm[0].id
        else:
            newDao.id_destinazione_merce = None
        #if tipoPagamento != "checked": #contrassegno
            #newDao.id_pagamento = 4
        #else:
            #newDao.id_pagamento = 5
        newDao.id_banca = None
        newDao.id_aliquota_iva_esenzione = None
        newDao.protocollo = ""
        newDao.causale_trasporto = ""
        newDao.aspetto_esteriore_beni = ""
        newDao.inizio_trasporto = None
        newDao.fine_trasporto = None
        newDao.id_vettore = None
        newDao.incaricato_trasporto = None
        newDao.totale_colli = None
        newDao.totale_peso = None
        newDao.note_interne = "Ordine da WEB"
        newDao.note_pie_pagina = ""
        newDao.applicazione_sconti = "scalare"
        righeDocumento=[]
        totale = 0
        for k,v in dati["prodotti"].iteritems():
            print " ERRREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", k,v
            quantita = int(v)
            art = Articolo().select(codiceEM=k)
            if art:
                idArticolo = art[0].id
            else:
                raise "non trovo l'articolo nel db"
            prezzo = leggiListino(pricelist[0].id, idArticolo, tiny=True)["prezzoIngrosso"]
            articolo = leggiArticolo(idArticolo)
            daoRiga = RigaDocumento()
            daoRiga.id_testata_documento = newDao.id
            daoRiga.id_articolo = idArticolo
            daoRiga.id_magazzino = 1
            daoRiga.descrizione = articolo["denominazione"]
            daoRiga.id_iva = articolo["idAliquotaIva"]
            daoRiga.id_listino = pricelist[0].id
            daoRiga.valore_unitario_lordo = prezzo
            daoRiga.valore_unitario_netto = prezzo
            daoRiga.percentuale_iva = articolo["percentualeAliquotaIva"]
            daoRiga.applicazione_sconti = []
            daoRiga.quantita = quantita
            daoRiga.id_multiplo = None
            daoRiga.moltiplicatore = 1
            daoRiga.scontiRigaDocumento = []
            righeDocumento.append(daoRiga)
            parziale = float(quantita) * float(leggiListino(pricelist[0].id, idArticolo, tiny=True)["prezzoDettaglio"])
            totale += parziale
        newDao.righeDocumento = righeDocumento
        newDao.totale_pagato = None
        newDao.totale_sospeso = None
        newDao.documento_saldato = None
        newDao.id_primo_riferimento = None
        newDao.id_secondo_riferimento = None
        tipo = "Ordine da cliente"
        valori = numeroRegistroGet(tipo=tipo, date=data_ordine)
        newDao.numero = valori[0]
        newDao.registro_numerazione= valori[1]
        if len(righeDocumento) > 0:
            newDao.persist()
        print "NEW DAO", newDao.__dict__
