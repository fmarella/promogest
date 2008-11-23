#-*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from sqlalchemy import and_, or_


def giacenzaSel(year=None, idMagazzino=None, idArticolo=None):
    from TestataMovimento import TestataMovimento
    from RigaMovimento import RigaMovimento
    from Riga import Riga
    from Operazione import Operazione

    righeArticoloMovimentate= params["session"]\
            .query(RigaMovimento,TestataMovimento)\
            .filter(and_(func.date_part("year", TestataMovimento.data_movimento)==year))\
            .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
            .filter(Riga.id_articolo==idArticolo)\
            .filter(Riga.id_magazzino==idMagazzino)\
            .all()

    lista = []
    for ram in righeArticoloMovimentate:

        def calcolaGiacenza(quantita=None, moltiplicatore=None, segno=None, valunine=None):
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
                "segnoOperazione":ram[1].segnoOperazione
                #"test_doc":ram[1].testata_documento.numero
                    }
        lista.append(diz)
    return lista

def TotaleAnnualeCliente(id_cliente=None):
    """ Ritorna il totale avere da un cliente """
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiCliente = TestataDocumento(isList=True).select(idCliente=id_cliente,
                                                    batchSize=None)
    totale =0
    for doc in documentiCliente:
        if doc.operazione in ["Fattura vendita",'Fattura differita vendita','Fattura accompagnatoria','Vendita dettaglio','Nota di credito a cliente']:
            totale += (doc.totale_pagato + doc.totale_sospeso)
    return totale


def TotaleClienteAperto(id_cliente=None):
    """ Ritorna il totale avere da un cliente """
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiCliente = TestataDocumento(isList=True).select(idCliente=id_cliente,
                                                    batchSize=None)
    totale =0
    for doc in documentiCliente:
        if doc.operazione in ["Fattura vendita",'Fattura differita vendita','Fattura accompagnatoria','Vendita dettaglio','Nota di credito a cliente']:
            totale += doc.totale_sospeso
    return totale


def TotaleAnnualeFornitore(id_fornitore=None):
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiFornitore = TestataDocumento(isList=True).select(idFornitore=id_fornitore,
                                                    batchSize=None)
    totale =0
    for doc in documentiFornitore:
        if doc.operazione in ['Fattura acquisto','Fattura differita acquisto''Nota di credito da fornitore']:
            totale += (doc.totale_pagato + doc.totale_sospeso)
    return totale


def TotaleFornitoreAperto(id_fornitore=None):
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiFornitore = TestataDocumento(isList=True).select(idFornitore=id_fornitore,
                                                    batchSize=None)
    totale =0
    for doc in documentiFornitore:
        if doc.operazione in ['Fattura acquisto','Fattura differita acquisto''Nota di credito da fornitore']:
            totale += doc.totale_sospeso
    return totale

def righeDocumentoDel(id=None):
    """Cancella le righe associate ad un documento"""
    from promogest.dao.RigaDocumento import RigaDocumento
    row = RigaDocumento(isList=True).select(idTestataDocumento= id,
                                                offset = None,
                                                batchSize = None,
                                                orderBy="id_testata_documento")
    if row:
        for r in row:
            params['session'].delete(r)
        params["session"].commit()
        return True

def righeMovimentoDel(id=None):
    """Cancella le righe associate ad un documento"""
    from promogest.dao.RigaMovimento import RigaMovimento
    row = RigaMovimento(isList=True).select(idTestataMovimento= id,
                                                    offset = None,
                                                    batchSize = None,
                                                    orderBy="id_testata_movimento")
    if row:
        for r in row:
            params['session'].delete(r)
        params["session"].commit()
        return True

def scontiTestataDocumentoDel(id=None):
    """Cancella gli sconti associati ad un documento"""
    from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
    row = ScontoTestataDocumento(isList=True).select(idScontoTestataDocumento= id,
                                                    offset = None,
                                                    batchSize = None,
                                                    orderBy="id_testata_documento")
    if row:
        for r in row:
            params['session'].delete(r)
        params["session"].commit()
        return True

def scontiVenditaDettaglioDel(idListino=None,idArticolo=None,dataListinoArticolo=None):
    """cancella gli sconti associati al listino articolo"""
    from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
    row = ScontoVenditaDettaglio(isList=True).select(idListino=idListino,
                                                    idArticolo=idArticolo,
                                                    #dataListinoArticolo=dataListinoArticolo,
                                                    offset = None,
                                                    batchSize = None,
                                                    orderBy="id_listino")
    if row:
        for r in row:
            params['session'].delete(r)
        params["session"].commit()
        return True

def scontiVenditaIngrossoDel(idListino_=None,idArticolo_=None,dataListinoArticolo_=None):
    """cancella gli sconti associati al listino articolo"""
    from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
    row = ScontoVenditaIngrosso(isList=True).select(idListino=idListino_,
                                                            idArticolo=idArticolo_,
                                                            dataListinoArticolo=dataListinoArticolo_,
                                                            offset = None,
                                                            batchSize = None,
                                                            orderBy="id_listino")
    if row:
        for r in row:
            params['session'].delete(r)
        params["session"].commit()
        return True

def testataDocumentoScadenzaDel(id=None):
    """Cancella la scadenza documento associato ad un documento"""
    from promogest.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
    row = TestataDocumentoScadenza(isList=True).select(idTestataDocumentoScadenza= id,
                                                                offset = None,
                                                                batchSize = None,
                                                                orderBy="id_testata_documento")
    for r in row:
        params['session'].delete(r)
    params["session"].commit()
    return True

def scontiRigaDocumentoDel(id=None):
    """Cancella gli sconti legati ad una riga movimento"""
    from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
    row = ScontoRigaDocumento(isList=True).select(idRigaDocumento= id,
                                                offset = None,
                                                batchSize = None)
    if row:
        for r in row:
            params['session'].delete(r)
        params["session"].commit()
        return True

def scontiRigaMovimentoDel(id=None):
    """Cancella gli sconti legati ad una riga movimento"""
    from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
    row = ScontoRigaMovimento(isList=True).select(idRigaMovimento= id,
                                                        offset = None,
                                                        batchSize = None)
    if row:
        for r in row:
            params['session'].delete(r)
        params["session"].commit()
        return True
