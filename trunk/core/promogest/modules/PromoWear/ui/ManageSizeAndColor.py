# -*- coding: UTF-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

import string
from decimal import *
import gtk, gobject, os
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import fillModelCombobox,fillComboboxListini


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

        column = gtk.TreeViewColumn("Taglia / Colore", rendererSx, text=1)
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
        cellspin.connect('edited', self.on_column_prezzo_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Prezzo', cellspin, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'denominazione_breve')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(60)
        self.treeview.append_column(column)

        celltext = gtk.CellRendererText()
        celltext.set_property("editable", True)
        celltext.set_property("visible", True)
        celltext.connect('edited', self.on_column_sconto_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Sconto', celltext, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'denominazione_breve')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(50)
        self.treeview.append_column(column)

        column = gtk.TreeViewColumn("Prezzo Netto", rendererSx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(60)
        self.treeview.append_column(column)


        column = gtk.TreeViewColumn("Denominazione", rendererSx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(80)
        self.treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object,str,str,str,str,str,str)
        self.treeview.set_model(self._treeViewModel)
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        self.price_entry.set_text(str(self.data['fornitura']['prezzoLordo']))
        self.discount_entry.set_text(str(self.formatSconti(self.data)))

        self._treeViewModel.clear()
        varianti = self.data["varianti"]
        for var in varianti:
            quantita =""
            prezzo = ""
            sconto = str(self.formatSconti(var))
            self._treeViewModel.append((var,
                                        var['taglia']+" - "+var['colore'],
                                        quantita,
                                        str(var['fornitura']['prezzoLordo']),
                                        sconto,
                                        str(var['fornitura']['prezzoNetto']),
                                        var['codice'] +" - "+var['denominazione']))
    def formatSconti(self, var):
        if not var['fornitura']['sconti']:
            sconto = ""
        elif str(var['fornitura']['sconti'][0]['tipo']) == "valore":
            sconto = str(var['fornitura']['sconti'][0]['valore'])+"€"
        elif str(var['fornitura']['sconti'][0]['tipo']) == "percentuale":
            sconto = str(var['fornitura']['sconti'][0]['valore'])+"%"
        else:
            sconto = ""
        return sconto

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
        model[path][0]['fornitura']["prezzoLordo"] = value
        model[path][3] = value

    def on_column_sconto_edited(self, cell, path, value, treeview, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][0]['fornitura']["sconto"] = [value]
        model[path][4] = value
        if model[path][3] and "%" in value:
            value= int(value[0:-1].strip())
            prezzo = float(model[path][3]) * (1 - float(value) / 100)
            model[path][5] = prezzo
            model[path][0]['fornitura']["sconti"] = [{'tipo':"percentuale",
                                            'valore':float(value)},]
            model[path][0]['fornitura']["prezzoNetto"]= model[path][5]
        elif model[path][3] and value == "0" or value == "":
            model[path][5] = model[path][3]
            model[path][0]['fornitura']["sconti"] = []
            model[path][0]['fornitura']["prezzoNetto"]= model[path][5]
        elif model[path][3] and "€" in value:
            value = str(value).strip()
            value = value.replace("€", '')
            value= int(value)
            model[path][5] = float(model[path][3]) - float(value)
            model[path][0]['fornitura']["sconti"] = [{'tipo':"valore",
                                            'valore':float(value)},]
            model[path][3]['fornitura']["prezzoNetto"]= float(model[path][5])
        #if model[path][3] and "%" in value:
            #value= int(value[0:-1].strip())
            #model[path][5] = float(model[path][3]) * (1 - float(value) / 100)

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
            row[0]['fornitura']["prezzoLordo"] = prezzogenerale
            row[3] = prezzogenerale

    def on_discount_entry_focus_out_event(self, entry, widget):
        scontogenerale = self.discount_entry.get_text()
        #self._treeViewModel, quantitagenerale
        for row in self._treeViewModel:
            row[4] = scontogenerale
            if row[3] and "%" in scontogenerale:
                value= int(scontogenerale[0:-1].strip())
                prezzo = float(row[3]) * (1 - float(value) / 100)
                row[5] = prezzo
                row[0]['fornitura']["sconti"] = [{'tipo':"percentuale",
                                                 'valore':float(value)},]
                row[0]['fornitura']["prezzoNetto"]= row[5]
            elif row[3] and scontogenerale == "0" or scontogenerale == "":
                row[5] = row[3]
                row[0]['fornitura']["sconti"] = []
                row[0]['fornitura']["prezzoNetto"]= row[5]
            elif row[3] and "€" in scontogenerale:
                value = str(scontogenerale).strip()
                value = value.replace("€", '')
                value= int(value)
                row[5] = float(row[3]) - float(value)
                row[0]['fornitura']["sconti"] = [{'tipo':"valore",
                                                'valore':float(value)},]
                row[0]['fornitura']["prezzoNetto"]= row[5]

    def on_conferma_singolarmente_button_clicked(self,button):
        self.data['fornitura']['prezzoLordo']=self.price_entry.get_text()
        resultList= []
        for row in self._treeViewModel:
            if row[0]['quantita'] == "0" or row[0]['quantita'] == "":
                continue
            else:
                resultList.append(row[0])
        Environment.tagliacoloretempdata= (False, resultList)
        self.mainWindow.promowear_manager_taglia_colore_togglebutton.set_active(False)
        self.destroy()

    def on_conferma_direttamente_button_clicked(self,button):
        self.data['fornitura']['prezzoLordo']=self.price_entry.get_text()
        resultList = []
        for row in self._treeViewModel:
            if row[0]['quantita'] == "0" or row[0]['quantita'] == "" :
                continue
            else:
                resultList.append(row[0])
        Environment.tagliacoloretempdata= (True, resultList)
        self.mainWindow.promowear_manager_taglia_colore_togglebutton.set_active(False)
        self.destroy()

    def on_cancel_button_clicked(self, button):
        self.mainWindow.promowear_manager_taglia_colore_togglebutton.set_active(False)
        resultList = []
        Environment.tagliacoloretempdata= (True, resultList)
        self.destroy()
