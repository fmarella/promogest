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
from promogest import Environment

OFFSET = 500
TABELLA = "inventario"
ORDERBY = "id"


MAINSCHEMA_LOCALE = "promogest2"
USER_LOCALE = "promoadmin"
PASSWORD_LOCALE = "admin"
HOST_LOCALE = "localhost"
PORT_LOCALE= 5432
DATABASE_LOCALE = "promogest_db"
SCHEMA_LOCALE = "elisir"

MAINSCHEMA_REMOTO= "promogest2"
USER_REMOTO = "promoadmin"
PASSWORD_REMOTO = "admin"
HOST_REMOTO = "192.168.1.66"
PORT_REMOTO = 5432
DATABASE_REMOTO = "promogest_db"
SCHEMA_REMOTO = "elisir"


class SincroInventario(object):
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
        self.pg_db_server_main_locale.schema = mainschema_locale
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
        conteggia = self.pg_db_server_remote.entity(TABELLA).count() # serve per poter affettare le select
        print "NUMERO DEI RECORD PRESENTI:", conteggia
        if conteggia >= blocSize:
            blocchi = abs(conteggia/blocSize)
            for j in range(0,blocchi+1):
                offset = j*blocSize
                print "OFFSET", offset , datetime.datetime.now(), "TABELLA", TABELLA
                exec ("remote=self.pg_db_server_remote.%s.order_by(self.pg_db_server_remote.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                exec ("locale=self.pg_db_server_locale.%s.order_by(self.pg_db_server_locale.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                self.logica(remote=remote, locale=locale,dao=TABELLA, all=True, offset=offset)
        elif conteggia < blocSize: # SI FA LA QUERY IN UN UNICI BOCCONE
            exec ("remote=self.pg_db_server_remote.%s.order_by(self.pg_db_server_remote.%s.%s).all()") %(TABELLA,TABELLA,ORDERBY)
            exec ("locale=self.pg_db_server_locale.%s.order_by(self.pg_db_server_locale.%s.%s).all()") %(TABELLA,TABELLA,ORDERBY)
                self.logica(remote=remote, locale=locale,dao=TABELLA, all=True)
    print "<<<<<<< INIZIATO :", self.tempo_inizio, " FINITO:", datetime.datetime.now() , ">>>>>>>>>>>>>"
    print "SINCRONIZZAZIONE TERMINATA CON SUCCESSO"

    def logica(self,remote=None, locale=None,dao=None,all=False,offset=None):
        """ cicla le righe della tabella e decide cosa fare """
        soupLocale = self.dammiSoupLocale(dao)
        soupRemoto = self.dammiSoupRemoto(dao)
        deleteRow=False
        if not remote and not locale:
            return False

        if str(list(locale)) != str(list(remote)):
            if len(locale) == len(remote):
                print "STESSO NUMERO DI RECORD", len(remote)
            elif len(remote) > len(locale):
                print "IL DB LOCALE CONTIENE PIU' RECORD", len(locale), "vs", len(remote)
            else:
                print "IL DB REMOTO CONTIENE PIU' RECORD", len(locale), "vs", len(remote)
                deleteRow=True
            for i in range(0,(len(locale))):
                if i <= (len(remote)-1):
                    try:
                        if  remote[i] != locale[i]:
                            print "PROCEDO CON UN UPDATE", str(locale[i]._table).split(".")[1]
                            print
                            print "REMOTE:", remote[i]
                            print
                            print "LOCALE:",  locale[i]
                            self.fixToTable(soupLocale=soupLocale,
                                            row=remote[i],
                                            rowLocale=locale[i],
                                            op="UPDATE",
                                            dao=str(remote[i]._table).split(".")[1],
                                            save=True,
                                            offset=offset)
                    except:
                            self.fixToTable(soupLocale=soupLocale,
                                            row=remote[i],
                                            rowLocale=locale[i],
                                            op="UPDATE",
                                            dao=str(remote[i]._table).split(".")[1],
                                            save=True,
                                            offset=offset)

                else:
                    print " ", str(remote[i]._table).split(".")[1], "INSERT"
                    #print " RIGA REMOTE", remote[i]
                    self.fixToTable(soupLocale=soupLocale,
                                    row=remote[i],
                                    op="INSERT",
                                    dao=str(remote[i]._table).split(".")[1],
                                    save=False)
            tabe = str(remote[i]._table).split(".")[1]
            if tabe != "articolo":
                try:
                    sqlalchemy.ext.sqlsoup.Session.commit()
                except Exception, e:
                    sqlalchemy.ext.sqlsoup.Session.rollback()
                    self.azzeraTable(table=dao)
            if deleteRow:
                for i in range(len(remote),len(locale)):
                    print "QUESTA È LA RIGA DA rimuovere ", str(locale[i]._table).split(".")[1], "Operazione DELETE"
                    self.fixToTable(soupLocale=soupLocale,
                                    #row=locale[i],
                                    rowLocale = locale[i],
                                    op="DELETE",
                                    dao=str(locale[i]._table).split(".")[1],
                                    save=True)
        else:
            print "TABELLE o BLOCCHI CON NUM DI RECORD UGUALI"

    def fixToTable(self, soup =None,soupLocale=None, op=None, row=None,rowLocale=None, dao=None, save=False, offset=None):
        """
        rimanda alla gestione delle singole tabelle con le operazioni da fare
        """
        #soupLocale.clear()

        soupLocale = self.dammiSoupLocale(dao)

        if op =="DELETE":
            sqlalchemy.ext.sqlsoup.Session.delete(rowLocale)
            sqlalchemy.ext.sqlsoup.Session.commit()
        elif op == "INSERT":
            exec ("rowLocale = soupLocale.%s.insert()") %dao
            for i in rowLocale.c:
                t = str(i).split(".")[1] #mi serve solo il nome tabella
                setattr(rowLocale, t, getattr(row, t))
            sqlalchemy.ext.sqlsoup.Session.add(rowLocale)
#            sqlalchemy.ext.sqlsoup.Session.commit()
            return
        elif op == "UPDATE":
            try:
                for i in rowLocale.c:
                    #mi serve solo il nome colonna
                    t = str(i).split(".")[1]
                    setattr(rowLocale, t, getattr(row, t))
                sqlalchemy.ext.sqlsoup.Session.add(rowLocale)
            except Exception,e :
                print "ERRORE",e
                print "QUALCOSA NELL'UPDATE NON È ANDATO BENE ....VERIFICHIAMO"
                sqlalchemy.ext.sqlsoup.Session.rollback()
                print "FATTO IL ROOLBACK"
                print
                print "RIGA LOCALE", rowLocale
                print
                print "RIGA REMOTA", row


#    def azzeraTable(self, table=None):
#        if table in ["operazione","tipo_aliquota_iva","stato_articolo","unita_base",
#                    "tipo_recapito","denominazione"]:
#            record = self.pg_db_server_main_locale.entity(table).all()
#        else:
#            record=self.pg_db_server_locale.entity(table).all()
#        if table =="listino":
#            record2=self.pg_db_server_locale.entity("listino_magazzino").all()
#            for g in record2:
#                self.pg_db_server_locale.delete(g)
#            sqlalchemy.ext.sqlsoup.Session.commit()
#        if record:
#            for l in record:
#                self.pg_db_server_locale.delete(l)
#                sqlalchemy.ext.sqlsoup.Session.delete(l)
#            sqlalchemy.ext.sqlsoup.Session.commit()
#            self.runBatch()

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
    SincroInventario()
