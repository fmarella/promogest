# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

import string
import operator
from decimal import *
import gtk, gobject, os
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import fillModelCombobox,fillComboboxListini
from promogest.dao.Fornitura import Fornitura
from promogest.modules.PromoWear.ui.PromowearUtils import leggiArticoloPromoWear, leggiFornituraPromoWear
from promogest.modules.PromoWear.dao.GruppoTagliaTaglia import GruppoTagliaTaglia


class ManageSizeAndColor(GladeWidget):
    """Gestione e selezione taglie e colori da inserire come righe in doc"""

    def __init__(self, mainWindow, articolo=None, data=None, idPerGiu=None,
                                            idListino=None, fonteValore=None):
        GladeWidget.__init__(self, 'gestione_varianti_taglie_colore',
                    fileName= 'promogest/modules/PromoWear/gui/gestione_varianti_taglia_colore.glade',
                    isModule=True)
        self.placeWindow(self.getTopLevel())
        self.getTopLevel().set_modal(modal=True)
        self.articoloPadre= articolo
        self.idPerGiu = idPerGiu
        self.data = data
        self._id_listino = idListino
        self._fornitura = None
        self._listino = None
        self._fonteValore=fonteValore
        if ((self._fonteValore == "acquisto_iva") or  (self._fonteValore == "acquisto_senza_iva")):
            self.TipoOperazione = "acquisto"
        elif ((self._fonteValore == "vendita_iva") or (self._fonteValore == "vendita_senza_iva")):
            self.TipoOperazione = "vendita"
        self.articoloPadreDict = self.creDictFornitura()
        self._treeViewModel = None
        self._rowEditingPath = None
        self._tabPressed = False
        self.denominazione_label.set_text(self.articoloPadre.codice +" - "+self.articoloPadre.denominazione)
        self.mainWindow = mainWindow
        self.draw()
        #self.getTopLevel().show_all()

    def draw(self):
        """Creo una treeview che abbia come colonne i colori e come righe
           le taglie direi che sia il caso di gestire anche le descrizioni variante visto che le ho
        """
        self.treeview = self.taglie_colori_treeview
        rendererSx = gtk.CellRendererText()

        column = gtk.TreeViewColumn("Taglia", rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.refresh, 'Taglia')
        column.set_resizable(True)
        #column.set_expand(False)
        column.set_min_width(40)
        self.treeview.append_column(column)

        column = gtk.TreeViewColumn("Colore", rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.refresh, 'Colore')
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
        column = gtk.TreeViewColumn('Quantità', cellspin, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
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
        column = gtk.TreeViewColumn('Prezzo', cellspin, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(60)
        self.treeview.append_column(column)

        celltext = gtk.CellRendererText()
        celltext.set_property("editable", True)
        celltext.set_property("visible", True)
        celltext.connect('edited', self.on_column_sconto_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Sconto', celltext, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(50)
        self.treeview.append_column(column)

        column = gtk.TreeViewColumn("Prezzo Netto", rendererSx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(60)
        self.treeview.append_column(column)


        column = gtk.TreeViewColumn("Denominazione", rendererSx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(80)
        self.treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object,str,str,str,str,str,str,str)
        self.treeview.set_model(self._treeViewModel)
        self.refresh(None)

    def creaRiga(self, var):
        if self.TipoOperazione == "acquisto":
            megaDict[artvar]["fornitura"]=self._fornitura = leggiFornitura(self.articoloPadre.id, idFornitore=self.idPerGiu, data=self.data)
        else:
            megaDict[artvar]["listino"] = self._listino = leggiListino(self._id_listino,idArticolo=self.articoloPadre.id )



    def creDictFornitura(self):
        """
            Creo un dizionario delle forniture? ... Commenta Francè commentaaaaaaaaaaa
        """
        artiDict= {}
        variantiList = []
        daoArticolo = self.articoloPadre
        
        varianti = daoArticolo.articoliVarianti 

        for varia in varianti:
            variante=leggiArticoloPromoWear(varia.id, full=True)
            if self.TipoOperazione =="acquisto":
                variante['valori'] = leggiFornituraPromoWear(idArticolo=varia.id,
                                                idFornitore=self.idPerGiu,
                                                data=self.data)
                variantiList.append(variante)
            else:   # vendita
                variante['valori'] = leggiListino(self._id_listino,idArticolo=self.articoloPadre.id )
                variante['valori']['prezzoDettaglioScontato'] = 0
                variantiList.append(variante)
        out = []
        for e in variantiList:
            out.append((e['ordine'],e))
        getcount = operator.itemgetter(0)
        map(getcount, out)
        out2 = sorted(out, key=getcount)
        newlist = []
        for a in out2:
            newlist.append(a[1])
        artiDict = leggiArticoloPromoWear(self.articoloPadre.id)
        artiDict["varianti"] = newlist #al dizionatio articolo dell'articolo padre aggancio la lista delle varianti
        if self.TipoOperazione == "acquisto":
            artiDict['valori'] = leggiFornitura(self.articoloPadre.id,idFornitore=self.idPerGiu, data=self.data)
        else:  #operazione vendita
            artiDict['valori'] = leggiListino(self._id_listino,idArticolo=self.articoloPadre.id )
        return artiDict


    def refresh(self,treeview=None, order = "Taglia"):
        """ Aggiornamento della principale treeview, si può ordinare? """
        self._treeViewModel.clear()
        if self.TipoOperazione == "acquisto":
            self.price_entry.set_text(str(self.articoloPadreDict['valori']['prezzoLordo']))
        else:
            self.price_entry.set_text(str(self.articoloPadreDict['valori']['prezzoDettaglio']))
        self.discount_entry.set_text(str(self.formatSconti(self.articoloPadreDict['valori'])))

        varianti = self.articoloPadreDict["varianti"]
        #print varianti

        for var in varianti:
            quantita =""
            if self.TipoOperazione == "acquisto":
                prezzoLordo = str(var['valori']['prezzoLordo'])
                prezzoNetto = str(var['valori']['prezzoNetto'])
            else:
                prezzoLordo = str(var['valori']['prezzoDettaglio'])
                prezzoNetto = str(var['valori']['prezzoDettaglioScontato'])
            
            sconto = str(self.formatSconti(var['valori']))
            self._treeViewModel.append((var,
                                        str(var['taglia']),
                                        str(var['colore']),
                                        quantita,
                                        prezzoLordo,
                                        sconto,
                                        prezzoNetto,
                                        str(var['codice']) +" - "+str(var['denominazione'])))

    def formatSconti(self, var):
        if self.TipoOperazione == "acquisto":
            if not var['sconti']:
                sconto = ""
            elif str(var['sconti'][0]['tipo']) == "valore":
                sconto = str(var['sconti'][0]['valore'])+"€"
            elif str(var['sconti'][0]['tipo']) == "percentuale":
                sconto = str(var['sconti'][0]['valore'])+"%"
            else:
                sconto = ""
        else: #tipo operazione vendita
            if not var['scontiDettaglio']:
                sconto = ""
            elif str(var['scontiDettaglio'][0]['tipo']) == "valore":
                sconto = str(var['sconti'][0]['valore'])+"€"
            elif str(var['scontiDettaglio'][0]['tipo']) == "percentuale":
                sconto = str(var['scontiDettaglio'][0]['valore'])+"%"
            else:
                sconto = ""
        return sconto

    def _getRowEditingPath(self, model, iterator):
        """ Restituisce il path relativo alla riga che e' in modifica """
        if iterator is not None:
            row = model[iterator]
            self._rowEditingPath = row.path

    def on_column_quantita_edited(self, cell, path, value, treeview, editNext=True):
        """ Function to set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][0]["quantita"] = value
        model[path][3] = value

    def on_column_prezzo_edited(self, cell, path, value, treeview, editNext=True):
        """ Function to set the value quantita edit in the cell"""
        model = treeview.get_model()
        if self.TipoOperazione == "acquisto":
                model[path][0]['valori']["prezzoLordo"] = value
        else:
            model[path][0]['valori']["prezzoDettaglio"] = value
        
        model[path][4] = value
        if model[path][5] =="0" or model[path][5] == None or model[path][5]=="" :
            model[path][6] = model[path][4]
        if self.TipoOperazione == "acquisto":
            model[path][0]['valori']["prezzoNetto"] = model[path][4]
        else:
            model[path][0]['valori']["prezzoDettaglioScontato"] = model[path][4]

    def on_column_sconto_edited(self, cell, path, value, treeview, editNext=True):
        """ Function to set the value quantita edit in the cell"""
        model = treeview.get_model()
        if self.TipoOperazione == "acquisto":
            model[path][0]['valori']["sconto"] = [value]
        else:
            model[path][0]['valori']["scontiDettaglio"] = [value]
        model[path][5] = value
        if model[path][4] and "%" in value:
            value= int(value[0:-1].strip())
            prezzo = float(model[path][4]) * (1 - float(value) / 100)
            model[path][6] = prezzo
            model[path][0]['valori']["sconti"] = [{'tipo':"percentuale",
                                            'valore':float(value)},]
            if self.TipoOperazione == "acquisto":
                model[path][0]['valori']["sconti"] = [{'tipo':"percentuale",
                                            'valore':float(value)},]
                model[path][0]['valori']["prezzoNetto"] = model[path][5]
            else:
                model[path][0]['valori']["scontiDettaglio"] = [{'tipo':"percentuale",
                                            'valore':float(value)},]
                model[path][0]['valori']["prezzoDettaglioScontato"] = model[path][5]
        elif model[path][4] and value == "0" or value == "":
            model[path][6] = model[path][4]
            if self.TipoOperazione == "acquisto":
                model[path][0]['valori']["sconti"] = []
                model[path][0]['valori']["prezzoNetto"] = model[path][6]
            else:
                model[path][0]['valori']["scontiDettaglio"] = []
                model[path][0]['valori']["prezzoDettaglioScontato"] = model[path][6]
        elif model[path][4] and "€" in value:
            value = str(value).strip()
            value = value.replace("€", '')
            value= int(value)
            model[path][6] = float(model[path][3]) - float(value)

            if self.TipoOperazione == "acquisto":
                model[path][0]['valori']["sconti"] = [{'tipo':"valore",
                                            'valore':float(value)},]
                model[path][3]['valori']["prezzoNetto"]= float(model[path][6])
            else:
                model[path][0]['valori']["scontiDettaglio"] = [{'tipo':"valore",
                                            'valore':float(value)},]
                model[path][3]['valori']["prezzoDettaglioScontato"]= float(model[path][6])

    def on_quantita_entry_focus_out_event(self, entry, widget):
        quantitagenerale = self.quantita_entry.get_text()
        for row in self._treeViewModel:
            row[0]['quantita'] = quantitagenerale
            row[3] = quantitagenerale

    def on_price_entry_focus_out_event(self, entry, widget):
        prezzogenerale = self.price_entry.get_text()
        for row in self._treeViewModel:
            if self.TipoOperazione == "acquisto":
                row[0]['valori']["prezzoLordo"] = prezzogenerale
            else:
                row[0]['valori']["prezzoDettaglio"] = prezzogenerale
            row[4] = prezzogenerale

    def on_discount_entry_focus_out_event(self, entry, widget):
        scontogenerale = self.discount_entry.get_text()
        for row in self._treeViewModel:
            row[5] = scontogenerale
            if row[4] and "%" in scontogenerale:
                value= int(scontogenerale[0:-1].strip())
                prezzo = float(row[4]) * (1 - float(value) / 100)
                row[6] = prezzo

                if self.TipoOperazione == "acquisto":
                    row[0]['valori']["sconti"] = [{'tipo':"percentuale",
                                                 'valore':float(value)},]
                    row[0]['valori']["prezzoNetto"]= row[6]
                else:
                    row[0]['valori']["scontiDettaglio"] = [{'tipo':"percentuale",
                                                 'valore':float(value)},]
                    row[0]['valori']["prezzoDettaglioScontato"]= row[6]
            elif row[4] and scontogenerale == "0" or scontogenerale == "":
                row[6] = row[4]

                if self.TipoOperazione == "acquisto":
                    row[0]['valori']["sconti"] = []
                    row[0]['valori']["prezzoNetto"]= row[5]
                else:
                    row[0]['valori']["sconti"] = []
                    row[0]['valori']["prezzoDettaglioScontato"]= row[6]
            elif row[4] and "€" in scontogenerale:
                value = str(scontogenerale).strip()
                value = value.replace("€", '')
                value= int(value)
                row[6] = float(row[3]) - float(value)
                if self.TipoOperazione == "acquisto":
                    row[0]['valori']["sconti"] = [{'tipo':"valore",
                                                'valore':float(value)},]
                    row[0]['valori']["prezzoNetto"]= row[6]
                else:
                    row[0]['valori']["sconti"] = [{'tipo':"valore",
                                                'valore':float(value)},]
                    row[0]['valori']["prezzoDettaglioScontato"]= row[6]


    def on_conferma_singolarmente_button_clicked(self,button):
        if self.TipoOperazione == "acquisto":
            self.articoloPadreDict['valori']['prezzoLordo']=self.price_entry.get_text()
        else:
            self.articoloPadreDict['valori']['prezzoDettaglio']=self.price_entry.get_text()
        resultList= []
        for row in self._treeViewModel:
            if row[0]['quantita'] == "0" or row[0]['quantita'] == "":
                continue
            else:
                resultList.append(row[0])
        #Environment.tagliacoloretempdata= (False, resultList)
        self.mainWindow.tagliaColoreRigheList = resultList
        self.mainWindow.promowear_manager_taglia_colore_togglebutton.set_active(False)
        self.destroy()


    def on_cancel_button_clicked(self, button):
        self.mainWindow.promowear_manager_taglia_colore_togglebutton.set_active(False)
        resultList = []
        Environment.tagliacoloretempdata= (True, resultList)
        self.destroy()
