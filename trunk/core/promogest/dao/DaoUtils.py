# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
import datetime
import gtk

def giacenzaSel(year=None, idMagazzino=None, idArticolo=None,allMag= None):
    """
    Calcola la quantità di oggetti presenti in magazzino
    @param year=None: Anno di riferimento
    @type year=None: Intero
    @param idMagazzino=None: se c'è questo è l'id magazzino
    @type idMagazzino=None: interno
    @param idArticolo=None: Id Articolo da quantificare
    @type idArticolo=None:
    @param allMag=: Tutti i magazzini ( utile per l'html )
    @type allMag=: bool
    """
    from TestataMovimento import TestataMovimento
    from RigaMovimento import RigaMovimento
    from Riga import Riga
    from promogest.dao.Magazzino import Magazzino
    if allMag:
        magazzini = Environment.params["session"].query(Magazzino.id).all()[0]
    else:
        magazzini = [idMagazzino]
    righeArticoloMovimentate= Environment.params["session"]\
            .query(RigaMovimento,TestataMovimento)\
            .filter(TestataMovimento.data_movimento.between(datetime.date(int(year), 1, 1), datetime.date(int(year) + 1, 1, 1)))\
            .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
            .filter(Riga.id_articolo==idArticolo)\
            .filter(Riga.id_magazzino.in_(magazzini))\
            .all()

    lista = []
    for ram in righeArticoloMovimentate:

        def calcolaGiacenza(quantita=None, moltiplicatore=None, segno=None, valunine=None):
            """
            Effettua realmente il calcolo
            """
            giacenza=0
            if segno =="-":
                giacenza -= quantita*moltiplicatore
            else:
                giacenza += quantita*moltiplicatore
            valore= giacenza*valunine
            return (giacenza, valore)

        diz = {"numero":ram[1].numero,
                "data_movimento":ram[1].data_movimento,
                "operazione":ram[1].operazione,
                "id_articolo":ram[0].id_articolo,
                "giacenza":calcolaGiacenza(quantita=ram[0].quantita,moltiplicatore=ram[0].moltiplicatore, segno=ram[1].segnoOperazione, valunine=ram[0].valore_unitario_netto)[0],
                "cliente":ram[1].ragione_sociale_cliente,
                "fornitore":ram[1].ragione_sociale_fornitore,
                "valore":calcolaGiacenza(quantita=ram[0].quantita,moltiplicatore=ram[0].moltiplicatore, segno=ram[1].segnoOperazione, valunine=ram[0].valore_unitario_netto)[1],
                "segnoOperazione":ram[1].segnoOperazione,
                    }
        lista.append(diz)
    return lista

def articoloStatistiche(arti=None, righe=None):

    prezzo_ultimo_vendita = 0
    prezzo_ultimo_acquisto = 0
    quantita_acquistata= 0
    quantita_venduta = 0
    data_ultimo_acquisto = ""
    data_ultima_vendita = ""
    prezzo_vendita = []
    prezzo_acquisto = []
    if arti:
        arti = arti
    else:
        arti = {}
    if righe:
        new_data =datetime.datetime(2003, 7, 14, 12, 30)
        for riga in righe:
            rm = riga[0]
            tm = riga[1]
            data_movimento=tm.data_movimento
            if data_movimento >= new_data:
                new_data = data_movimento
                if tm.segnoOperazione == "-":
                    prezzo_ultimo_vendita = rm.valore_unitario_netto
                    data_ultima_vendita = new_data
                else:
                    prezzo_ultimo_acquisto = rm.valore_unitario_netto
                    data_ultimo_acquisto = new_data
            if tm.segnoOperazione == "-":
                prezzo_vendita.append(rm.valore_unitario_netto)
            else:
                prezzo_acquisto.append(rm.valore_unitario_netto)
            if tm.segnoOperazione == "-":
                quantita_venduta += rm.quantita *rm.moltiplicatore
            else:
                quantita_acquistata += rm.quantita *rm.moltiplicatore
            giacenza = abs(quantita_acquistata-quantita_venduta)

        if prezzo_acquisto:
            media_acquisto = sum(prezzo_acquisto) / len(prezzo_acquisto)
        else:
            media_acquisto = 0
        if prezzo_vendita:
            media_vendita = sum(prezzo_vendita) / len(prezzo_vendita)
        else:
            media_vendita = 0
        arti.update(prezzo_ultima_vendita = prezzo_ultimo_vendita,
                    data_ultima_vendita = data_ultima_vendita,
                    prezzo_ultimo_acquisto = prezzo_ultimo_acquisto,
                    data_ultimo_acquisto = data_ultimo_acquisto,
                    media_acquisto = media_acquisto,
                    media_vendita = media_vendita,
                    quantita_venduta = quantita_venduta,
                    quantita_acquistata = quantita_acquistata,
                    giacenza = giacenza)
    else:
        arti.update(prezzo_ultima_vendita = 0,
                data_ultima_vendita = data_ultima_vendita,
                prezzo_ultimo_acquisto = 0,
                data_ultimo_acquisto = data_ultimo_acquisto,
                media_acquisto = 0,
                media_vendita = 0,
                quantita_venduta = 0,
                quantita_acquistata = 0,
                giacenza = 0)
    return arti

def giacenzaArticolo(year=None, idMagazzino=None, idArticolo=None, allMag=None):
    """
    Calcola la giacenza insieme a giacenzaSel
    """
    if not idArticolo or not year or (not idMagazzino and not allMag):
        return "0"
    else:
        lista = giacenzaSel(year=year, idMagazzino=idMagazzino, idArticolo=idArticolo, allMag=allMag)
        totGiacenza = 0

        for t in lista:
            totGiacenza += (t['giacenza'] or 0)
            #totGiacenza += (t[4] or 0)

        return round(totGiacenza,2)


def TotaleAnnualeCliente(id_cliente=None):
    """
    Ritorna il totale avere da un cliente
    """
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiCliente = TestataDocumento().select(idCliente=id_cliente,
                                                batchSize=None)
    totale =0
    for doc in documentiCliente:
        if doc.operazione in ["Fattura vendita",
                                'Fattura differita vendita',
                                'Fattura accompagnatoria',
                                'Vendita dettaglio',
                                'Nota di credito a cliente']:
            if not doc.totale_pagato: doc.totale_pagato=0
            if not doc.totale_sospeso: doc.totale_sospeso=0
            totale += (doc.totale_pagato + doc.totale_sospeso)
    return totale


def TotaleClienteAperto(id_cliente=None):
    """
    Ritorna il totale avere da un cliente
    """
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiCliente = TestataDocumento().select(idCliente=id_cliente,
                                                    batchSize=None)
    totale =0
    for doc in documentiCliente:
        if doc.operazione in ["Fattura vendita",
                            'Fattura differita vendita',
                            'Fattura accompagnatoria',
                            'Vendita dettaglio',
                            'Nota di credito a cliente']:
            totale += doc.totale_sospeso
    return totale


def TotaleAnnualeFornitore(id_fornitore=None):
    """
    Calcola i sospesi del fornitore
    """
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiFornitore = TestataDocumento().select(idFornitore=id_fornitore,
                                                    batchSize=None)
    totale =0
    for doc in documentiFornitore:
        if doc.operazione in ['Fattura acquisto',
                            'Fattura differita acquisto',
                            'Nota di credito da fornitore']:
            if not doc.totale_pagato: doc.totale_pagato=0
            if not doc.totale_sospeso: doc.totale_sospeso=0
            totale += (doc.totale_pagato + doc.totale_sospeso)
    return totale


def TotaleFornitoreAperto(id_fornitore=None):
    """
    Calcola i sospesi del fornitore
    """
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiFornitore = TestataDocumento().select(idFornitore=id_fornitore,
                                                    batchSize=None)
    totale =0
    for doc in documentiFornitore:
        if doc.operazione in ['Fattura acquisto',
                                'Fattura differita acquisto',
                                'Nota di credito da fornitore']:
            totale += doc.totale_sospeso
    return totale

def righeDocumentoDel(id=None):
    """
    Cancella le righe associate ad un documento
    """
    from promogest.dao.RigaDocumento import RigaDocumento
    if posso("SM"):
        from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
    row = RigaDocumento().select(idTestataDocumento= id,
                                                offset = None,
                                                batchSize = None)
    if row:
        for r in row:
            if posso("SM"):
                mp = MisuraPezzo().select(idRiga=r.id)
                if mp:
                    for m in mp:
                        Environment.params['session'].delete(m)
                    Environment.params["session"].commit()
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True

def righeMovimentoDel(id=None):
    """
    Cancella le righe associate ad un documento
    """
    from promogest.dao.RigaMovimento import RigaMovimento
    if "SuMisura" in Environment.modulesList:
        from promogest.modules.SuMisura.dao.MisuraPezzo import MisuraPezzo
    row = RigaMovimento().select(idTestataMovimento= id,
                                offset = None,
                                batchSize = None)
    if row:
        for r in row:
            if posso("SM"):
                mp = MisuraPezzo().select(idRiga=r.id)
                if mp:
                    for m in mp:
                        Environment.params['session'].delete(m)
                    Environment.params["session"].commit()
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True

def scontiTestataDocumentoDel(id=None):
    """
    Cancella gli sconti associati ad un documento
    """
    from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
    row = ScontoTestataDocumento().select(idScontoTestataDocumento= id,
                                                    offset = None,
                                                    batchSize = None)
    if row:
        for r in row:
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True

def scontiVenditaDettaglioDel(idListino=None,idArticolo=None,dataListinoArticolo=None):
    """
    cancella gli sconti associati al listino articolo
    """
    from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
    row = ScontoVenditaDettaglio().select(idListino=idListino,
                                            idArticolo=idArticolo,
                                            dataListinoArticolo=dataListinoArticolo,
                                            offset = None,
                                            batchSize = None,
                                            orderBy=ScontoVenditaDettaglio.id_listino)
    if row:
        for r in row:
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True

def scontiVenditaIngrossoDel(idListino=None,idArticolo=None,dataListinoArticolo=None):
    """
    cancella gli sconti associati al listino articolo
    """
    from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
    row = ScontoVenditaIngrosso().select(idListino=idListino,
                                                    idArticolo=idArticolo,
                                                    dataListinoArticolo=dataListinoArticolo,
                                                    offset = None,
                                                    batchSize = None,
                                                    orderBy=ScontoVenditaIngrosso.id_listino)
    if row:
        for r in row:
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True

def testataDocumentoScadenzaDel(id=None):
    """
    Cancella la scadenza documento associato ad un documento
    """
    from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
    row = TestataDocumentoScadenza().select(idTestataDocumentoScadenza= id,
                                                                offset = None,
                                                                batchSize = None,
                                                                orderBy=TestataDocumentoScadenza.id_testata_documento)
    for r in row:
        Environment.params['session'].delete(r)
    Environment.params["session"].commit()
    return True

def scontiRigaDocumentoDel(id=None):
    """
    Cancella gli sconti legati ad una riga movimento
    """
    from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
    row = ScontoRigaDocumento().select(idRigaDocumento= id,
                                                offset = None,
                                                batchSize = None)
    if row:
        for r in row:
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True

def scontiRigaMovimentoDel(id=None):
    """
    Cancella gli sconti legati ad una riga movimento
    """
    from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
    row = ScontoRigaMovimento().select(idRigaMovimento= id,
                                        offset = None,
                                        batchSize = None)
    if row:
        for r in row:
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True

def ckd(dao):
    classe = dao.__class__.__name__
    Environment.pg2log.info("MODULI E OPZIONI" + str(Environment.modulesList) +str(Environment.tipo_pg))
    stopp = False
    if "ONE BASIC" in Environment.modulesList and Environment.tipodb =="sqlite":
        records = Environment.session.query(dao.__class__).count()
        if "TestataDocumento" in classe:
            if records > 50: stopp = True
        if "Listino" in classe:
            if records > 1: stopp = True
        if "Promemoria" in classe:
            if records > 5: stopp = True
        if "Articolo" in classe:
            if records > 500: stopp = True
        if "Banca" in classe:
            if records > 1: stopp = True
        if "CategoriaArticolo" in classe:
            if records > 3: stopp = True
        if "FamigliaArticolo" in classe:
            if records > 3: stopp = True
        if "Cliente" in classe:
            if records > 50: stopp = True
        if "Fornitore" in classe:
            if records > 10: stopp = True
        if "Magazzino" in classe:
            if records > 1: stopp = True
        if "Pagamento" in classe:
            if records > 3: stopp = True
        if "Vettore" in classe:
            if records > 1: stopp = True
        if "Colore" in classe:
            if records > 5: stopp = True
        if "Taglia" in classe:
            if records > 5: stopp = True
        if stopp:
            msg = """HAI RAGGIUNTO IL LIMITE MASSIMO CONSENTITO
DALLA VERSIONE ONE BASIC GRATUITA PER QUESTA OPERAZIONE, ACQUISTA
LA VERSIONE "ONE STANDARD" PER ELIMINARE TUTTI I LIMITI
O LA "ONE FULL" PER ATTIVARE ANCHE TUTTI I MODULI"""
            dialoggg = gtk.MessageDialog(None,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_INFO,
                    gtk.BUTTONS_OK,
                    msg)
            dialoggg.run()
            dialoggg.destroy()
            Environment.params["session"].rollback()
            return False
    elif "ONE STANDARD" in Environment.modulesList:
#        records = Environment.session.query(dao.__class__).count()
#        if "TestataDocumento" in classe:
#            if records > 50: stopp = True
        print "VERSIONE STANDARD", classe

#    else:
#        print " TUTTO OK PUOI ANDARE"
    return True
