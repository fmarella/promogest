# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import sys
import datetime
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.sqlsoup import SqlSoup
#from promogest import Environment

OFFSET = 500
TABELLA = "testata_scontrino"
ORDERBY = "id"
MAGAZZINO = 3
POS = 2
USER = 1


MAINSCHEMA_LOCALE = "promogest2"
USER_LOCALE = "promoadmin"
PASSWORD_LOCALE = "admin"
HOST_LOCALE = "localhost"
PORT_LOCALE= "5432"
DATABASE_LOCALE = "promogest_db"
SCHEMA_LOCALE = "elisir"

MAINSCHEMA_REMOTO= "promogest2"
USER_REMOTO = "promoadmin"
PASSWORD_REMOTO = "admin"
HOST_REMOTO = "localhost"
PORT_REMOTO = "5432"
DATABASE_REMOTO = "promogest_db"
SCHEMA_REMOTO = "elisir"


class SpostaVenditaDettaglio(object):
    """ Finestra di gestione esdportazione variazioni Database
    """
    def __init__(self):
        print " ACCENDIAMO I MOTORI "
        self.runBatch()

    def connectDbRemote(self):
        """ effettua la connessione al DB remoto """
        engine = create_engine('postgres:'+'//'
                                +USER_REMOTO+':'
                                + PASSWORD_REMOTO+ '@'
                                + HOST_REMOTO + ':'
                                + PORT_REMOTO + '/'
                                + DATABASE_REMOTO,
                                encoding='utf-8',
                                convert_unicode=True )
        tipo_eng = engine.name
        engine.echo = False
        self.metaRemote = MetaData(engine)
        self.pg_db_server_remote = SqlSoup(self.metaRemote)
        self.pg_db_server_remote.schema = SCHEMA_REMOTO
        self.pg_db_server_main_remote = SqlSoup(self.metaRemote)
        self.pg_db_server_main_remote.schema = MAINSCHEMA_REMOTO
        SessionRemote = scoped_session(sessionmaker(bind=engine))
        self.sessionRemote = SessionRemote()
        print ">>>> CONNESSO AL DB REMOTO : %s IP: %s PORTA: %s SCHEMA %s <<<<< " %(DATABASE_REMOTO, HOST_REMOTO, PORT_REMOTO, SCHEMA_REMOTO)

    def connectDbLocale(self):
        """ effettua la connessione al DB locale """
        engineLocale = create_engine('postgres:'+'//'
                                        + USER_LOCALE +':'
                                        + PASSWORD_LOCALE + '@'
                                        + HOST_LOCALE + ':'
                                        + PORT_LOCALE + '/'
                                        + DATABASE_LOCALE,
                                        encoding='utf-8',
                                        convert_unicode=True )
        tipo_eng = engineLocale.name
        engineLocale.echo = False
        self.metaLocale = MetaData(engineLocale)
        self.pg_db_server_locale = SqlSoup(self.metaLocale)
        self.pg_db_server_locale.schema = SCHEMA_LOCALE
        self.pg_db_server_main_locale = SqlSoup(self.metaLocale)
        self.pg_db_server_main_locale.schema = MAINSCHEMA_LOCALE
        SessionLocale = scoped_session(sessionmaker(bind=engineLocale))
        self.engineLocale = engineLocale
        self.sessionLocale = SessionLocale()
        print ">>>> CONNESSO AL DB LOCALE : %s IP: %s PORTA: %s SCHEMA %s <<<<< " %(DATABASE_LOCALE, HOST_LOCALE, PORT_LOCALE, SCHEMA_LOCALE)

    def dammiSoupLocale(self, dao):
        soupLocale = None
        soupLocale = self.pg_db_server_locale
        return soupLocale

    def dammiSoupRemoto(self, dao):
        soupRemoto = None
        soupRemoto = self.pg_db_server_remoto
        return soupRemoto

    def daosScheme(self):
        """ Crea le liste delle query ciclando nelle tabelle """
        blocSize = OFFSET
        db = self.pg_db_server_remote
        daos = db.testata_scontrino.all()
        for ts in daos:
#        ts = daos[600]
            sts = db.sconto_testata_scontrino.filter(db.sconto_testata_scontrino.id_testata_scontrino == ts.id).all()
            stsdict = {}
            if sts:
                stss = db.sconto_scontrino.filter(db.sconto_scontrino.id == sts[0].id).one()
                stsdict = {
                "id" :stss.id,
                "valore": stss.valore,
                "tipo_sconto": stss.tipo_sconto}
            righe = db.riga_scontrino.filter(db.riga_scontrino.id_testata_scontrino==ts.id).all()
            rr = []
            if righe:
                for riga in righe:
                    scontoriga = db.sconto_riga_scontrino.filter(db.sconto_riga_scontrino.id_riga_scontrino == riga.id).all()
                    sr = {}
                    if scontoriga:
                        ssc = db.sconto_scontrino.filter(db.sconto_scontrino.id == scontoriga[0].id).one()
                        sr = {
                            "id" :ssc.id,
                            "valore": ssc.valore,
                            "tipo_sconto": ssc.tipo_sconto}
                    r = {
                      "id":riga.id,
                      "prezzo":riga.prezzo,
                      "prezzo_scontato": riga.prezzo_scontato,
                      "quantita":riga.quantita,
                      "descrizione":riga.descrizione,
                      "id_testata_scontrino": riga.id_testata_scontrino,
                      "id_articolo":riga.id_articolo,
                      "sconti": sr}
                    rr.append(r)
            scontrino = {
                    "id":ts.id,
                    "data_inserimento": ts.data_inserimento,
                    "totale_scontrino": ts.totale_scontrino,
                    "totale_contanti" : ts.totale_contanti,
                    "totale_assegni":ts.totale_assegni,
                    "totale_carta_credito": ts.totale_carta_credito,
                    "id_testata_movimento": ts.id_testata_movimento,
                    "id_magazzino":ts.id_magazzino or MAGAZZINO,
                    "id_ccardtype":ts.id_ccardtype,
                    "id_pos" : ts.id_pos or POS,
                    "id_user" : ts.id_user or USER,
                    "righe_scontrino" : rr,
                    "sconto_testata_scontrino": stsdict
                        }
            print scontrino
            dbl = self.pg_db_server_locale
            tsl = dbl.testata_scontrino.insert()
            tsl.data_inserimento = scontrino["data_inserimento"]
            tsl.totale_scontrino = scontrino["totale_scontrino"]
            tsl.totale_contanti = scontrino["totale_contanti"]
            tsl.totale_assegni = scontrino["totale_assegni"]
            tsl.totale_carta_credito = scontrino["totale_carta_credito"]
            tsl.id_testata_movimento = scontrino["id_testata_movimento"]
            tsl.id_magazzino = scontrino["id_magazzino"]
            tsl.id_ccardtype = scontrino["id_ccardtype"]
            tsl.id_pos = scontrino["id_pos"]
            tsl.id_user = scontrino["id_user"]
            sqlalchemy.ext.sqlsoup.Session.add(tsl)
            sqlalchemy.ext.sqlsoup.Session.commit()
            if scontrino["righe_scontrino"]:
                for riga in scontrino["righe_scontrino"]:
                    rl = dbl.riga_scontrino.insert()
                    rl.prezzo = riga["prezzo"]
                    rl.prezzo_scontato = riga["prezzo_scontato"]
                    rl.quantita = riga["quantita"]
                    rl.descrizione =riga["descrizione"]
                    rl.id_testata_scontrino = tsl.id
                    rl.id_articolo= riga["id_articolo"]
                    sqlalchemy.ext.sqlsoup.Session.add(rl)
                    sqlalchemy.ext.sqlsoup.Session.commit()
                    if riga["sconti"]:
                        sscl = dbl.sconto_scontrino.insert()
                        sscl.tipo_sconto = riga["sconti"]["tipo_sconto"]
                        sscl.valore = riga["sconti"]["valore"]
                        sqlalchemy.ext.sqlsoup.Session.add(sscl)
                        sqlalchemy.ext.sqlsoup.Session.commit()
                        srscl = dbl.sconto_riga_scontrino.insert()
                        srscl.id = sscl.id
                        srscl.id_riga_scontrino = rl.id
                        sqlalchemy.ext.sqlsoup.Session.add(srscl)
                        sqlalchemy.ext.sqlsoup.Session.commit()
            if scontrino["sconto_testata_scontrino"]:
                ssclt = dbl.sconto_scontrino.insert()
                ssclt.tipo_sconto = scontrino["sconto_testata_scontrino"]["tipo_sconto"]
                ssclt.valore = scontrino["sconto_testata_scontrino"]["valore"]
                sqlalchemy.ext.sqlsoup.Session.add(ssclt)
                sqlalchemy.ext.sqlsoup.Session.commit()
                stsl = dbl.sconto_testata_scontrino.insert()
                stsl.id = ssclt.id
                stsl.id_testata_scontrino = tsl.id
                sqlalchemy.ext.sqlsoup.Session.add(stsl)
                sqlalchemy.ext.sqlsoup.Session.commit()
            print "SALVATO SCONTRINO"
        print "<<<<<<< INIZIATO :", self.tempo_inizio, " FINITO:", datetime.datetime.now() , ">>>>>>>>>>>>>"
        print "SINCRONIZZAZIONE TERMINATA CON SUCCESSO"


    def runBatch(self):
        sqlalchemy.ext.sqlsoup.Session.expunge_all()
        self.connectDbRemote()
        self.connectDbLocale()
        self.tempo_inizio = datetime.datetime.now()
        print "INIZIO SINCRO",datetime.datetime.now()
        self.daosScheme()
        sqlalchemy.ext.sqlsoup.Session.expunge_all()
        sys.exit()

if __name__ == '__main__':
    SpostaVenditaDettaglio()
