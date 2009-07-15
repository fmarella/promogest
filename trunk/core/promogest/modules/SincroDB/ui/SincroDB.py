# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import gtk
import gobject
import datetime
import sqlalchemy
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.GladeWidget import GladeWidget
from sqlalchemy.ext.sqlsoup import SqlSoup

tablesMain = [
            #"azienda",
            "operazione",
            "tipo_aliquota_iva",
            "stato_articolo",
            "unita_base",
            #"role",
            "language",
            "tipo_recapito",
            #"user",
            #"app_log",
            #"action",
            #"roleaction"
]

tablesSchemeArticolo = [
            ("magazzino","id"),
            #("setting","key"),
            ("aliquota_iva","id"),
            ("categoria_articolo","id"),
            ("famiglia_articolo","id"),#########
            ("image","id"),
            ("imballaggio","id"),
            ("articolo","id"),
            ("multiplo","id"),
            ("pagamento","id"),
            ("fornitore","id"),
            ("persona_giuridica","id"),
            ("sconto" ,"id"),
            ("categoria_cliente","id"),
            ("codice_a_barre_articolo","id"),

            #("cart","id"),
            ("articolo_associato","id"),
            #("access","id"),
            ("listino","id"),
            ("listino_magazzino","id_listino"),
            ("listino_categoria_cliente","id_listino"),

            ("listino_articolo","id_listino"),
            #("feed","id"),
            ("fornitura","id"),
            ("sconto_fornitura","id"),
            #("inventario","id"),
            #("listino_complesso_articolo_prevalente","id_articolo"),
            #("listino_complesso_listino","id_listino"),

            ("sconti_vendita_dettaglio","id"),
            ("sconti_vendita_ingrosso","id"),
            #("spesa","id"),
            ("stoccaggio","id")
]
tablesSchemeAnagrafiche = [
            ("persona_giuridica","id"),
            ("banca","id"),
            ("cliente","id"),
            ("categoria_fornitore","id"),
            ("destinazione_merce","id"),
            ("vettore","id"),
            ("agente","id"),
            ("cliente_categoria_cliente","id_cliente"),
            ("contatto","id"),
            ("contatto_cliente","id"),
            ("recapito","id"),
            ("categoria_contatto","id"),
            ("contatto_categoria_contatto","id_contatto"),
            ("contatto_fornitore","id"),
            ("contatto_magazzino","id"),
            ("contatto_azienda","id"),
]

tablesSchemePromemoria = [
            ("promemoria","id"),

]

tablesSchemeDocumenti = [
            ("testata_documento","id"),
            ("testata_movimento","id"),
            ("riga","id"),
            ("riga_movimento","id"),
            ("sconto_riga_movimento","id"),
            #("inventario","id"),
            ("riga_documento","id"),
            ("sconto_riga_documento","id"),
            ("sconto_testata_documento","id"),
            ("testata_documento_scadenza","id"),
            ("informazioni_contabili_documento","id"),
]

class SincroDB(GladeWidget):
    """ Finestra di gestione esdportazione variazioni Database """
    def __init__(self):
        GladeWidget.__init__(self, 'sincro_dialog',
                        fileName='sincro_dialog.glade')
        self.placeWindow(self.getTopLevel())

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
        mainschema_remoto = Environment.conf.SincroDB.mainschema_remoto
        user_remoto = Environment.conf.SincroDB.user_remoto
        password_remoto = Environment.conf.SincroDB.password_remoto
        host_remoto = Environment.conf.SincroDB.host_remoto
        port_remoto = Environment.conf.SincroDB.port_remoto
        database_remoto = Environment.conf.SincroDB.database_remoto

        #azienda=conf.Database.azienda
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
            #Session = sessionmaker(bind=engine)
        SessionRemote = scoped_session(sessionmaker(bind=engine))
        self.sessionRemote = SessionRemote()

    def connectDbLocale(self):
        mainschema_locale = Environment.conf.SincroDB.mainschema_locale
        user_locale = Environment.conf.SincroDB.user_locale
        password_locale = Environment.conf.SincroDB.password_locale
        host_locale = Environment.conf.SincroDB.host_locale
        port_locale = Environment.conf.SincroDB.port_locale
        database_locale = Environment.conf.SincroDB.database_locale

        #azienda=conf.Database.azienda
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
            #Session = sessionmaker(bind=engine)
        SessionLocale = scoped_session(sessionmaker(bind=engineLocale))
        self.engineLocale = engineLocale
        self.sessionLocale = SessionLocale()
        #self.sessionLocale.autocommit

    def daosMain(self, tables=None):
        """
        Crea le liste delle query ciclando nelle tabelle
        """
        for dg in tables:
            #exec ("remote=self.pg_db_server_main_remote.%s.all()") %dg
            remote = self.pg_db_server_main_remote.entity(dg).all()
            if len(remote)!=1:
                remote.sort()
            #exec ("locale=self.pg_db_server_main_locale.%s.all()") %dg
            locale = self.pg_db_server_main_locale.entity(dg).all()
            if len(locale)!=1:
                locale.sort()
            self.logica(remote=remote, locale=locale, all=True)
        print "<<<<<<<< FINITO CON LO SCHEMA PRINCIPALE >>>>>>>>", datetime.datetime.now()


    def daosScheme(self, tables=None):
        """
        Crea le liste delle query ciclando nelle tabelle
        """
        for dg in tables:
            print "TABELLA:", dg
            conteggia = self.pg_db_server_remote.entity(dg[0]).count() # serve per poter affettare le select
            conteggialocale = self.pg_db_server_remote.entity(dg[0]).count()
            #exec ( "conteggia = self.pg_db_server_remote.%s.count()")  %(dg[0])
            #exec ( "conteggialocale = self.pg_db_server_locale.%s.count()")  %(dg[0])
            print "CONTEGGIA:", conteggia, conteggialocale
            blocSize = 500
            if conteggia >= blocSize:
                blocchi = abs(conteggia/blocSize)
                for j in range(0,blocchi+1):
                    offset = j*blocSize
                    print "OFFFFFSET", offset , datetime.datetime.now()
                    #remote=self.pg_db_server_remote.entity(dg[0]).limit(blocSize).offset(offset).all()
                    #locale=self.pg_db_server_locale.entity(dg[0]).limit(blocSize).offset(offset).all()
                    exec ("remote=self.pg_db_server_remote.%s.order_by(self.pg_db_server_remote.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                    exec ("locale=self.pg_db_server_locale.%s.order_by(self.pg_db_server_locale.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                    self.logica(remote=remote, locale=locale, all=True)
            elif conteggia < blocSize:
                #remote=self.pg_db_server_remote.entity(dg[0]).all()
                #locale=self.pg_db_server_locale.entity(dg[0]).all()
                exec ("remote=self.pg_db_server_remote.%s.order_by(self.pg_db_server_remote.%s.%s).all()") %(dg[0],dg[0],dg[1])
                exec ("locale=self.pg_db_server_locale.%s.order_by(self.pg_db_server_locale.%s.%s).all()") %(dg[0],dg[0],dg[1])
                self.logica(remote=remote, locale=locale, all=True)
        print "<<<<<<<< FINITO CON LO SCHEMA AZIENDA >>>>>>>>", datetime.datetime.now()


    def logica(self,remote=None, locale=None, all=False):
        """ cicla le righe della tabella e decide cosa fare """
        deleteRow=False
        print len(remote) , len(locale)
        if remote != locale:
            if len(remote) == len(locale):
                print "STESSO NUMERO DI RECORD", len(remote)
            elif len(remote) > len(locale):
                print "IL DB REMOTO CONTIENE PIU' RECORD", len(remote), "vs", len(locale)
            else:
                print "IL DB LOCALE CONTIENE PIU' RECORD", len(remote), "vs", len(locale)
                deleteRow=True
            for i in range(0,(len(remote))):
                if str(remote[i]._table).split(".")[1] in tablesMain:
                    soupLocale = self.pg_db_server_main_locale
                else:
                    soupLocale = self.pg_db_server_locale
                if i <= (len(locale)-1):
                    #print "REMOTE", remote[i]
                    #print "LOCALE", locale[i]
                    if  remote[i] != locale[i]:
                        print "QUESTA È LA RIGA DIVERSA NELLA TABELLA ", str(remote[i]._table).split(".")[1], "Operazione UPDATE"
                        print " RIGA REMOTE", remote[i].id
                        print " RIGA LOCALE", locale[i].id
                        self.fixToTable(soupLocale=soupLocale,
                                        row=remote[i],
                                        rowLocale=locale[i],
                                        op="UPDATE",
                                        dao=str(remote[i]._table).split(".")[1],
                                        all=all)
                else:
                    print "QUESTA È LA RIGA DA AGGIUNGERE NELLA TABELLA ", str(remote[i]._table).split(".")[1], "Operazione INSERT"
                    print " RIGA REMOTE", remote[i]
                    self.fixToTable(soupLocale=soupLocale,
                                    row=remote[i],
                                    op="INSERT",
                                    dao=str(remote[i]._table).split(".")[1],
                                    all=all)
            if deleteRow:
                for i in range(len(remote),len(locale)):
                    print "QUESTA È LA RIGA DA rimuovere ", str(locale[i]._table).split(".")[1], "Operazione DELETE"
                    self.fixToTable(soupLocale=soupLocale,
                        #row=locale[i],
                        rowLocale = locale[i],
                        op="DELETE",
                        dao=str(locale[i]._table).split(".")[1],
                        all=all)
        else:
            print "TABELLE UGUALI"

    def fixToTable(self, soup =None,soupLocale=None, op=None, row=None,rowLocale=None, dao=None, all=False):
        """
        rimanda alla gestione delle singole tabelle con le operazioni da fare
        """

        if op =="DELETE":
            soupLocale.delete(rowLocale)
        elif op == "INSERT":
            #rowlocale_ = soupLocale.entity(dao).insert()
            exec ( "rowLocale = soupLocale.%s.insert()" ) %dao
            for i in rowLocale.c:

                t = str(i).split(".")[1] #mi serve solo il nome tabella
                setattr(rowLocale, t, getattr(row, t))
        elif op == "UPDATE":

            for i in rowLocale.c:
                t = str(i).split(".")[1] #mi serve solo il nome tabella

                setattr(rowLocale, t, getattr(row, t))
        try:
            sqlalchemy.ext.sqlsoup.Session.commit()
            sqlalchemy.ext.sqlsoup.Session.flush()
        except Exception,e :
            print "ERRORE", e
            #msg = """ATTENZIONE ERRORE NEL SALVATAGGIO
    #Qui sotto viene riportato l'errore di sistema:
#
    #( normalmente il campo in errore è tra "virgolette")
#
    #%s
#
    #L'errore può venire causato da un campo fondamentale
    #mancante, da un codice già presente, si invita a
    #rincontrollare i campi e riprovare
    #Grazie!
    #""" %e
            #overDialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL
                                                #| gtk.DIALOG_DESTROY_WITH_PARENT,
                                                    #gtk.MESSAGE_ERROR,
                                                    #gtk.BUTTONS_CANCEL, msg)
            #response = overDialog.run()
            #overDialog.destroy()
            sqlalchemy.ext.sqlsoup.Session.rollback()
            #sqlalchemy.ext.sqlsoup.Session.clear()
            #self.connectDbLocale()
            #SessionLocale = scoped_session(sessionmaker(bind=self.engineLocale))
            #self.sessionLocale = SessionLocale()
            #try:
                #exec ("record = self.pg_db_server_locale.%s.get(rowLocale.id)") %dao
            #except:
                #pass
            #print "QUIIIIIIIIIIIIIIIIIIIIIII", record
            #if record:
                #soupLocale.delete(record)
                #sqlalchemy.ext.sqlsoup.Session.commit()
                #self.daosScheme(tables=tablesSchemeArticolo)
                #self.fixToTable(soup=soup,soupLocale=soupLocale, op=op,rowLocale=rowLocale, dao=dao, row=row, all=all)
            #print "UFFFFFFFFFFFFFFFFFFFF", row.codice
            if dao=="articolo":
                exec ("record = self.pg_db_server_locale.%s.filter_by(codice=row.codice)") %dao
                if record:
                    print "ECCOLOOOOOOOOOOOOOOOOOOOOOOO", record[0].id
                    soupLocale.delete(record[0])
                    sqlalchemy.ext.sqlsoup.Session.commit()
                    self.daosScheme(tables=tablesSchemeArticolo)
            elif dao=="listino_articolo":
                exec ("record = self.pg_db_server_locale.%s.filter_by(id_listino=row.id_listino, id_articolo=row.id_articolo)") %dao
                if record:
                    print "ECCOLOOOOOOOOOOOOOOOOOOOOOOO", record[0].id_articolo
                    soupLocale.delete(record[0])
                    sqlalchemy.ext.sqlsoup.Session.commit()
                    #self.daosScheme(tables=tablesSchemeArticolo)
                    self.fixToTable(soup=soup,soupLocale=soupLocale, op=op,rowLocale=rowLocale, dao=dao, row=row, all=all)
            elif dao=="listino_complesso_listino":
                exec ("record = self.pg_db_server_locale.%s.filter_by(id_listino_complesso=row.id_listino_complesso, id_listino=row.id_listino)") %dao
                if record:
                    print "ECCOLOOOOOOOOOOOOOOOOOOOOOOO", record
                    soupLocale.delete(record[0])
                    sqlalchemy.ext.sqlsoup.Session.commit()
                    #self.daosScheme(tables=tablesSchemeArticolo)
                    self.fixToTable(soup=soup,soupLocale=soupLocale, op=op,rowLocale=rowLocale, dao=dao, row=row, all=all)

        return True

    def on_run_button_clicked(self, button):
        self.connectDbRemote()
        self.connectDbLocale()
        print "INIZIO sincro",datetime.datetime.now()
        self.daosMain(tables=tablesMain)
        if self.tuttecose_checkbutton.get_active():
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
        #if self.magazzini_togglebutton.get_active():
            #self.daosScheme(tables=tablesSchemeDocumenti)

    def on_close_button_clicked(self, button):
        self.destroy()

#try:
    #command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".caratteri_stampa_id_seq",schemadest +".caratterie_stampa")
    #session.execute(text(command))
#except:
    #print "ERRORE carattere_stampa_id_seq"
