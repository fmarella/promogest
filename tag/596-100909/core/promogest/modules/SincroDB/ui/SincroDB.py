# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import gtk
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


tablesMain = [
            #"azienda",
            ("operazione","denominazione"),
            ("tipo_aliquota_iva","id"),
            ("stato_articolo","id"),
            ("unita_base","id"),
            #"role",
            #"language",
            ("tipo_recapito","denominazione"),
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
            ("persona_giuridica","id"),
            ("fornitore","id"),
#
            ("sconto" ,"id"),
            ("categoria_cliente","id"),
            ("codice_a_barre_articolo","id"),

            #("cart","id"),
            ("articolo_associato","id"),
            #("access","id"),
            ("listino","id"),
            ("listino_magazzino","id_listino"),
            ("listino_categoria_cliente","id_listino"),
#
            ("listino_articolo","id_listino"),
            #("feed","id"),
            ("fornitura","id"),
            ("sconto_fornitura","id"),
            #("inventario","id"),
            ("listino_complesso_listino","id_listino"),
            ("listino_complesso_articolo_prevalente","id_articolo"),
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
    """ Finestra di gestione esdportazione variazioni Database """
    def __init__(self,conf=None, batch=False, schema=None, fileconf=None):
        GladeWidget.__init__(self, 'sincro_dialog',
                        fileName='sincro_dialog.glade')
        self.placeWindow(self.getTopLevel())
        if batch:
            print " MI ACCINGO A CARICARE IL FILE configure dalla cartella '%s' ed usare lo schema '%s'" %(fileconf, schema)
            Environment.conf = conf
            Environment.params["schema"] = schema
            self.batch = batch


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
        print ">>>> CONNESSO AL DB REMOTO : %s IP: %s PORTA: %s SCHEMA %s <<<<< " %(database_remoto, host_remoto,port_remoto,Environment.params["schema"])

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
        print ">>>> CONNESSO AL DB LOCALE : %s IP: %s PORTA: %s SCHEMA %s <<<<< " %(database_locale, host_locale,port_locale,Environment.params["schema"])
        #self.sessionLocale.autocommit

    def daosMain(self, tables=None):
        """
        Crea le liste delle query ciclando nelle tabelle
        """
        for dg in tables:
            self.table_label.set_text(str(dg[0]).upper())
            self.avanzamento_pgbar.pulse()
            exec ("remote=self.pg_db_server_main_remote.%s.order_by((self.pg_db_server_main_remote.%s.%s).asc()).all()") %(dg[0],dg[0],dg[1])
            exec ("locale=self.pg_db_server_main_locale.%s.order_by((self.pg_db_server_main_locale.%s.%s).asc()).all()") %(dg[0],dg[0],dg[1])
            print "DAAOOOO", dg[0]
            self.logica(remote=remote, locale=locale, dao=dg[0], all=True)
        print "<<<<<<<< FINITO CON LO SCHEMA PRINCIPALE >>>>>>>>", datetime.datetime.now()


    def daosScheme(self, tables=None):
        """
        Crea le liste delle query ciclando nelle tabelle
        """
        for dg in tables:
            self.table_label.set_text(str(dg[0]).upper())
            self.avanzamento_pgbar.pulse()
            print "TABELLA:", dg[0]
            conteggia = self.pg_db_server_remote.entity(dg[0]).count() # serve per poter affettare le select
            print "CONTEGGIA:", conteggia
            blocSize = int(Environment.conf.SincroDB.offset)
            #blocSize = 500
            if conteggia >= blocSize:
                blocchi = abs(conteggia/blocSize)
                for j in range(0,blocchi+1):
                    self.avanzamento_pgbar.pulse()
                    offset = j*blocSize
                    print "OFFSET", offset , datetime.datetime.now(), "TABELLA", dg[0]
                    exec ("remote=self.pg_db_server_remote.%s.order_by(self.pg_db_server_remote.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                    exec ("locale=self.pg_db_server_locale.%s.order_by(self.pg_db_server_locale.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                    self.logica(remote=remote, locale=locale,dao=dg[0], all=True)
            elif conteggia < blocSize:
                exec ("remote=self.pg_db_server_remote.%s.order_by(self.pg_db_server_remote.%s.%s).all()") %(dg[0],dg[0],dg[1])
                exec ("locale=self.pg_db_server_locale.%s.order_by(self.pg_db_server_locale.%s.%s).all()") %(dg[0],dg[0],dg[1])
                self.logica(remote=remote, locale=locale,dao=dg[0], all=True)
        print "<<<<<<<< FINITO CON LO SCHEMA AZIENDA >>>>>>>>",
        print "<<<<<<< INIZIATO :", self.tempo_inizio, " FINITO:", datetime.datetime.now() , ">>>>>>>>>>>>>"
        self.run =False
        gobject.source_remove(self.timer)
        self.timer = 0
        self.avanzamento_pgbar.destroy()
        self.table_label.set_text("SINCRONIZZAZIONE TERMINATA CON SUCCESSO")


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
                print "cancello",  g
                sqlalchemy.ext.sqlsoup.Session.commit()
        if record:
            for l in record:
                self.pg_db_server_locale.delete(l)
                print "cancello",  l
            sqlalchemy.ext.sqlsoup.Session.commit()
        if table in ["operazione","tipo_aliquota_iva","stato_articolo","unita_base",
            "tipo_recapito","denominazione"]:
            self.daosMain(tables=tablesMain)
        else:
            self.daosScheme(tables=tablesSchemeArticolo)

    def logica(self,remote=None, locale=None,dao=None,all=False):
        """ cicla le righe della tabella e decide cosa fare """
        if dao in ["operazione","tipo_aliquota_iva","stato_articolo","unita_base",
                    "tipo_recapito","denominazione"]:
            soupLocale = self.pg_db_server_main_locale
        else:
            soupLocale = self.pg_db_server_locale
        deleteRow=False
        if not remote and not locale:
            return False
        #try:
        if list(remote) != list(locale):
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
                            print "QUESTA È LA RIGA DIVERSA NELLA TABELLA ", str(remote[i]._table).split(".")[1], "Operazione UPDATE"
                            self.fixToTable(soupLocale=soupLocale,
                            row=remote[i],
                            rowLocale=locale[i],
                            op="UPDATE",
                            dao=str(remote[i]._table).split(".")[1],
                            save=True)
                    except:
                        print "QUESTA È LA RIGA DIVERSA NELLA TABELLA ", str(remote[i]._table).split(".")[1], "Operazione UPDATE"
                        self.fixToTable(soupLocale=soupLocale,
                                        row=remote[i],
                                        rowLocale=locale[i],
                                        op="UPDATE",
                                        dao=str(remote[i]._table).split(".")[1],
                                        save=True)
                else:
                    print "QUESTA È LA RIGA DA AGGIUNGERE NELLA TABELLA ", str(remote[i]._table).split(".")[1], "Operazione INSERT"
                    #print " RIGA REMOTE", remote[i]
                    self.fixToTable(soupLocale=soupLocale,
                                    row=remote[i],
                                    op="INSERT",
                                    dao=str(remote[i]._table).split(".")[1],
                                    save=False)
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

    def fixToTable(self, soup =None,soupLocale=None, op=None, row=None,rowLocale=None, dao=None, save=False):
        """
        rimanda alla gestione delle singole tabelle con le operazioni da fare
        """
        soupLocale.clear()
        if dao in ["operazione","tipo_aliquota_iva","stato_articolo","unita_base",
                    "tipo_recapito","denominazione"]:
            soupLocale = self.pg_db_server_main_locale
        else:
            soupLocale = self.pg_db_server_locale
        if op =="DELETE":
            sqlalchemy.ext.sqlsoup.Session.delete(rowLocale)
            #soupLocale.delete(rowLocale)
        elif op == "INSERT":
            #rowlocale = soupLocale.entity("elisir."+dao).insert()
            #print "SOUPPPPPPPPPPPPPPPPPPP", soupLocale
            exec ("rowLocale = soupLocale.%s.insert()" ) %dao
            for i in rowLocale.c:
                t = str(i).split(".")[1] #mi serve solo il nome tabella
                setattr(rowLocale, t, getattr(row, t))
            sqlalchemy.ext.sqlsoup.Session.add(rowLocale)
            #soupLocale.add(rowLocale)
        elif op == "UPDATE":
            for i in rowLocale.c:
                t = str(i).split(".")[1] #mi serve solo il nome colonna
                setattr(rowLocale, t, getattr(row, t))
            print rowLocale
            sqlalchemy.ext.sqlsoup.Session.add(rowLocale)
        try:
            sqlalchemy.ext.sqlsoup.Session.commit()
        except Exception,e :
            print "ERRORE",e # e.args, "FFFF", e.instance ,"MMM",  e.message, "ORIG", e.orig , "PRA", type(e.params), "STA", e.statement, e.params["codice"]
            sqlalchemy.ext.sqlsoup.Session.rollback()
            self.azzeraTable(table=dao)

    def rimuoviRecord(self, soupLocale=None, dao=None, row=None, codice=None):
        record = None
        try:
            exec ("record = self.pg_db_server_locale.%s.get(rowLocale.id)") %dao
        except:
            print "RECORD PER ID NON ESISTENTE"
        if record:
            soupLocale.delete(record)
            sqlalchemy.ext.sqlsoup.Session.commit()
            self.daosScheme(tables=tablesSchemeArticolo)
            #self.fixToTable(soup=soup,soupLocale=soupLocale, op=op,rowLocale=rowLocale, dao=dao, row=row, all=all)
        if dao=="articolo":
            record=self.pg_db_server_locale.entity(dao).all()
            #exec ("record = self.pg_db_server_locale.%s.all()") %dao
            if record:
                #print "ECCOLOOOOOOOOOOOOOOOOOOOOOOO", record[0].id
                for l in record:
                    self.pg_db_server_locale.delete(l)
                    #print "cancello",  l
                sqlalchemy.ext.sqlsoup.Session.commit()
                self.daosScheme(tables=tablesSchemeArticolo)

        elif dao=="listino_articolo":
            exec ("record = self.pg_db_server_locale.%s.filter_by(id_listino=row.id_listino, id_articolo=row.id_articolo)") %dao
            if record:
                print "ECCOLOOOOOOOOOOOOOOOOOOOOOOO", record[0].id_articolo
                self.pg_db_server_locale.delete(record[0])
                sqlalchemy.ext.sqlsoup.Session.commit()
                self.daosScheme(tables=tablesSchemeArticolo)
                #self.fixToTable(soup=soup,soupLocale=soupLocale, op=op,rowLocale=rowLocale, dao=dao, row=row, all=all)
        elif dao=="listino_complesso_listino":
            exec ("record = self.pg_db_server_locale.%s.filter_by(id_listino_complesso=row.id_listino_complesso, id_listino=row.id_listino)") %dao
            if record:
                print "ECCOLOOOOOOOOOOOOOOOOOOOOOOO", record
                self.pg_db_server_locale.delete(record[0])
                sqlalchemy.ext.sqlsoup.Session.commit()
                self.daosScheme(tables=tablesSchemeArticolo)

                #self.fixToTable(soup=soup,soupLocale=soupLocale, op=op,rowLocale=rowLocale, dao=dao, row=row, all=all)

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
        #if self.magazzini_togglebutton.get_active():
            #self.daosScheme(tables=tablesSchemeDocumenti)
        #print "MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.run =False
        gobject.source_remove(self.timer)
        self.timer = 0
        #msg = ('Aggiornamento effettuato')
        #dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        #gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
        #response = dialog.run()
        #dialog.destroy()

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

#try:
    #command = "SELECT setval( '%s',(SELECT max(id)+1 FROM %s));" %(schemadest+".caratteri_stampa_id_seq",schemadest +".caratterie_stampa")
    #session.execute(text(command))
#except:
    #print "ERRORE carattere_stampa_id_seq"
if __name__ == '__main__':
    # Import Psyco if available
    import Envir
        #BigBang()
