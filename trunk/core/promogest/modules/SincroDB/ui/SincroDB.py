# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import gtk
import gobject
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.AppLog import AppLog
from promogest.dao.Articolo import Articolo
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Listino import Listino
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.GladeWidget import GladeWidget
from sqlalchemy.ext.sqlsoup import SqlSoup
from promogest.modules.SincroDB.data.listino_table import listino_table
from promogest.modules.SincroDB.data.aliquota_iva_table import aliquota_iva_table
from promogest.modules.SincroDB.data.listino_articolo_table import listino_articolo_table
from promogest.modules.SincroDB.data.tipo_aliquota_iva_table import tipo_aliquota_iva_table
from promogest.modules.SincroDB.data.articolo_table import articolo_table

class SincroDB(GladeWidget):
    """ Finestra di gestione esdportazione variazioni Database """
    def __init__(self):
        GladeWidget.__init__(self, 'sincro_dialog',
                        fileName='sincro_dialog.glade')
        self.placeWindow(self.getTopLevel())
        self.magazzini_treeview()
        self.filename_entry.set_text("exportData")
        self.draw()

    def draw(self):
        treeview = self.sincro_treeview
        self._sincroTreeViewModel = gtk.ListStore(bool, str, str, str,  str, str, str)
        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, treeview, True)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)

        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        #column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Utente_DB', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Schema Azienda', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Operato?', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Message', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Valore', renderer, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Data Operazione', renderer, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_model(self._sincroTreeViewModel)

    def magazzini_treeview(self):
        """ disegna la treeeview dei magazzini """
        treeview = self.magazzino_treeview
        self._magazzinoTreeViewModel = gtk.ListStore(bool, int, str)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, treeview, True)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)

        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        #column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)
        #treeview.set_search_column(3)

        mag=Magazzino().select(batchSize=None)
        for u in mag:
            self._magazzinoTreeViewModel.append((False,
                            u.id,
                            u.denominazione))

        treeview.set_model(self._magazzinoTreeViewModel)

    def onColumnEdited(self, cell, path, treeview,value, editNext=True):
        model = treeview.get_model()
        model[path][0] = not model[path][0]

    def on_tuttecose_checkbutton_toggled(self,toggled):
        """ check delle anag da esportare ...le seleziona tutte """
        if self.tuttecose_checkbutton.get_active():
            self.articoli_togglebutton.set_active(True)
            self.clienti_togglebutton.set_active(True)
            self.parametri_togglebutton.set_active(True)
            self.magazzini_togglebutton.set_active(True)
            self.fornitori_togglebutton.set_active(True)
            self.vettori_togglebutton.set_active(True)
        else:
            self.articoli_togglebutton.set_active(False)
            self.clienti_togglebutton.set_active(False)
            self.parametri_togglebutton.set_active(False)
            self.magazzini_togglebutton.set_active(False)
            self.fornitori_togglebutton.set_active(False)
            self.vettori_togglebutton.set_active(False)


    def on_perchi_checkbutton_toggled(self, toggle):
        print "FDHHDFHKGKGHDFHFHFHDF"
        model = self.magazzino_treeview.get_model()
        if self.perchi_checkbutton.get_active():
            for m in model:
                if m[0]:
                    pass
                else:
                    m[0] = not m[0]
        else:
            for m in model:
                if m[0]:
                    m[0] = not m[0]
                else:
                    pass

    def on_genera_button_clicked(self, button):
        """
        Ricerca l'ultima data utile e la suggferisce nella entry
        """
        print "GENERA BUTTONE"

    def connectDbRemote(self):
        self.mainSchema = "promogest2"
        user = "promoadmin"
        password = "admin"
        host = "192.168.1.119"
        port = "5432"
        database = "promogest_db"

        #azienda=conf.Database.azienda
        engine = create_engine('postgres:'+'//'
                        +user+':'
                        + password+ '@'
                        + host + ':'
                        + port + '/'
                        + database,
                        encoding='utf-8',
                        convert_unicode=True )
        tipo_eng = engine.name
        engine.echo = False
        self.metaRemote = MetaData(engine)
        self.pg_db_server_remote = SqlSoup(self.metaRemote)
        self.pg_db_server_remote.schema = Environment.params["schema"]
        self.pg_db_server_main_remote = SqlSoup(self.metaRemote)
        self.pg_db_server_main_remote.schema = "promogest2"
            #Session = sessionmaker(bind=engine)
        SessionRemote = scoped_session(sessionmaker(bind=engine))
        self.sessionRemote = SessionRemote()

    def connectDbLocale(self):
        self.mainSchema = "promogest2"
        user = "promoadmin"
        password = "admin"
        host = "localhost"
        port = "5432"
        database = "promogest_db"

        #azienda=conf.Database.azienda
        engine = create_engine('postgres:'+'//'
                        +user+':'
                        + password+ '@'
                        + host + ':'
                        + port + '/'
                        + database,
                        encoding='utf-8',
                        convert_unicode=True )
        tipo_eng = engine.name
        engine.echo = False
        self.metaLocale = MetaData(engine)
        self.pg_db_server_locale = SqlSoup(self.metaLocale)
        self.pg_db_server_locale.schema = Environment.params["schema"]
        self.pg_db_server_main_locale = SqlSoup(self.metaLocale)
        self.pg_db_server_main_locale.schema = "promogest2"
            #Session = sessionmaker(bind=engine)
        SessionLocale = scoped_session(sessionmaker(bind=engine))
        self.sessionLocale = SessionLocale()



    def createSchema(self):
        """
        Genera un bel db, aggiornato alla versione attualecd corpo
        """
        variazioni = AppLog().select(batchSize=None)
        for v in variazioni:
            print v.message , loads(v.object)
        try:
            listino = Listino().getRecord(id=loads(v.object))
        except:
            print "pazienza"
        print "listtiinonononono", listino


    def retreiveDir(self):
        savetoDir = self.destination_filechooserbutton.get_current_folder()
        return savetoDir

    def retreiveFileName(self):
        saveToName = self.filename_entry.get_text()
        return saveToName


        #daosScheme = ["magazzino","setting","aliquota_iva","categoria_articolo",
                    #"famiglia_articolo","image","imballaggio","articolo","multiplo",
                    #"listino","persona_giuridica","pagamento","banca","cliente",
                    #"categoria_fornitore","CategoriaFornitoreDb","fornitore",
                    #"destinazione_merce","vettore","agente","testata_documento",
                    #"testata_movimento","riga","sconto" ,"riga_movimento",
                    #"sconto_riga_movimento","static_page", "static_menu",
                    #"contatto", "contatto_cliente","recapito","categoria_contatto",
                    #"contatto_categoria_contatto","categoria_cliente", "codice_a_barre_articolo",
                    #"listino_articolo", "cart","articolo_associato","access",
                    #"listino_magazzino","listino_categoria_cliente",
                    #"cliente_categoria_cliente","contatto_fornitore",
                    #"contatto_magazzino","contatto_azienda","feed",
                    #"fornitura", "sconto_fornitura","informazioni_contabili_documento",
                    #"inventario","promemoria","riga_documento","listino_complesso_listino",
                    #"listino_complesso_articolo_prevalente","sconto_riga_documento",
                    #"sconto_testata_documento", "sconti_vendita_dettaglio",
                    #"sconti_vendita_ingrosso","spesa","testata_documento_scadenza",
                    #"stoccaggio"]


    def retreiveWhat(self):
        """
        Vediamo cosa è stato selezionato per l'esportazione
        """
        articoli = self.articoli_togglebutton.get_active()
        clienti= self.clienti_togglebutton.get_active()
        parametri = self.parametri_togglebutton.get_active()
        magazzini = self.magazzini_togglebutton.get_active()
        fornitori = self.fornitori_togglebutton.get_active()
        vettori = self.vettori_togglebutton.get_active()
        daData = stringToDate(self.da_data_filter_entry.get_text())
        adData = stringToDate(self.a_data_filter_entry.get_text())
        model = self.magazzino_treeview.get_model()
        toMagazziniId= []
        for m in model:
            if m[0]: toMagazziniId.append(m[1])
        #righe = AppLog().select(batchSize=None, level="N")
        app_log = Table('app_log', self.metaRemote, autoload=True, schema=self.mainSchema)
        righe = self.sessionRemote.query(app_log).filter(app_log.c.schema_azienda == Environment.params["schema"]).all()
        modello = self.sincro_treeview.get_model()
        modello.clear()
        for r in righe:
            modello.append((True,
                            r.utentedb,
                            r.schema_azienda,
                            r.level,
                            r.message,
                            r.value,
                            r.registration_date))
        self.sincro_treeview.set_model(modello)


        if self.tuttecose_checkbutton.get_active():
            daosMain = [
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
            for dg in daosMain:
                exec ("remote=self.pg_db_server_main_remote.%s.all()") %dg
                remote.sort()
                exec ("locale=self.pg_db_server_main_locale.%s.all()") %dg
                locale.sort()
                #print dg, "=",locale
                self.logica(remote=remote, locale=locale)

    def logica(remote=None, locale=None):
        if remote == locale:
            print "VEROOOOOO"
            continue
        else:
            if len(remote) == len(locale):
                print "STESSO NUMERO DI RECORD", len(remote)
            elif len(remote) > len(locale):
                print "IL DB REMOTO CONTIENE PIU' RECORD", len(remote), "vs", len(locale)
            else:
                print "IL DB LOCALE CONTIENE PIU' RECORD", len(remote), "vs", len(locale)
            for i in range(0,len(remote)):
                if i< len(locale):
                    if  remote[i] == locale[i]:
                        print "-> RIGHE UGUALI"
                    else:
                        print "QUESTA È LA RIGA DIVERSA NELLA TABELLA ", str(locale[i]._table).split(".")[1], "Operazione UPDATE"
                        self.fixToTable(row=remote[i], op="UPDATE", dao=str(locale[i]._table).split(".")[1])
                else:
                    print "QUESTA È LA RIGA DA AGGIUNGERE NELLA TABELLA ", str(remote[i]._table).split(".")[1], "Operazione INSERT"
                    self.fixToTable(row=remote[i], op="INSERT", dao=str(remote[i]._table).split(".")[1])

                    #else:
                        #print "DIVERSO NUMERO", len(remote)

    def fixToTable(self, soup =None, op=None, row=None,dao=None):
        if dao=="Listino" or dao=="listino":
            listino_table(soup=soup,op=op, dao=dao, row=row)
        elif dao=="TipoAliquotaIva" or dao=="tipo_aliquota_iva":
            tipo_aliquota_iva_table(soup=soup,op=op, dao=dao, row=row)
    #for g in righe:
            #messlist = g.message.split(";")
            #op = messlist[0]
            #dao = messlist[1]
            #if dao =="Listino":
                #listino_table(soup=self.pg_db_server,op=op, dao=dao, row=g)
            #elif dao =="ListinoArticolo":
                #listino__articolo_table(soup=self.pg_db_server,op=op, dao=dao, row=g)
            #elif dao =="AliquotaIva":
                #aliquota_iva_table(soup=self.pg_db_server,op=op, dao=dao, row=g)
            #elif dao =="Articolo":
                #articolo_table(soup=self.pg_db_server,op=op, dao=dao, row=g)
                

    def on_run_button_clicked(self, button):
        self.connectDbRemote()
        self.connectDbLocale()
        #self.createSchema()
        print "RUN",  self.retreiveDir(), self.retreiveFileName()
        self.retreiveDir()
        self.retreiveFileName()
        self.retreiveWhat()
        #self.retreiveData()

