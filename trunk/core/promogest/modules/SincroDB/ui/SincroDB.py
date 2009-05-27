# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import gtk
import gobject
from sqlalchemy.ext.serializer import loads, dumps
from promogest import Environment
from promogest.dao.AppLog import AppLog
from promogest.dao.Articolo import Articolo
from promogest.dao.Magazzino import Magazzino
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.GladeWidget import GladeWidget

class SincroDB(GladeWidget):
    """ Finestra di gestione esdportazione variazioni Database """
    def __init__(self):
        GladeWidget.__init__(self, 'sincro_dialog',
                        fileName='sincro_dialog.glade')
        self.placeWindow(self.getTopLevel())
        self.magazzini_treeview()
        self.filename_entry.set_text("exportData")

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

    def on_perchi_checkbutton_toggled(self, toggle):
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

    def createSchema(self):
        """
        Genera un bel db, aggiornato alla versione attualecd corpo
        """
        variazioni = AppLog().select(batchSize=None)
        for v in variazioni:
            print v 
        #engine = create_engine('sqlite:////home/mentore/pg2_work/ciccio_db')
        ## create MetaData
        #meta2 = MetaData()
        ## bind to an engine
        #meta2.bind = engine

        #prova = []
        #newmetadata = Environment.params['metadata']
##        print newmetadata.tables
        #for t in newmetadata.sorted_tables:
            #t.__dict__['metadata'] = meta2
            #t.__dict__['schema'] = ""
            #t.__dict__['fullname'] = t.__dict__['fullname'].split(".")[1]
        #for g in newmetadata.sorted_tables:
            #print g.__dict__
##            t.create(meta2, checkfirst=True)
        #newmetadata.create_all(checkfirst=True)
##            table.split('.')[1]
##        prova.append
##        newmetadata.create_all(bind=create_engine('sqlite:////home/mentore/pg2_work/ciccio_db'), checkfirst=True)
        #return


    def retreiveDir(self):
        savetoDir = self.destination_filechooserbutton.get_current_folder()
        return savetoDir

    def retreiveFileName(self):
        saveToName = self.filename_entry.get_text()
        return saveToName

    def retreiveData(self):
        Environment.meta.reflect(schema="latelier" )
        app = Environment.params["session"].query(AppLog).filter(and_(AppLog.schema_azienda =="latelier",AppLog.message=="INSERT Articolo")).all()
        #app = Environment.params["session"].query(Articolo).all()[:10]
        print app
        for a in app:
            #print a.pkid
            print a.id
            #b = dumps(a)
            #print a.object
            c =  loads(a.object, Environment.params["metadata"],Environment.Session)
            print "GGGGGGGGGG",c.codice

    def retreiveWhat(self):
        """
        Vediamo cosa è stato selezionato per l'esportazione
        """
        articoli = self.articoli_togglebutton.set_active(True)
        clienti = self.clienti_togglebutton.set_active(True)
        parametri = self.parametri_togglebutton.set_active(True)
        magazzini = self.magazzini_togglebutton.set_active(True)
        fornitori = self.fornitori_togglebutton.set_active(True)
        vettori = self.vettori_togglebutton.set_active(True)


    def on_run_button_clicked(self, button):
        self.createSchema()
        print "RUN",  self.retreiveDir(), self.retreiveFileName()
        self.retreiveDir()
        self.retreiveFileName()
        #self.retreiveData()

