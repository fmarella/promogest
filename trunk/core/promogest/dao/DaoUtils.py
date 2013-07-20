# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment


def numeroRegistroGet(tipo=None, date=None):
    """
    """
    #TODO: aggiungere i check sui diversi tipi di rotazione
    from promogest.dao.TestataMovimento import TestataMovimento
    from promogest.dao.TestataDocumento import TestataDocumento
    from promogest.dao.Setting import Setting

    numeri = []

    registro = Setting().getRecord(id=str(tipo + ".registro").strip())
    if not registro:
        raise Exception("Registro numerazione non trovato.")

    registrovalue = registro.value
    registrovalueforrotazione = registrovalue+".rotazione"
    rotazione = Setting().select(keys=registrovalueforrotazione)
    if not rotazione:
        Environment.pg2log.info("Registro rotazione numerazione non trovato (tipo documento=%s)." % tipo)

    rotazione_temporale_dict = {'annuale':"year",
                                "mensile":"month",
                                "giornaliera":"day"}

    from sqlalchemy import func
    if tipo == "Movimento":
        numeroSEL = Environment.session.query(func.max(TestataMovimento.numero)).filter((and_(TestataMovimento.data_movimento.between(datetime.date(date.year, 1, 1), datetime.date(date.year + 1, 1, 1)),
                TestataMovimento.registro_numerazione==registrovalue))).one()[0]
    else:
        numeroSEL = Environment.session.query(func.max(TestataDocumento.numero)).filter((and_(TestataDocumento.data_documento.between(datetime.date(date.year, 1, 1), datetime.date(date.year + 1, 1, 1)),
                TestataDocumento.registro_numerazione==registrovalue))).one()[0]
    if numeroSEL:
        numero = numeroSEL + 1
    else:
        numero = 1
    return (numero, registrovalue)


def giacenzaDettaglio( daData=None, aData=None,
                        year=None, idMagazzino=None,
                        idArticolo=None, allMag=None):
    """
    Calcola la quantità di oggetti presenti in magazzino
    """
    from promogest.dao.TestataMovimento import TestataMovimento
    from promogest.dao.TestataDocumento import TestataDocumento

    from promogest.dao.RigaMovimento import RigaMovimento
    from promogest.dao.Riga import Riga
    from promogest.dao.Fornitura import Fornitura
    from promogest.dao.Magazzino import Magazzino

    def addFornitura(data=None):
        return Fornitura().select(idArticolo=idArticolo, dataFornitura=data)

    if allMag:
        magazzini = Environment.params["session"].query(Magazzino.id).all()
        if not magazzini:
            return []
        else:
            mag = []
            #magazzini = magazzini[0]
            for m in magazzini:
                mag.append(m[0])
            magazzini = mag
        righeArticoloMovimentate = Environment.params["session"]\
                .query(RigaMovimento, TestataMovimento)\
                .filter(TestataMovimento.data_movimento.between(
                            daData or datetime.date(int(year), 1, 1),
                            aData or datetime.date(int(year) + 1, 1, 1)))\
                .filter(
                    RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                .filter(Riga.id_articolo == idArticolo)\
                .filter(Riga.id_magazzino.in_(magazzini))\
                .order_by(TestataMovimento.data_movimento)\
                .all()
    else:
        magazzini = idMagazzino
        righeArticoloMovimentate = Environment.params["session"]\
                .query(RigaMovimento, TestataMovimento)\
                .filter(TestataMovimento.data_movimento.between(
                    daData or datetime.date(int(year), 1, 1),
                    aData or datetime.date(int(year) + 1, 1, 1)))\
                .filter(
                    RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                .filter(Riga.id_articolo == idArticolo)\
                .filter(Riga.id_magazzino == magazzini)\
                .order_by(TestataMovimento.data_movimento)\
                .all()
    lista = []
    giacenza = 0
    for ram in righeArticoloMovimentate:
        if ram[1].segnoOperazione == "+":
            fornitura = addFornitura(data=ram[1].data_movimento)
        else:
            fornitura = None
        if ram[1]:
            daoTestataDocumento = None
            idTestataDocumento = ram[1].id_testata_documento
            if idTestataDocumento:
                daoTestataDocumento = TestataDocumento().getRecord(
                                                    id=idTestataDocumento)

        qua = ram[0].quantita * ram[0].moltiplicatore
        magazzino = ""
        if ram[1].segnoOperazione == "-":
            if ram[1].operazione == "Scarico Scomposizione kit" \
                                        and "$SSK$" in ram[0].descrizione:
                giacenza += qua
            else:
                giacenza += -1 * qua
        elif ram[1].segnoOperazione == "+":
            giacenza = qua
        elif ram[1].segnoOperazione == "=":
            if ram[1].operazione == "Trasferimento merce magazzino":
                if ram[0].id_magazzino == ram[1].id_to_magazzino:
                    if qua >= 0:
                        giacenza = qua
                    else:
                        giacenza = -1 * qua
                else:
                    if qua <= 0:
                        giacenza = qua
                    else:
                        giacenza = -1 * qua
                if ram[0].id_magazzino == ram[1].id_to_magazzino:
                    magazzino = ram[0].magazzino
        valore = giacenza * ram[0].valore_unitario_netto

        diz = {"daoRigaMovimento": ram[0],
                "daoTestataMovimento": ram[1],
                "daoTestataDocumento": daoTestataDocumento,
                "magazzino": magazzino,
                "numero": ram[1].numero,
                "fornitura": fornitura,
                "data_movimento": ram[1].data_movimento,
                "operazione": ram[1].operazione,
                "id_articolo": ram[0].id_articolo,
                "giacenza": giacenza,
                "cliente": ram[1].ragione_sociale_cliente,
                "fornitore": ram[1].ragione_sociale_fornitore,
                "valore": valore,
                "segnoOperazione": ram[1].segnoOperazione,
                    }
        lista.append(diz)
        giacenza = 0
    return lista


def articoloStatistiche(arti=None, righe=None):

    prezzo_ultimo_vendita = 0
    prezzo_ultimo_acquisto = 0
    quantita_acquistata = 0
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
        new_data = datetime.datetime(2003, 7, 14, 12, 30)
        for riga in righe:
            rm = riga[0]
            tm = riga[1]
            data_movimento = tm.data_movimento
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
                quantita_venduta += rm.quantita * rm.moltiplicatore
            else:
                quantita_acquistata += rm.quantita * rm.moltiplicatore
            giacenza = abs(quantita_acquistata - quantita_venduta)

        if prezzo_acquisto:
            media_acquisto = sum(prezzo_acquisto) / len(prezzo_acquisto)
        else:
            media_acquisto = 0
        if prezzo_vendita:
            media_vendita = sum(prezzo_vendita) / len(prezzo_vendita)
        else:
            media_vendita = 0
        arti.update(prezzo_ultima_vendita=prezzo_ultimo_vendita,
                    data_ultima_vendita=data_ultima_vendita,
                    prezzo_ultimo_acquisto=prezzo_ultimo_acquisto,
                    data_ultimo_acquisto=data_ultimo_acquisto,
                    media_acquisto=media_acquisto,
                    media_vendita=media_vendita,
                    quantita_venduta=quantita_venduta,
                    quantita_acquistata=quantita_acquistata,
                    giacenza=giacenza)
    else:
        arti.update(prezzo_ultima_vendita=0,
                data_ultima_vendita=data_ultima_vendita,
                prezzo_ultimo_acquisto=0,
                data_ultimo_acquisto=data_ultimo_acquisto,
                media_acquisto=0,
                media_vendita=0,
                quantita_venduta=0,
                quantita_acquistata=0,
                giacenza=0)
    return arti


def giacenzaArticolo(
daData=None, aData=None,year=None, idMagazzino=None, idArticolo=None,
                                                                allMag=None):
    """
    Calcola la quantità di oggetti presenti in magazzino
    """
    from promogest.dao.TestataMovimento import TestataMovimento
    from promogest.dao.RigaMovimento import RigaMovimento
    from promogest.dao.Operazione import Operazione
    from promogest.dao.Magazzino import Magazzino
    if not year:
        year = Environment.workingYear
    if not idArticolo or (not idMagazzino and not allMag):
        return "0"
    if allMag:
        magazzini = Environment.params["session"].query(Magazzino.id).all()
        if not magazzini:
            return []
        else:
            mag = []
            for m in magazzini:
                mag.append(m[0])
            magazzini = mag
        righeArticoloMovimentate = Environment.params["session"]\
                .query(RigaMovimento.quantita,
                        RigaMovimento.moltiplicatore,
                        RigaMovimento.valore_unitario_netto,
                        Operazione.segno,
                        RigaMovimento.id,
                        RigaMovimento.descrizione)\
                .join(TestataMovimento, Operazione)\
                .filter(TestataMovimento.data_movimento.between(
                    daData or datetime.date(int(year), 1, 1),
                    aData or datetime.date(int(year) + 1, 1, 1)))\
                .filter(
                    RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                .filter(RigaMovimento.id_magazzino.in_(magazzini))\
                .filter(RigaMovimento.id_articolo == idArticolo)\
                .all()
    else:
        magazzini = idMagazzino
        righeArticoloMovimentate = Environment.params["session"]\
                .query(RigaMovimento.quantita,
                        RigaMovimento.moltiplicatore,
                        RigaMovimento.valore_unitario_netto,
                        Operazione.segno,
                        RigaMovimento.id,
                        RigaMovimento.descrizione)\
                .join(TestataMovimento, Operazione)\
                .filter(TestataMovimento.data_movimento.between(
                    daData or datetime.date(int(year), 1, 1),
                    aData or datetime.date(int(year) + 1, 1, 1)))\
                .filter(
                    RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                .filter(RigaMovimento.id_magazzino == magazzini)\
                .filter(RigaMovimento.id_articolo == idArticolo)\
                .all()

    giacenza = 0
    piu = 0
    meno = 0
    for ram in righeArticoloMovimentate:
        segno = ram[3]
        qua = ram[0] * ram[1]
        if segno == "-":
            if "$SSK$" in ram[5]:
                giacenza += qua
                piu += qua
            else:
                giacenza -= qua
                meno += qua

        elif segno == "+":
            giacenza += qua
            piu += abs(qua)

        elif segno == "=":
            r = RigaMovimento().getRecord(id=ram[4])
            tm = TestataMovimento().getRecord(id=r.id_testata_movimento)
            if tm.operazione == "Trasferimento merce magazzino":
                if r.id_magazzino == tm.id_to_magazzino:
                    if qua >= 0:
                        giacenza += qua
                        piu += qua
                    else:
                        giacenza += -1 * qua
                        meno += qua
                else:
                    if qua <= 0:
                        giacenza += qua
                        piu += qua
                    else:
                        giacenza += -1 * qua
                        meno += qua

    if len(righeArticoloMovimentate):
        val = giacenza * ram[2]
    else:
        val = 0
    return (round(giacenza, 2), round(val, 2), piu, round(meno, 2))


def TotaleAnnualeCliente(id_cliente=None):
    """
    Ritorna il totale avere da un cliente
    """
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiCliente = TestataDocumento().select(idCliente=id_cliente,
                                                batchSize=None)
    totale = 0
    for doc in documentiCliente:
        if doc.operazione in ["Fattura vendita",
                                'Fattura differita vendita',
                                'Fattura accompagnatoria',
                                'Vendita dettaglio',
                                'Nota di credito a cliente']:
            if not doc.totale_pagato:
                doc.totale_pagato = 0
            if not doc.totale_sospeso:
                doc.totale_sospeso = 0
            totale += (doc.totale_pagato + doc.totale_sospeso)
    return totale


def TotaleClienteAperto(id_cliente=None):
    """
    Ritorna il totale avere da un cliente
    """
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiCliente = TestataDocumento().select(idCliente=id_cliente,
                                                    batchSize=None)
    totale = 0
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
    totale = 0
    for doc in documentiFornitore:
        if doc.operazione in ['Fattura acquisto',
                            'Fattura differita acquisto',
                            'Nota di credito da fornitore']:
            if not doc.totale_pagato:
                doc.totale_pagato = 0
            if not doc.totale_sospeso:
                doc.totale_sospeso = 0
            totale += (doc.totale_pagato + doc.totale_sospeso)
    return totale


def TotaleFornitoreAperto(id_fornitore=None):
    """
    Calcola i sospesi del fornitore
    """
    from promogest.dao.TestataDocumento import TestataDocumento
    documentiFornitore = TestataDocumento().select(idFornitore=id_fornitore,
                                                    batchSize=None)
    totale = 0
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
    row = RigaDocumento().select(idTestataDocumento=id,
                                                offset=None,
                                                batchSize=None)
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
    row = RigaMovimento().select(idTestataMovimento=id,
                                offset=None,
                                batchSize=None)
    if row:
        sm = posso("SM")
        for r in row:
            if sm:
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
    row = ScontoTestataDocumento().select(idScontoTestataDocumento=id,
                                                    offset=None,
                                                    batchSize=None)
    if row:
        for r in row:
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True


def scontiVenditaDettaglioDel(idListino=None,
                                    idArticolo=None,
                                    dataListinoArticolo=None):
    """
    cancella gli sconti associati al listino articolo
    """
    from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
    row = ScontoVenditaDettaglio().select(idListino=idListino,
                                    idArticolo=idArticolo,
                                    dataListinoArticolo=dataListinoArticolo,
                                    offset=None,
                                    batchSize=None,
                                    orderBy=ScontoVenditaDettaglio.id_listino)
    if row:
        for r in row:
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True


def scontiVenditaIngrossoDel(idListino=None,
                                idArticolo=None, dataListinoArticolo=None):
    """
    cancella gli sconti associati al listino articolo
    """
    from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
    row = ScontoVenditaIngrosso().select(idListino=idListino,
                                    idArticolo=idArticolo,
                                    dataListinoArticolo=dataListinoArticolo,
                                    offset=None,
                                    batchSize=None,
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
    from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import \
                                                    TestataDocumentoScadenza
    row = TestataDocumentoScadenza().select(
                        idTestataDocumentoScadenza=id,
                        offset=None,
                        batchSize=None,
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
    row = ScontoRigaDocumento().select(idRigaDocumento=id,
                                                offset=None,
                                                batchSize=None)
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
    row = ScontoRigaMovimento().select(idRigaMovimento=id,
                                        offset=None,
                                        batchSize=None)
    if row:
        for r in row:
            Environment.params['session'].delete(r)
        Environment.params["session"].commit()
        return True


def ckd(dao):
    classe = dao.__class__.__name__

    stopp = False
    if classe not in ["TestataScontrino",
    "Articolo", "ArticoloTagliaColore", "TestataDocumento"]:
        return True
    records = Environment.session.query(dao.__class__).count()
    #print "CLASSE", classe, records,Environment.modulesList, "BASIC" in Environment.modulesList
    if "BASIC" in Environment.modulesList:
        if Environment.tipodb == "sqlite":
            if "TestataScontrino" in classe:
                if records > 16:
                    stopp = True
            if "TestataDocumento" in classe:
                if records > 48:
                    stopp = True
            if "Articolo" in classe:
                if records > 400:
                    stopp = True
            if "ArticoloTagliaColore" in classe:
                if records > 600:
                    stopp = True
            if "TestataCommessa" in classe:
                if records > 5:
                    stopp = True
    elif "STANDARD" in Environment.modulesList:
        if "+S" not in Environment.modulesList:
            if "TestataScontrino" in classe:
                if records > 16:
                    stopp = True
        if "+W" not in Environment.modulesList:
            if "ArticoloTagliaColore" in classe:
                if records > 600:
                    stopp = True
        if "TestataCommessa" in classe:
            if records > 5:
                stopp = True

    elif "FULL" in Environment.modulesList:
        if "+S" not in Environment.modulesList:
            if "TestataScontrino" in classe:
                if records > 16:
                    stopp = True
        if "+W" not in Environment.modulesList:
            if "ArticoloTagliaColore" in classe:
                if records > 600:
                    stopp = True
    if stopp:
        msg = """ATTENZIONE!
Hai raggiunto il limite massimo di inserimenti consentito
dalla versione del programma da te in uso
Acquista la versione "STANDARD" O "FULL" per attivarei moduli semplici
Oppure il modulo SHOP e/o WEAR per vendere al dettaglio
e/o la gestiore taglie e colori.

    GRAZIE"""
        from promogest.lib.utils import messageError
        messageError(msg=msg)
        Environment.params["session"].rollback()
        return False
    return True

def codeIncrement(value):
    """
    FIXME
    @param value:
    @type value:
    """
    import re
    lastNum = re.compile(r'(?:[^\d]*(\d+)[^\d]*)+')

    def increment(s):
        """ look for the last sequence of number(s) in a string and increment """
        m = lastNum.search(s)
        if m:
            next = str(int(m.group(1))+1)
            start, end = m.span(1)
            s = s[:max(end-len(next), start)] + next + s[end:]
            return s

    return increment(value)

def getRecapitiCliente(idCliente):
    """Dato un cliente restituisce un dizionario dei recapiti"""
    from promogest.dao.daoContatti.ContattoCliente import ContattoCliente
    from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
    recaCli = {}
    cc = ContattoCliente().select(idCliente=idCliente)
    if cc:
        reca = RecapitoContatto().select(idContatto=cc[0].id,  batchSize=None)
        return reca
    return []

def getRecapitiFornitore(idFornitore):
    """Dato un cliente restituisce un dizionario dei recapiti"""
    from promogest.dao.daoContatti.ContattoFornitore import ContattoFornitore
    from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
    recaCli = {}
    cc = ContattoFornitore().select(idFornitore=idFornitore)
    if cc:
        reca = RecapitoContatto().select(idContatto=cc[0].id,  batchSize=None)
        return reca
    return []

def getRecapitiAnagraficaSecondaria(idAnagraficaSecondaria):
    """Dato un cliente restituisce un dizionario dei recapiti"""
    from promogest.dao.daoContatti.ContattoAnagraficaSecondaria import ContattoAnagraficaSecondaria
    from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
    recaCli = {}
    cc = ContattoAnagraficaSecondaria().select(idAnagraficaSecondaria=idAnagraficaSecondaria)
    if cc:
        reca = RecapitoContatto().select(idContatto=cc[0].id,  batchSize=None)
        return reca
    return []

def get_columns(table):
    """ritorna la lista dei nomi delle colonne di una tabella

    :table: istanza di una tabella del database
    :returns: nomi delle colonne
    """
    return [c.name for c in table.columns]
