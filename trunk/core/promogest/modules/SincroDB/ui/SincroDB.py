# -*- coding: utf-8 -*-

#    Copyright (C) 2009, 2010 by Promotux di Francesco Meloni snc - http://www.promotux.it/

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

import random
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
                                tablesSchemeDocumenti,\
                                tablesSchemePromoWear,\
                                tablesMainSchemePromoWear




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

    def __init__(self, conf=None, batch=False, schema=None, fileconf=None, wear= False):
        GladeWidget.__init__(self, 'sincro_dialog',
                        fileName='sincro_dialog.glade')
        self.placeWindow(self.getTopLevel())
        self.batch = batch
        self.wear = wear
        self.promeid = None
        if batch: #versione senza interfaccia grafica
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
        """ effettua la connessione al DB locale """
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
        """ Crea le liste delle query ciclando nelle tabelle principali"""
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
            conteggia_locale = self.pg_db_server_remote.entity("listino_articolo").filter_by(id_listino=li.id).count()
            safer = False
            if conteggia_locale>conteggia:
                safer=True
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
                    print "REMOTEEEE", len(remote), "LOCALEEEEEE", len(locale)
                    if len(locale)>len(remote):
                        print "ATTENZIONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", len(remote), len(locale)
                    self.manageListinoArticoloSafe(remote, locale, safer=safer)
#                    self.logica(remote=remote, locale=locale,dao=dg[0], all=True, offset=None)
            elif conteggia < blocSize:
                remote=self.pg_db_server_remote.listino_articolo.filter_by(id_listino=li.id).order_by(self.pg_db_server_remote.listino_articolo.id_articolo,self.pg_db_server_remote.listino_articolo.data_listino_articolo).all()
                locale=self.pg_db_server_locale.listino_articolo.filter_by(id_listino=li.id).order_by(self.pg_db_server_remote.listino_articolo.id_articolo,self.pg_db_server_locale.listino_articolo.data_listino_articolo).all()
                print "REMOTEEEE", len(remote), "LOCALEEEEEE", len(locale), "NON SPACCHETTATO"
                if len(locale)>len(remote):
                    print "ATTENZIONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", len(remote), len(locale)
                self.manageListinoArticoloSafe(remote, locale, safer=safer)
#                self.logica(remote=remote, locale=locale,dao=dg[0], all=True)
        return True

    def daosScheme(self, tables=None, scarto=0):
        """ Crea le liste delle query ciclando nelle tabelle """
        blocSize = int(Environment.conf.SincroDB.offset)
        #blocSize = 500
        for dg in tables:
            self.table_label.set_text(str(dg[0]).upper())
            #listino lo gestisco facendo select per id listino così gestisco meglio i nuovi record
            if dg[0] =="listino_articolo":
                self.gestisciListinoArticolo(dg)
            else:
#                self.avanzamento_pgbar.pulse()
                print "TABELLA IN LAVORAZIONE :", dg[0]
                conteggia = self.pg_db_server_remote.entity(dg[0]).count() # serve per poter affettare le select
                print "NUMERO DEI RECORD PRESENTI:", conteggia
                if conteggia >= blocSize:
                    blocchi = abs(conteggia/blocSize)
                    for j in range(0,blocchi+1):
                        offset = j*blocSize
                        print "OFFSET", offset , datetime.datetime.now(), "TABELLA", dg[0]
                        exec ("remote=self.pg_db_server_remote.%s.order_by(self.pg_db_server_remote.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                        exec ("locale=self.pg_db_server_locale.%s.order_by(self.pg_db_server_locale.%s.%s).limit(blocSize).offset(offset).all()") %(dg[0],dg[0],dg[1])
                        if str(remote[0]._table).split(".")[1] =="articolo":
                            self.manageArticoloSafe(remote)
                        elif str(remote[0]._table).split(".")[1] =="codice_a_barre_articolo":
                            self.manageCodBarreSafe(remote)
                        elif str(remote[0]._table).split(".")[1] =="fornitura":
                            self.manageFornituraSafe(remote)
                        elif str(remote[0]._table).split(".")[1] =="sconto":
                            self.manageScontoSafe(remote)
                        elif str(remote[0]._table).split(".")[1] =="listino_complesso_listino":
                            self.manageListinoComplessoListinoSafe(remote)
                        elif str(remote[0]._table).split(".")[1] =="stoccaggio":
                            self.manageStoccaggioSafe(remote)
                        elif str(remote[0]._table).split(".")[1] =="sconti_vendita_dettaglio":
                            self.manageScontiVenditaDettaglioSafe(remote)
                        elif str(remote[0]._table).split(".")[1] =="sconti_vendita_ingrosso":
                            self.manageScontiVenditaIngrossoSafe(remote)
                        elif str(remote[0]._table).split(".")[1] =="listino_magazzino":
                            self.manageListinoMagazzinoSafe(remote)
                        else:

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
        diciamo che è la funzione principale
        """
        soupLocale = self.dammiSoupLocale(dao)
        deleteRow=False
        if not remote and not locale:
            return False
        # comparazione tra le query locali e quelle remote.
#        print "VEDIAMO", str(list(remote))
        if str(list(remote)) != str(list(locale)):
            if len(remote) == len(locale):
                print "STESSO NUMERO DI RECORD", len(remote)
            elif len(remote) > len(locale):
                print "IL DB REMOTO CONTIENE PIU' RECORD", len(remote), "vs", len(locale)
            else:
                print "IL DB LOCALE CONTIENE PIU' RECORD", len(remote), "vs", len(locale)
                deleteRow=True
            if 5==3:
                pass
            else:
                for i in range(0,(len(remote))):
                    self.tabe = str(remote[i]._table).split(".")[1]
                    if i <= (len(locale)-1):
    #                    try:
                        # comparo gli elementi con lo stesso indice che è
                        # la cosa più semplice
                        do = False
                        dao_locale_ex = None
    #                    print "LEN LOCALE",i
                        rem_dic = remote[i].__dict__
                        loc_dic = locale[i].__dict__
    #                    print rem_dic, loc_dic
                        for k,v in rem_dic.items():
                            if k != "_sa_instance_state":
                                if rem_dic[k] != loc_dic[k]:
    #                                print "ORAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", rem_dic[k], loc_dic[k]
                                    do = True
                                    tabe = str(remote[i]._table).split(".")[1]
                                    if tabe == "articolo" and k =="denominazione":
                                        dao_locale_ex = locale[i]
                                    elif tabe == "listino_articolo":
                                        dao_locale_ex = locale[i]
                                    break
                        if  do:
                            print "PROCEDO CON UN UPDATE", str(remote[i]._table).split(".")[1]
    #                        print
    #                        print "LOCALE:", locale[i]
    #                        print
    #                        print "REMOTE:", remote[i]
                            self.fixToTable(soupLocale=soupLocale,
                                            rowMaster=remote[i],
                                            rowSlave=locale[i],
                                            op="UPDATE",
                                            dao=str(remote[i]._table).split(".")[1],
                                            save=True,
                                            offset=offset,
                                            dao_locale_ex = dao_locale_ex)
    #                    print " FATTO"
                        do = False
                        continue


                    else:
                        print " ", str(remote[i]._table).split(".")[1], "INSERT", i
                        #print " RIGA REMOTE", remote[i]
                        self.fixToTable(soupLocale=soupLocale,
                                        rowMaster=remote[i],
                                        op="INSERT",
                                        dao=str(remote[i]._table).split(".")[1],
                                        save=False)

            if self.tabe != "articolo":
                try:
                    sqlalchemy.ext.sqlsoup.Session.commit()
                except Exception, e:
                    if self.tabe=="listino_articolo":
                        print "ERRORE NEI LISTINI", e
                        sqlalchemy.ext.sqlsoup.Session.rollback()
                        record_id1 = self.pg_db_server_locale.listino_articolo.filter_by(id_listino=remote[i].id_listino).all()
    #                        print "RECOOOOOOOOOOOOOOOOORD", record_id1
                        if record_id1:
                            for r in record_id1:
                                sqlalchemy.ext.sqlsoup.Session.delete(r)
                            sqlalchemy.ext.sqlsoup.Session.commit()
    #                            print "QUIIII"
                            self.daosScheme(tables=[("listino_articolo","id_listino")])
                    else:
                        print "ERRORE NEL SALVATAGGIO DEI RECORD", e
                        sqlalchemy.ext.sqlsoup.Session.rollback()
                        self.azzeraTable(table=dao)
            if deleteRow and self.tabe !="articolo":
                for i in range(len(remote),len(locale)):
                    print "QUESTA È LA RIGA DA rimuovere ", str(locale[i]._table).split(".")[1], "Operazione DELETE"
                    self.fixToTable(soupLocale=soupLocale,
                                    #row=locale[i],
                                    rowSlave = locale[i],
                                    op="DELETE",
                                    dao=str(locale[i]._table).split(".")[1],
                                    save=True)
        else:
            print "TABELLE o BLOCCHI CON NUM DI RECORD UGUALI"

    def promeListinoArticolo(self, dao_local, dao_locale_ex):
        descr = "\nErrore nella compilazione dei dati listino articolo "
        d1 = self.pg_db_server_locale.articolo.get(dao_local.id_articolo)
        if d1:
            art = d1
            descr = "\nListino articolo %s - %s è cambiato da %s a %s " %(art.codice, art.denominazione,dao_locale_ex.prezzo_dettaglio, dao_local.prezzo_dettaglio)
        return descr


    def promemoriaInserAlert(self, dao_local, dao_locale_ex):
#        soupLocale = self.dammiSoupLocale(dao)

        tabe = str(dao_local._table).split(".")[1]
        if  tabe == "listino_articolo":
            annot = self.promeListinoArticolo(dao_local, dao_locale_ex)
        else:
            annot = "Articolo cambiato da %s a %s" %(dao_locale_ex.denominazione , dao_local.denominazione)
        if self.promeid:
            prome = self.pg_db_server_locale.promemoria.get(self.promeid)
            prome.annotazione = prome.annotazione+annot
        else:
            prome = self.pg_db_server_locale.promemoria.insert()
            prome.annotazione = annot
        prome.data_inserimento = datetime.datetime.now()
        prome.data_scadenza  = datetime.datetime.now()
        prome.oggetto = " Modifica"
        prome.incaricato ="sincro"
        prome.autore = "sincroBOT"
        prome.descrizione = "Automessaggio"
        prome.riferimento = "Interno"
        prome.giorni_preavviso  = 1
        prome.in_scadenza =True
        prome.scaduto =False
        prome.completato = False
        sqlalchemy.ext.sqlsoup.Session.add(prome)
        sqlalchemy.ext.sqlsoup.Session.commit()
        self.promeid = prome.id

    def createRandomString(self, num=5):
        b = ""
        for c in range(num):
            a = random.choice('1234567890abcdefghilmnopqrstuvz')
            b = b + a
        return b


    def manageArticoloSafe(self, remote):
        do = False
        for r in remote:
            loc = self.pg_db_server_locale.articolo.get(r.id)
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
#                    print "AAAAAAAAAAAAAAAAAAAA", a
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
                    try:
                        print "LOCA", loc, r
                        sqlalchemy.ext.sqlsoup.Session.commit()
                        do = False
                    except Exception,e :
                        print "ERRORE",e
                        sqlalchemy.ext.sqlsoup.Session.rollback()
                        print "FATTO IL ROOLBACK"
                        record_codice = self.pg_db_server_locale.articolo.filter_by(codice=r.codice).all()
                        if record_codice:
                            print " ABBIAMO UN CODICE GIA PRESENTE"
                            riga_scontr1 = self.pg_db_server_locale.riga_scontrino.filter_by(id_articolo=record_codice[0].id).all()
                            if riga_scontr1:
                                for r in riga_scontr1:
                                    r.id_articolo = 19746
                                    sqlalchemy.ext.sqlsoup.Session.add(r)
                                    sqlalchemy.ext.sqlsoup.Session.commit()
                            sqlalchemy.ext.sqlsoup.Session.delete(record_codice[0])
                            sqlalchemy.ext.sqlsoup.Session.commit()
                            if self.batch:
                                self.runBatch()
                            else:
                                self.test()
            else:
                print "ARTICOLO DA INSERIRE"
                soupLocale = self.dammiSoupLocale("articolo")
                newloc = soupLocale.articolo.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
#                print "QUESTO E DA INSERIRE", newloc
                try:
                    sqlalchemy.ext.sqlsoup.Session.commit()
                except Exception,e :
                    print "ERRORE",e
                    sqlalchemy.ext.sqlsoup.Session.rollback()
                    print "FATTO IL ROOLBACK"
                    record_codice = self.pg_db_server_locale.articolo.filter_by(codice=r.codice).all()
                    if record_codice:
                        print " ABBIAMO UN CODICE GIA PRESENTE"
                        riga_scontr1 = self.pg_db_server_locale.riga_scontrino.filter_by(id_articolo=record_codice[0].id).all()
                        if riga_scontr1:
                            for r in riga_scontr1:
                                r.id_articolo = 19746
                                sqlalchemy.ext.sqlsoup.Session.add(r)
                                sqlalchemy.ext.sqlsoup.Session.commit()
                        sqlalchemy.ext.sqlsoup.Session.delete(record_codice[0])
                        sqlalchemy.ext.sqlsoup.Session.commit()
                        if self.batch:
                            self.runBatch()
                        else:
                            self.test()
#        if len(locale)>len(remote):

#            print "CI SONO PIU RECORD IN LOCALE"
#            for l in locale:
#                loc = self.pg_db_server_locale.articolo.get(l.id)
#                if loc:
#                    ro = True
#                    for r in remote:
#                        if r.id == l.id:
#                            ro = False
#                    if ro:
#                        print "ELLE", l
#                        sqlalchemy.ext.sqlsoup.Session.delete(l)
#                        sqlalchemy.ext.sqlsoup.Session.commit()
#                        ro = True


    def manageListinoArticoloSafe(self, remote, locale, safer=None):
        do = False
        if safer:
            print "SUPER SAFER AL LAVORO"
            for l in locale:
                rem = self.pg_db_server_remote.listino_articolo.get([l.id_listino,l.id_articolo, l.data_listino_articolo])
                if not rem:
                    print "ECCODIC CHE RIMUOVIAMO", l
                    sqlalchemy.ext.sqlsoup.Session.delete(l)
                    sqlalchemy.ext.sqlsoup.Session.commit()

        for r in remote:
            loc = self.pg_db_server_locale.listino_articolo.get([r.id_listino,r.id_articolo, r.data_listino_articolo])
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
                    sqlalchemy.ext.sqlsoup.Session.commit()
                    do = False
            else:
                do = True
                soupLocale = self.dammiSoupLocale("listino_articolo")
                newloc = soupLocale.listino_articolo.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
                sqlalchemy.ext.sqlsoup.Session.commit()
                print "INSERISCO LSTART"


    def manageListinoMagazzinoSafe(self, remote):
        do = False
        for r in remote:
            loc = self.pg_db_server_locale.listino_magazzino.get(r.id)
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
                    sqlalchemy.ext.sqlsoup.Session.commit()
                    do = False
            else:
                soupLocale = self.dammiSoupLocale("listino_magazzino")
                newloc = soupLocale.listino_magazzino.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
                sqlalchemy.ext.sqlsoup.Session.commit()
                print "INSERISCO SCO VE INGR"


    def manageScontiVenditaIngrossoSafe(self, remote):
        do = False
        for r in remote:
            loc = self.pg_db_server_locale.sconti_vendita_ingrosso.get(r.id)
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
#                    sqlalchemy.ext.sqlsoup.Session.commit()
#                    do = False
            else:
                do = True
                soupLocale = self.dammiSoupLocale("sconti_vendita_ingrosso")
                newloc = soupLocale.sconti_vendita_ingrosso.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
#                sqlalchemy.ext.sqlsoup.Session.commit()
                print "INSERISCO SCO VE INGR"
        if do:
            sqlalchemy.ext.sqlsoup.Session.commit()
            do = False

    def manageScontiVenditaDettaglioSafe(self, remote):
        do = False
        for r in remote:
            loc = self.pg_db_server_locale.sconti_vendita_dettaglio.get(r.id)
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
#                    sqlalchemy.ext.sqlsoup.Session.commit()
#                    do = False
            else:
                do = True
                soupLocale = self.dammiSoupLocale("sconti_vendita_dettaglio")
                newloc = soupLocale.sconti_vendita_dettaglio.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
#                sqlalchemy.ext.sqlsoup.Session.commit()
                print "INSERISCO SCO VE DETT"
        if do:
            sqlalchemy.ext.sqlsoup.Session.commit()
            do = False

    def manageFornituraSafe(self, remote):
        do = False
        for r in remote:
            loc = self.pg_db_server_locale.fornitura.get(r.id)
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
                    try:
                        sqlalchemy.ext.sqlsoup.Session.commit()
                    except Exception,e :
                        print "ERRORE",e
                        sqlalchemy.ext.sqlsoup.Session.rollback()
                        print "FATTO IL ROOLBACK", 'id_fornitore', 'id_articolo', 'data_prezzo'
                        record_codice = self.pg_db_server_locale.fornitura.filter_by(id_fornitore=r.id_fornitore,
                                                                                    id_articolo=r.id_articolo,
                                                                                    data_prezzo= r.data_prezzo).all()
                        if record_codice:
                            print " ABBIAMO UN CODICE GIA PRESENTE"
                            sqlalchemy.ext.sqlsoup.Session.delete(record_codice[0])
                            sqlalchemy.ext.sqlsoup.Session.commit()
                        do = False
#                        if self.batch:
#                            self.runBatch()
#                        else:
#                            self.test()
            else:
                do = True
                soupLocale = self.dammiSoupLocale("fornitura")
                newloc = soupLocale.fornitura.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
                try:
                    sqlalchemy.ext.sqlsoup.Session.commit()
                except Exception,e :
                    print "ERRORE",e
                    sqlalchemy.ext.sqlsoup.Session.rollback()
                    print "FATTO IL ROOLBACK", 'id_fornitore', 'id_articolo', 'data_prezzo'
                    record_codice = self.pg_db_server_locale.fornitura.filter_by(id_fornitore=r.id_fornitore,
                                                                                id_articolo=r.id_articolo,
                                                                                data_prezzo= r.data_prezzo).all()
                    if record_codice:
                        print " ABBIAMO UN CODICE GIA PRESENTE"
                        sqlalchemy.ext.sqlsoup.Session.delete(record_codice[0])
                        sqlalchemy.ext.sqlsoup.Session.commit()
                    do = False
#                    if self.batch:
#                        self.runBatch()
#                    else:
#                        self.test()


    def manageStoccaggioSafe(self, remote):
        do = False
        for r in remote:
            loc = self.pg_db_server_locale.stoccaggio.get(r.id)
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
#                    sqlalchemy.ext.sqlsoup.Session.commit()
#                    do = False
            else:
                do = True
                print "INSERISCO STOCCAGGIO"
                soupLocale = self.dammiSoupLocale("sconto")
                newloc = soupLocale.stoccaggio.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
#                sqlalchemy.ext.sqlsoup.Session.commit()
        if do:
            sqlalchemy.ext.sqlsoup.Session.commit()
            do = False


    def manageScontoSafe(self, remote):
        do = False
        for r in remote:
            loc = self.pg_db_server_locale.sconto.get(r.id)
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
#                    sqlalchemy.ext.sqlsoup.Session.commit()
#                    do = False
            else:
                do =True
                print "INSERISCO SCONTO"
                soupLocale = self.dammiSoupLocale("sconto")
                newloc = soupLocale.sconto.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
#                sqlalchemy.ext.sqlsoup.Session.commit()
        if do:
            sqlalchemy.ext.sqlsoup.Session.commit()
            do = False


    def manageListinoComplessoListinoSafe(self, remote):
        do = False
        for r in remote:
            loc = self.pg_db_server_locale.listino_complesso_listino.get([r.id_listino, r.id_listino_complesso])
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
                    sqlalchemy.ext.sqlsoup.Session.commit()
                    do = False
            else:
                print "INSERISCO LISTINO COMPLESSO"
                soupLocale = self.dammiSoupLocale("listino_complesso_listino")
                newloc = soupLocale.listino_complesso_listino.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
                sqlalchemy.ext.sqlsoup.Session.commit()


    def manageCodBarreSafe(self, remote):
        do = False
        for r in remote:
            loc = self.pg_db_server_locale.codice_a_barre_articolo.get(r.id)
            if loc:
                for a in r.c:
                    t = str(a).split(".")[1]
                    if getattr(r, t) !=  getattr(loc, t):
                        print "DIVERSO" , getattr(r, t), getattr(loc, t)
                        do = True
                if do:
                    for i in loc.c:
                        ti = str(i).split(".")[1]
                        setattr(loc, ti, getattr(r, ti))
                    sqlalchemy.ext.sqlsoup.Session.add(loc)
                    try:
                        sqlalchemy.ext.sqlsoup.Session.commit()
                    except Exception,e :
                        print "ERRORE",e
                        sqlalchemy.ext.sqlsoup.Session.rollback()
                        print "FATTO IL ROOLBACK"
                        record_codice = self.pg_db_server_locale.codice_a_barre_articolo.filter_by(codice=r.codice).all()
                        if record_codice:
                            print " ABBIAMO UN CODICE GIA PRESENTE"
                            sqlalchemy.ext.sqlsoup.Session.delete(record_codice[0])
                            sqlalchemy.ext.sqlsoup.Session.commit()
                        do = False
                        if self.batch:
                            self.runBatch()
                        else:
                            self.test()
            else:
                print "INSERISCO CODICE A BARRE"
                soupLocale = self.dammiSoupLocale("codice_a_barre_articolo")
                newloc = soupLocale.codice_a_barre_articolo.insert()
                for i in newloc.c:
                    t = str(i).split(".")[1] #mi serve solo il nome tabella
                    setattr(newloc, t, getattr(r, t))
                sqlalchemy.ext.sqlsoup.Session.add(newloc)
                try:
                    sqlalchemy.ext.sqlsoup.Session.commit()
                except Exception,e :
                    print "ERRORE",e
                    sqlalchemy.ext.sqlsoup.Session.rollback()
                    print "FATTO IL ROOLBACK"
                    record_codice = self.pg_db_server_locale.codice_a_barre_articolo.filter_by(codice=r.codice).all()
                    if record_codice:
                        print " ABBIAMO UN CODICE GIA PRESENTE"
                        sqlalchemy.ext.sqlsoup.Session.delete(record_codice[0])
                        sqlalchemy.ext.sqlsoup.Session.commit()
                    do = False
                    if self.batch:
                        self.runBatch()
                    else:
                        self.test()


    def fixToTable(self, soup =None,soupLocale=None, op=None, rowMaster=None,rowSlave=None, dao=None, save=False, offset=None, dao_locale_ex=None):
        """rimanda alla gestione delle singole tabelle con le operazioni da fare
        """
        soupLocale = self.dammiSoupLocale(dao)

        if op =="DELETE":
            sqlalchemy.ext.sqlsoup.Session.delete(rowSlave)
            sqlalchemy.ext.sqlsoup.Session.commit()
        elif op == "INSERT":
            exec ("rowSlaveInsert = soupLocale.%s.insert()") %dao
            for i in rowMaster.c:
                t = str(i).split(".")[1] #mi serve solo il nome tabella
                setattr(rowSlaveInsert, t, getattr(rowMaster, t))
            sqlalchemy.ext.sqlsoup.Session.add(rowSlaveInsert)
        elif op == "UPDATE":
            try:
                for i in rowSlave.c:
                    #mi serve solo il nome colonna
                    t = str(i).split(".")[1]
                    setattr(rowSlave, t, getattr(rowMaster, t))
                sqlalchemy.ext.sqlsoup.Session.add(rowSlave)
            except Exception,e :
                print "QUALCOSA NELL'UPDATE NON È ANDATO BENE ERRORE",e
                sqlalchemy.ext.sqlsoup.Session.rollback()
                print "FATTO IL ROOLBACK"
                print
                print "RIGA LOCALE", rowSlave
                print
                print "RIGA REMOTA", rowMaster
                print
                self.azzeraTable(table=dao)

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
            sqlalchemy.ext.sqlsoup.Session.commit()

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
        if self.wear:
            self.daosMain(tables=tablesMainSchemePromoWear)
        self.daosScheme(tables=tablesSchemeArticolo)
        if self.wear:
            self.daosScheme(tables=tablesSchemePromoWear)
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
