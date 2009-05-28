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


    def createSchema(self):
        """
        Genera un bel db, aggiornato alla versione attualecd corpo
        """
        variazioni = AppLog().select(batchSize=None)
        for v in variazioni:
            print v.message, loads(v.object)

    def retreiveDir(self):
        savetoDir = self.destination_filechooserbutton.get_current_folder()
        return savetoDir

    def retreiveFileName(self):
        saveToName = self.filename_entry.get_text()
        return saveToName

    def retreiveData(self):
        Environment.meta.reflect(schema="latelier" )
        app = Environment.params["session"].query(AppLog).filter(and_(AppLog.schema_azienda =="latelier",AppLog.message=="INSERT Articolo")).all()


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
        righe = AppLog().select(batchSize=None, level="N")
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


    def on_run_button_clicked(self, button):
        #self.createSchema()
        print "RUN",  self.retreiveDir(), self.retreiveFileName()
        self.retreiveDir()
        self.retreiveFileName()
        self.retreiveWhat()
        #self.retreiveData()

