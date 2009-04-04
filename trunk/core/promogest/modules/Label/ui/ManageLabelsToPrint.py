# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007-2009 by Promotux Informatica - http://www.promotux.it/
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

import string
from decimal import *
import gtk, gobject, os
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import fillModelCombobox,fillComboboxListini
from promogest.dao.Fornitura import Fornitura
from promogest.dao.DaoUtils import giacenzaArticolo


class ManageLabelsToPrint(GladeWidget):

    def __init__(self, mainWindow=None,daos=None):
        """Widget di transizione per visualizzare e confermare gli oggetti
            preparati per la stampa ( Multi_dialog.glade tab 1) 
        """
        GladeWidget.__init__(self, 'multi_dialog',
                        fileName= 'multi_dialog.glade')
        self.revert_button.destroy()
        self.apply_button.destroy()
        self.mainWindow = mainWindow
        self.daos = daos
        self.draw()

    def draw(self):
        """Creo una treeviewper la visualizzazione degli articoli che
            andranno poi in stampa
        """
        treeview = self.labels_treeview

        rendererSx = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Codice", rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_min_width(80)
        treeview.append_column(column)

        column = gtk.TreeViewColumn("Denominazione", rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(80)
        treeview.append_column(column)

        column = gtk.TreeViewColumn("codide a barre", rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(60)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(60)
        treeview.append_column(column)

        cellspin = gtk.CellRendererSpin()
        cellspin.set_property("editable", True)
        cellspin.set_property("visible", True)
        adjustment = gtk.Adjustment(1, 1, 1000,1,2)
        cellspin.set_property("adjustment", adjustment)
        #cellspin.set_property("digits",3)
        cellspin.set_property("climb-rate",3)
        cellspin.connect('edited', self.on_column_quantita_edited, treeview, True)
        column = gtk.TreeViewColumn('Quantità', cellspin, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(40)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object,str,str,str,str,str)
        treeview.set_model(self._treeViewModel)
        fillComboboxMagazzini(self.id_magazzino_label_combobox, True)
        self.id_magazzino_label_combobox.set_active(0)
        self.refresh()


    def on_ok_button_clicked(self,button):
        resultList= []
        for row in self._treeViewModel:
            if row[5] == "0" or row[5] == "":
                continue
            else:
                for v in range(0,int(row[5])):
                    resultList.append(row[0])

        self.mainWindow._handlePrinting(pdfGenerator=self.mainWindow.labelHandler,
                                report=True,daos=resultList,
                                label=True,returnResults=True)
        self.getTopLevel().destroy()


    def refresh(self):
        # Aggiornamento TreeView
        self._treeViewModel.clear()
        #print(dir(self.daos[0]))
        for dao in self.daos:
            quantita ="1"
            self._treeViewModel.append((dao,
                                        dao.codice_articolo,
                                        dao.articolo,
                                        dao.codice_a_barre,
                                        dao.prezzo_dettaglio,
                                        quantita,

                                        ))



    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        #model[path][0]["quantita"] = value
        model[path][5] = value

    def on_calculate_button_clicked(self, button):
        idMagazzino = findIdFromCombobox(self.id_magazzino_label_combobox)
        print "IDMAGAZZINOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", idMagazzino
        if self.manuale_radio.get_active():
            quantitagenerale = self.quantita_entry.get_text()
            for row in self._treeViewModel:
                row[5] = quantitagenerale
        elif self.giacenza_radio.get_active():
            for row in self._treeViewModel:
                if idMagazzino:
                    giacenza = giacenzaArticolo(year=Environment.workingYear,
                                            idMagazzino=idMagazzino,
                                            idArticolo=row[0].id_articolo)
                else:
                    giacenza = giacenzaArticolo(year=Environment.workingYear,
                                            idArticolo=row[0].id_articolo,
                                            allMag=True)
                if int(giacenza) <= 0 :
                    row[5] = "1"
                else:
                    row[5] = str(int(giacenza))
        elif self.movimento_radio.get_active():
            from promogest.dao.TestataDocumento import TestataDocumento
            for row in self._treeViewModel:
                docu = TestataDocumento().select(idArticolo=row[0].id_articolo)
                if docu:
                    doc = docu[-1]
                    for riga in doc.righe:
                        if riga.codice_articolo == row[1]:
                            quanti = riga.quantita
                            if int(quanti) <= 0 :
                                row[5] = "1"
                            else:
                                row[5] = str(int(quanti))

    def on_manuale_radio_toggled(self, radiobutton):
        if not self.manuale_radio.get_active():
            self.quantita_entry.set_property("sensitive",False)
        else:
            self.quantita_entry.set_property("sensitive",True)
        
    def on_quantita_entry_icon_press(self,entry,button,secondary):
        self.quantita_entry.set_text("")


    def on_discard_button_clicked(self, button):
        self.getTopLevel().destroy()
