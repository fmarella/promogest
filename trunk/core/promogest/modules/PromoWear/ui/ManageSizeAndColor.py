# -*- coding: UTF-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author:  Marco Pinna "Dr astico" <zoccolodignu@gmail.com>
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

import re, string, decimal
from decimal import *
import gtk, gobject, os
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.dao.Articolo import Articolo
import promogest.ui.AnagraficaListini
import promogest.ui.Main
from promogest.ui.Main import *
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import fillModelCombobox,fillComboboxListini
import promogest.ui.Login


class ManageSizeAndColor(GladeWidget):
    """Does price-list importation"""

    def __init__(self, mainWindow, data=None):
        #GladeWidget.__init__(self, 'promogest/modules/PromoWear/gui/gestione_varianti_taglia_colore')
        GladeWidget.__init__(self, 'gestione_varianti_taglie_colore',
                                fileName= 'promogest/modules/PromoWear/gui/gestione_varianti_taglia_colore.glade',
                                isModule=True)
        self.placeWindow(self.getTopLevel())
        self.getTopLevel().set_modal(modal=True)
        self.data= data
        self._treeViewModel = None
        self._rowEditingPath = None
        self._tabPressed = False
        self.denominazione_label.set_text(data['codice'] +" - "+data['denominazione'])
        self.mainWindow = mainWindow
        self.draw()
        #self.getTopLevel().show_all()

    def draw(self):
        """Creo una treeview che abbia come colonne i colori e come righe
            le taglie direi che sia il caso di gestire anche le descrizioni variante visto che le ho
        """
        self.treeview = self.taglie_colori_treeview
        rendererSx = gtk.CellRendererText()

        column = gtk.TreeViewColumn("Taglie", rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        #column.set_expand(False)
        column.set_min_width(40)
        self.treeview.append_column(column)



        cellspin = gtk.CellRendererSpin()
        cellspin.set_property("editable", True)
        cellspin.set_property("visible", True)

        adjustment = gtk.Adjustment(1, 1, 1000,0.500,2)
        cellspin.set_property("adjustment", adjustment)
        cellspin.set_property("digits",3)
        cellspin.set_property("climb-rate",3)
        cellspin.connect('edited', self.on_column_quantita_edited, self.treeview, True)
        #renderer = gtk.CellRendererText()
        #renderer.set_property('editable', True)
        #renderer.connect('edited', self.on_column_quantita_edited, self.treeview, True)
        #renderer.set_data('column', 0)
        #renderer.set_data('max_length', 10)

        column = gtk.TreeViewColumn('Quantità', cellspin, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(40)
        self.treeview.append_column(column)


        cellspin = gtk.CellRendererSpin()
        cellspin.set_property("editable", True)
        cellspin.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 100000,0.100,2)
        cellspin.set_property("adjustment", adjustment)
        cellspin.set_property("digits",3)
        cellspin.set_property("climb-rate",3)

        #renderer = gtk.CellRendererText()
        #renderer.set_property('editable', True)
        cellspin.connect('edited', self.on_column_prezzo_edited, self.treeview, True)
        #renderer.set_data('column', 1)
        #renderer.set_data('max_length', 15)

        column = gtk.TreeViewColumn('Prezzo', cellspin, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'denominazione_breve')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(80)
        self.treeview.append_column(column)

        column = gtk.TreeViewColumn("Denominazione", rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(80)
        self.treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object,str,str,str,str)
        self.treeview.set_model(self._treeViewModel)
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        self.price_entry.set_text(str(self.data['fornitura']['prezzoNetto']))

        self._treeViewModel.clear()
        varianti = self.data["varianti"]
        for var in varianti:
            quantita =""
            prezzo = ""
            self._treeViewModel.append((var,
                                        var['taglia']+" - "+var['colore'],
                                        quantita,
                                        str(var['fornitura']['prezzoNetto']),
                                        var['codice'] +" - "+var['denominazione']))

    def _getRowEditingPath(self, model, iterator):
        """ Restituisce il path relativo alla riga che e' in modifica """
        if iterator is not None:
            row = model[iterator]
            self._rowEditingPath = row.path

    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][0]["quantita"] = value
        model[path][2] = value

    def on_column_prezzo_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][0]["prezzoNetto"] = value
        model[path][3] = value

    def on_quantita_entry_focus_out_event(self, entry, widget):
        quantitagenerale = self.quantita_entry.get_text()
        #self._treeViewModel, quantitagenerale
        for row in self._treeViewModel:
            row[0]["quantita"] = quantitagenerale
            row[2] = quantitagenerale

    def on_price_entry_focus_out_event(self, entry, widget):
        prezzogenerale = self.price_entry.get_text()
        #self._treeViewModel, quantitagenerale
        for row in self._treeViewModel:
            row[0]["prezzoNetto"] = prezzogenerale
            row[3] = prezzogenerale

    def on_conferma_singolarmente_button_clicked(self,button):
        self.data['prezzoNetto']=self.price_entry.get_text()
        resultList= []
        for row in self._treeViewModel:
            resultList.append(row[0])
        Environment.tagliacoloretempdata= (False, resultList)
        self.mainWindow.promowear_manager_taglia_colore_togglebutton.set_active(False)
        self.destroy()

    def on_conferma_direttamente_button_clicked(self,button):
        self.data['prezzoNetto']=self.price_entry.get_text()
        resultList = []
        for row in self._treeViewModel:
            resultList.append(row[0])
        Environment.tagliacoloretempdata= (True, resultList)
        self.mainWindow.promowear_manager_taglia_colore_togglebutton.set_active(False)
        self.destroy()

    def on_cancel_button_clicked(self, button):
        self.mainWindow.promowear_manager_taglia_colore_togglebutton.set_active(False)
        self.destroy()
