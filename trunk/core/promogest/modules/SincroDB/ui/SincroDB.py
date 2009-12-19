# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>
import sys
import gobject
import datetime
import threading
import sqlalchemy
#from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.sqlsoup import SqlSoup
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from tabelle_to_sincro import tablesMain, tablesSchemeArticolo,\
                                tablesSchemeAnagrafiche,\
                                tablesSchemePromemoria,\
                                tablesSchemeDocumenti

#avanzamento_pgbar
# Update the value of the progress bar so that we get
# some movement

def progress_timeout(pbobj):
    if pbobj.run:
        pbobj.avanzamento_pgbar.set_text('Sincronizzazione dei DB')
        pbobj.avanzamento_pgbar.pulse()
        #if pbobj.th.isAlive():
            #print "IL SINCRO PROCEDE"
    #else:
        # Calculate the value of the progress bar using the
        # value range set in the adjustment object
        #new_val = pbobj.avanzamento_pgbar.get_fraction() + 0.01
        #if new_val > 1.0:
            #new_val = 0.0
        # Set the new value
        #pbobj.avanzamento_pgbar.set_fraction(new_val)

    # As this is a timeout function, return TRUE so that it
    # continues to get called
        return True
    else:
        return False


class SincroDB(GladeWidget):
    """ Finestra di gestione esdportazione variazioni Database
    """

    def __init__(self, conf=None, batch=False, schema=None, fileconf=None):
        GladeWidget.__init__(self, 'sincro_dialog',
                        fileName='sincro_dialog.glade')
        self.placeWindow(self.getTopLevel())
        self.batch = batch
        if batch:
            print " MI ACCINGO A CARICARE IL FILE configure dalla cartella '%s' ed usare lo schema '%s'" %(fileconf, schema)
            Environment.conf = conf
            Environment.params["schema"] = schema
            #self.batch = batch

    def on_tuttecose_checkbutton_toggled(self,toggled):
        """ check delle anag da esportare ...le seleziona tutte """
        if self.tuttecose_checkbutton.get_active():
            self.articoli_togglebutton.set_active(True)
            self.clienti_togglebutton.set_active(True)
            self.parametri_togglebutton.set_active(True)
            self.magazzini_togglebutton.set_active(True)
        else:
            self.articoli_togglebutton.set_active(False)
            self.clienti_togglebutton.set_active(False)
            self.parametri_togglebutton.set_active(False)
            self.magazzini_togglebutton.set_active(False)

    def connectDbRemote(self):
        """ effettua la connessione al DB remoto """
        mainschema_remoto = Environment.conf.SincroDB.mainschema_remoto
        user_remoto = Environment.conf.SincroDB.user_remoto
        password_remoto = Environment.conf.SincroDB.password_remoto
        host_remoto = Environment.conf.SincroDB.host_remoto
        port_remoto = Environment.conf.SincroDB.port_remoto
        database_remoto = Environment.conf.SincroDB.database_remoto

        engine = create_engine('postgres:'+'//'
                                +user_remoto+':'
                                + password_remoto+ '@'
                                + host_remoto + ':'
                                + port_remoto + '/'
                                + database_remoto,
                                encoding='utf-8',
                                convert_unicode=True )
        tipo_eng = engine.name
        engine.echo = False
        self.metaRemote = MetaData(engine)
        self.pg_db_server_remote = SqlSoup(self.metaRemote)
        self.pg_db_server_remote.schema = Environment.params["schema"]
        self.pg_db_server_main_remote = SqlSoup(self.metaRemote)
        self.pg_db_server_main_remote.schema = mainschema_remoto
        SessionRemote = scoped_session(sessionmaker(bind=engine))
        self.sessionRemote = SessionRemote()
        print ">>>> CONNESSO AL DB REMOTO : %s IP: %s PORTA: %s SCHEMA %s <<<<< " %(database_remoto, host_remoto, port_remoto, Environment.params["schema"])

    def connectDbLocale(self):
        mainschema_locale = Environment.conf.SincroDB.mainschema_locale
        user_locale = Environment.conf.SincroDB.user_locale
        password_locale = Environment.conf.SincroDB.password_locale
        host_locale = Environment.conf.SincroDB.host_locale
        port_locale = Environment.conf.SincroDB.port_locale
        database_locale = Environment.conf.SincroDB.database_locale

        engineLocale = create_engine('postgres:'+'//'
                                        +user_locale+':'
                                        + password_locale+ '@'
                                        + host_locale + ':'
                                        + port_locale + '/'
                                        + database_locale,
                                        encoding='utf-8',
                                        convert_unicode=True )
        tipo_eng = engineLocale.name
        engineLocale.echo = False
        self.metaLocale = MetaData(engineLocale)
        self.pg_db_server_locale = SqlSoup(self.metaLocale)
        self.pg_db_server_locale.schema = Environment.params["schema"]
        self.pg_db_server_main_locale = SqlSoup(self.metaLocale)
        self.pg_db_server_main_locale.schema = mainschema_locale
        SessionLocale = scoped_session(sessionmaker(bind=engineLocale))
        self.engineLocale = engineLocale
        self.sessionLocale = SessionLocale()
        print ">>>> CONNESSO AL DB LOCALE : %s IP: %s PORTA: %s SCHEMA %s <<<<< " %(database_locale, host_locale, port_locale, Environment.params["schema"])

    def daosMain(self, tables=None):
        """ Crea le liste delle query ciclando nelle tabelle """
        for dg in tables:
            self.table_label.set_text(str(dg[0]).upper())
            self.avanzamento_pgbar.pulse()
            exec ("remote=self.pg_db_server_main_remote.%s.order_by((self.pg_db_server_main_remote.%s.%s).asc()).all()") %(dg[0], dg[0], dg[1])
            exec ("locale=self.pg_db_server_main_locale.%s.order_by((self.pg_db_server_main_locale.%s.%s).asc()).all()") %(dg[0], dg[0], dg[1])
            print "QUESTO E' IL DAO DELLE TABELLE MAIN IN LAVORAZIONE ...", dg[0]
            self.logica(remote=remote, locale=locale, dao=dg[0], all=True)
        print "<<<<<<<< FINITO CON LO SCHEMA PRINCIPALE >>>>>>>>", datetime.datetime.now()

    def dammiSoupLocale(self, dao):
        soupLocale = None
        if dao in ["operazione","tipo_aliquota_iva","stato_articolo","unita_base",
            "tipo_recapito","denominazione"]:
            soupLocale = self.pg_db_server_main_locale
        else:
            soupLocale = self.pg_db_server_locale
        return soupLocale

    def gestisciListinoArticolo(self, dg=None):
        blocSize = int(Environment.conf.SincroDB.offset)
        listini=self.pg_db_server_remote.listino.order_by(self.pg_db_server_remote.listino.id).all()
        for li in listini:
            self.avanzamento_pgbar.pulse()
            conteggia = self.pg_db_server_remote.entity("listino_articolo").filter_by(id_listino=li.id).count()
            print "GLI ARTICOLI SONO:",conteggia, "ID LISTINO", li.id
            if conteggia >= blocSize:
                blocchi = abs(conteggia/blocSize)
                for j in range(0,blocchi+1):
                    self.avanzamento_pgbar.pulse()
                    offset = j*blocSize
                    print "SPEZZETTO IL LISTINO OFFSET", offset, datetime.datetime.now(), "TABELLA", dg[0]
                    remote=self.pg_db_server_remote.listino_articolo.\
                                filter_by(id_listino=li.id).\
                                order_by(self.pg_db_server_remote.listino_articolo.id_articolo,
                                        self.pg_db_server_remote.listino_articolo.data_listino_articolo).\
                                limit(blocSize).\
                                offset(offset).all()
                    locale=self.pg_db_server_locale.\
                            listino_articolo.\
                            filter_by(id_listino=li.id).\
                            order_by(self.pg_db_server_remote.listino_articolo.id_articolo,
                                    self.pg_db_server_locale.listino_articolo.data_listino_articolo).\
                            limit(blocSize).\
                            offset(offset).all()
                    self.logica(remote=remote, locale=locale,dao=dg[0], all=True, offset=None)
            elif conteggia < blocSize:
                remote=self.pg_db_server_remote.listino_articolo.filter_by(id_listino=li.id).order_by(self.pg_db_server_remote.listino_articolo.id_articolo,self.pg_db_server_remote.listino_articolo.data_listino_articolo).all()
                locale=self.pg_db_server_locale.listino_articolo.filter_by(id_listino=li.id).order_by(self.pg_db_server_remote.listino_articolo.id_articolo,self.pg_db_server_locale.listino_articolo.data_listino_articolo).all()
                self.logica(remote=remote, locale=locale,dao=dg[0], all=True)
        return True

    def daosScheme(self, tables=None, offsett=None):
        """ Crea le liste delle query ciclando nelle tabelle """
        blocSize = int(Environment.conf.SincroDB.offset)
        #blocSize = 500
        for dg in tables:
            self.table_label.set_text(str(dg[0]).upper())
            #listino lo gestisco facendo select per id listino così gestisco meglio i nuovi record
            if dg[0] =="listino_articolo":
                self.gestisciListinoArticolo(dg)
            else:
                self.avanzamento_pgbar.pulse()
                print "TABELLA IN LAVORAZIONE :", dg[0]
                conteggia = self.pg_db_server_remote.entity(dg[0]).count() # serve per poter affettare le select
                print "NUMERO DEI RECORD PRESENTI:", conteggia
                if conteggia >= blocSize:
                    blocchi = abs(conteggia/blocSize)
                    for j in range(0,blocchi+1):
                        self.avanzamento_pgbar.pulse()
                        offset = j*blocSize
                        print "OFFSET", offset , datetime.datetime.now(), "TABELLA", dg[0]
                        exec ("remote=self.pg_db_server_remote.%s.order_by(self.pg_db_server_remote.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                        exec ("locale=self.pg_db_server_locale.%s.order_by(self.pg_db_server_locale.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                        self.logica(remote=remote, locale=locale,dao=dg[0], all=True, offset=offset)
                elif conteggia < blocSize: # SI FA LA QUERY IN UN UNICI BOCCONE
                    exec ("remote=self.pg_db_server_remote.%s.order_by(self.pg_db_server_remote.%s.%s).all()") %(dg[0],dg[0],dg[1])
                    exec ("locale=self.pg_db_server_locale.%s.order_by(self.pg_db_server_locale.%s.%s).all()") %(dg[0],dg[0],dg[1])
                    self.logica(remote=remote, locale=locale,dao=dg[0], all=True)
        print "<<<<<<<< FINITO CON LO SCHEMA AZIENDA >>>>>>>>"
        print "<<<<<<< INIZIATO :", self.tempo_inizio, " FINITO:", datetime.datetime.now() , ">>>>>>>>>>>>>"
        self.run =False
        if not self.batch:
            gobject.source_remove(self.timer)
            self.timer = 0
            self.avanzamento_pgbar.destroy()
            self.table_label.set_text("SINCRONIZZAZIONE TERMINATA CON SUCCESSO")
        else:
            print "SINCRONIZZAZIONE TERMINATA CON SUCCESSO"

    def logica(self,remote=None, locale=None,dao=None,all=False,offset=None):
        """ cicla le righe della tabella e decide cosa fare
        """
        soupLocale = self.dammiSoupLocale(dao)
        deleteRow=False
        if not remote and not locale:
            return False

        if str(list(remote)) != str(list(locale)):
            if len(remote) == len(locale):
                print "STESSO NUMERO DI RECORD", len(remote)
            elif len(remote) > len(locale):
                print "IL DB REMOTO CONTIENE PIU' RECORD", len(remote), "vs", len(locale)
            else:
                print "IL DB LOCALE CONTIENE PIU' RECORD", len(remote), "vs", len(locale)
                deleteRow=True
            for i in range(0,(len(remote))):
                if i <= (len(locale)-1):
                    try:
                        if  remote[i] != locale[i]:
                            print "PROCEDO CON UN UPDATE", str(remote[i]._table).split(".")[1]
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
                    if tabe=="listino_articolo":
                        print "ERRORE NEI LISTINI", e
                        sqlalchemy.ext.sqlsoup.Session.rollback()
                        record_id1 = self.pg_db_server_locale.listino_articolo.filter_by(id_listino=remote[i].id_listino).all()
#                        print "RECOOOOOOOOOOOOOOOOORD", record_id1
                        if record_id1:
                            for r in record_id1:
                                sqlalchemy.ext.sqlsoup.Session.delete(r)
                                sqlalchemy.ext.sqlsoup.Session.commit()
                            print "QUIIII"
                            self.daosScheme(tables=["listino_articolo"])
                    else:
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
        elif op == "UPDATE":
            try:
                for i in rowLocale.c:
                    #mi serve solo il nome colonna
                    t = str(i).split(".")[1]
                    setattr(rowLocale, t, getattr(row, t))
                sqlalchemy.ext.sqlsoup.Session.add(rowLocale)
                if dao == "articolo":
                    sqlalchemy.ext.sqlsoup.Session.commit()
            except Exception,e :
                print "ERRORE",e
                print "QUALCOSA NELL'UPDATE NON È ANDATO BENE ....VERIFICHIAMO"
                sqlalchemy.ext.sqlsoup.Session.rollback()
                print "FATTO IL ROOLBACK"
                print
                print "RIGA LOCALE", rowLocale
                print
                print "RIGA REMOTA", row
                print
                if dao == "articolo":
                    try:
                        record_codice = self.pg_db_server_locale.articolo.filter_by(codice=row.codice).one()
                        if record_codice:
                            print "CODICE DUPLICATO ...DEVO INTERVENIRE MODIFICANDO IL CODICE E RILANCIANDO "
                            record_codice.codice = str(record_codice.codice)+"_ex_id_"+str(record_codice.id)
                            sqlalchemy.ext.sqlsoup.Session.add(record_codice)
                            sqlalchemy.ext.sqlsoup.Session.commit()
                            for i in rowLocale.c:
                                t = str(i).split(".")[1] #mi serve solo il nome colonna
                                setattr(rowLocale, t, getattr(row, t))
                            sqlalchemy.ext.sqlsoup.Session.add(rowLocale)
                            sqlalchemy.ext.sqlsoup.Session.commit()
                            return
                    except:
                        pass
                    try:
                        print "SONO NELL try dentro l'ecept che gestisce la particolarità articolo"
                        sqlalchemy.ext.sqlsoup.Session.rollback()
                        record_id1 = self.pg_db_server_locale.articolo.get(row.id)
                        record_id2 = self.pg_db_server_locale.articolo.get(rowLocale.id)
                        sqlalchemy.ext.sqlsoup.Session.delete(record_id2)
                        sqlalchemy.ext.sqlsoup.Session.delete(rowLocale)
                        sqlalchemy.ext.sqlsoup.Session.commit()
                        return
                    except:
                        print "SECONTO TRY INUTILE"
                        pass

                    try:
                        sqlalchemy.ext.sqlsoup.Session.rollback()
                        riga_scontr = self.pg_db_server_locale.riga_scontrino.filter_by(id_articolo=rowLocale.id).one()
                        riga_scontr.id_articolo = row.id
                        sqlalchemy.ext.sqlsoup.Session.add(riga_scontr)
                        sqlalchemy.ext.sqlsoup.Session.commit()
                        sqlalchemy.ext.sqlsoup.Session.delete(rowLocale)
                        sqlalchemy.ext.sqlsoup.Session.commit()
                        return
                    except:
                        print "terzo try"
                    if self.batch:
                        self.runBatch()
                    else:
                        self.test()
#                else:
#                    self.azzeraTable(table=dao)

    def azzeraTable(self, table=None):
        if table in ["operazione","tipo_aliquota_iva","stato_articolo","unita_base",
                    "tipo_recapito","denominazione"]:
            record = self.pg_db_server_main_locale.entity(table).all()
        else:
            record=self.pg_db_server_locale.entity(table).all()
        if table =="listino":
            record2=self.pg_db_server_locale.entity("listino_magazzino").all()
            for g in record2:
                self.pg_db_server_locale.delete(g)
            sqlalchemy.ext.sqlsoup.Session.commit()
        if record:
            for l in record:
                self.pg_db_server_locale.delete(l)
                sqlalchemy.ext.sqlsoup.Session.delete(l)
            #print "cancello",  l
            sqlalchemy.ext.sqlsoup.Session.commit()
#            sqlalchemy.ext.sqlsoup.Session.flush()

        if table in ["operazione","tipo_aliquota_iva","stato_articolo","unita_base",
            "tipo_recapito","denominazione"]:
            self.daosMain(tables=tablesMain)
        else:
            if self.batch:
                self.runBatch()
            else:
                self.test()

    def test(self):
        self.connectDbRemote()
        self.connectDbLocale()
        self.tempo_inizio = datetime.datetime.now()
        print "INIZIO sincro",datetime.datetime.now()
        self.daosMain(tables=tablesMain)
        if self.tuttecose_checkbutton.get_active() or self.batch:
            self.daosScheme(tables=tablesSchemeArticolo)
            self.daosScheme(tables=tablesSchemeAnagrafiche)
            self.daosScheme(tables= tablesSchemePromemoria)
            #self.daosScheme(tables=tablesSchemeDocumenti)
            return
        if self.articoli_togglebutton.get_active():
            self.daosScheme(tables=tablesSchemeArticolo)
        if self.clienti_togglebutton.get_active():
            self.daosScheme(tables=tablesSchemeAnagrafiche)
        if self.parametri_togglebutton.get_active():
            self.daosScheme(tables= tablesSchemePromemoria)
        self.run =False
        gobject.source_remove(self.timer)
        self.timer = 0

    def runBatch(self):
        sqlalchemy.ext.sqlsoup.Session.expunge_all()

        self.connectDbRemote()
        self.connectDbLocale()
        self.tempo_inizio = datetime.datetime.now()
        print "INIZIO sincro",datetime.datetime.now()
        self.daosMain(tables=tablesMain)
        self.daosScheme(tables=tablesSchemeArticolo)
        self.daosScheme(tables=tablesSchemeAnagrafiche)
        self.daosScheme(tables= tablesSchemePromemoria)
        sqlalchemy.ext.sqlsoup.Session.expunge_all()
        sys.exit()

    def on_run_button_clicked(self, button=None):
        self.run = True
        self.timer = gobject.timeout_add(80,progress_timeout, self)
        #gobject.idle_add(self.test())
        self.th = threading.Thread(target=self.test)
        self.th.start()
        #thread.join(1.3)
        #self.test()

    def on_close_button_clicked(self, button):
        self.destroy()

#if __name__ == '__main__':
#    import Envir
#        #BigBang()
