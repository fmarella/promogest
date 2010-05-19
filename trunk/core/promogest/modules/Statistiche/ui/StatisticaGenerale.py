# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>

import os
import gtk
import datetime
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Riga import Riga
from promogest.dao.Articolo import Articolo
from promogest.dao.Magazzino import Magazzino
from promogest.dao.CategoriaCliente import CategoriaCliente
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.ClienteCategoriaCliente import ClienteCategoriaCliente
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.DaoUtils import *
from promogest.lib.HtmlViewer import HtmlViewer


class StatisticaGenerale(GladeWidget):

    def __init__(self, idMagazzino=None, nome=""):

        GladeWidget.__init__(self, 'statistica_dialog',
                'Statistiche/gui/statistiche_dialog.glade',
                isModule=True)
        self.placeWindow(self.getTopLevel())
        self.da_data_entry.set_text('01/01/' + Environment.workingYear)
        self.a_data_entry.set_text(dateToString(datetime.datetime.now()))
#        self._idMagazzino = idMagazzino
        self.da_data_entry.show_all()
        self.a_data_entry.show_all()
        self.cateClienteId = []
        self.cateArticoloId = []
        self.magazzinoId = []
        self.cateClienteDen = []
        self.cateArticoloDen = []
        self.magazzinoDen = []
        self.magazzinoTutti = False
        self.cateArticoloTutti = False
        self.cateClienteTutti = False
        self.nomestatistica= nome
        self.draw()

    def draw(self):

        self.treeview = self.show_treeview

        cellspin = gtk.CellRendererToggle()
        cellspin.set_property('activatable', True)
        cellspin.connect('toggled', self.on_column_selected_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Seleziona', cellspin)
        column.add_attribute( cellspin, "active", 1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        self.treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Descrizione', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.treeview.append_column(column)

        self.treeview.set_search_column(2)

        self._treeViewModel = gtk.ListStore(object, bool, str)
        self.treeview.set_model(self._treeViewModel)
        self._refresh()


    def _refresh(self):
        datata = self.da_data_entry.get_text()
        adata= self.a_data_entry.get_text()
        produt = self.produttore_entry.get_text()
        buffer= self.sommario_textview.get_buffer()
        line_count = buffer.get_line_count()
        if not self.magazzinoTutti:
            maga = str(self.magazzinoDen)[1:-1]
        else:
            maga = "TUTTI"
        if not self.cateArticoloTutti:
            catea = str(self.cateArticoloDen)[1:-1]
        else:
            catea = "TUTTI"
        if not self.cateClienteTutti:
            catec = str(self.cateClienteDen)[1:-1]
        else:
            catec = "TUTTI"
        stringa ="""
        Stiamo per creare un CSV relativo alla statistica: %s
        Con i seguenti parametri di ricerca e filtraggio:
        DA DATA: %s
        A DATA: %s
        PRODUTTORE: %s
        MAGAZZINO: %s
        CATEGORIA CLIENTE: %s
        CATEGORIA ARTICOLO: %s
        CLIENTE : %s
        """%(self.nomestatistica, datata, adata, produt, maga, catec, catea,"")
        buffer.set_text(stringa)
        self.sommario_textview.set_buffer(buffer)
#        print buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter()), produt,line_count


    def on_column_selected_edited(self, cell, path, treeview,value, editNext=True):
        """ Function to set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][1] = not model[path][1]
        for a in  model[path].iterchildren():
             a[1] = model[path][1]
#        self.printModel()


    def on_statistica_dialog_destroy(self, widget):
        self.a_data_entry.destroy()
        self.da_data_entry.destroy()
        self.getTopLevel().destroy()
        #return

    def on_ok_button_clicked(self, button):
        self.exportss(self)

    def on_tutti_button_clicked(self, button):
#        model = self.treeview.get_model()
        for m in self._treeViewModel:
            m[1] = True

    def on_nessuno_button_clicked(self, button):
#        model = self.treeview.get_model()
        for m in self._treeViewModel:
            m[1] = False

    def on_categoria_cliente_button_clicked(self, button):
        self._treeViewModel.clear()
        cate = CategoriaCliente().select(batchSize=None)
        for c in cate:
            self._treeViewModel.append([c,False, c.denominazione])
        self.treeview.set_model(self._treeViewModel)

    def on_categoria_articolo_clicked(self, button):
        self._treeViewModel.clear()
        cate = CategoriaArticolo().select(batchSize=None)
        for c in cate:
            self._treeViewModel.append([c,False, c.denominazione])
        self.treeview.set_model(self._treeViewModel)

    def on_magazzino_button_clicked(self, button):
        self._treeViewModel.clear()
        mag = Magazzino().select(batchSize=None)
        for c in mag:
            self._treeViewModel.append([c,False, c.denominazione])
        self.treeview.set_model(self._treeViewModel)

    def on_famiglia_articolo_clicked(self, button):
        return

    def on_aggiungi_regola_button_clicked(self, button):
        if len(self._treeViewModel) > 0:
            if type(self._treeViewModel[0][0]).__name__ =="CategoriaCliente":
                self.cateClienteId=[]
                self.cateClienteDen=[]
                self.cateClienteTutti = True
            elif type(self._treeViewModel[0][0]).__name__ =="CategoriaArticolo":
                self.cateArticoloId = []
                self.cateArticoloDen = []
                self.cateArticoloTutti = True
            elif type(self._treeViewModel[0][0]).__name__ =="Magazzino":
                self.magazzinoId = []
                self.magazzinoDen = []
                self.magazzinoTutti = True
            for riga in self._treeViewModel:
                if type(riga[0]).__name__ =="CategoriaCliente" and riga[1] == True:
                    self.cateClienteId.append(riga[0].id)
                    self.cateClienteDen.append(str(riga[0].denominazione))
                elif type(riga[0]).__name__ =="CategoriaCliente" and riga[1] == False:
                    self.cateClienteTutti = False
                elif type(riga[0]).__name__ =="CategoriaArticolo" and riga[1] == True:
                    self.cateArticoloId.append(riga[0].id)
                    self.cateArticoloDen.append(str(riga[0].denominazione))
                elif type(riga[0]).__name__ =="CategoriaArticolo" and riga[1] == False:
                    self.cateArticoloTutti = False
                elif type(riga[0]).__name__ =="Magazzino" and riga[1] == True:
                    self.magazzinoId.append(riga[0].id)
                    self.magazzinoDen.append(str(riga[0].denominazione))
                elif type(riga[0]).__name__ =="Magazzino" and riga[1] == False:
                    self.magazzinoTutti = False
        self._refresh()

    def exportss(self, filename):
        idsCliente = []
        idsArticoli = []
        artiID = []
        intervallo = ''
        self.res = []
        daData = stringToDate(self.da_data_entry.get_text())
        aData = stringToDate(self.a_data_entry.get_text())
        produt = self.produttore_entry.get_text()

        clienti = ClienteCategoriaCliente().select(idCategoria = self.cateClienteId, batchSize=None)
        for cli in clienti:
            idsCliente.append(cli.id_cliente)

        articoli = Articolo().select(idCategoria = self.cateArticoloId,
                                    produttore = produt,  batchSize=None)
        for art in articoli:
            idsArticoli.append(art.id)

        quantitaVendutaDict = {}
        quantitaVenduta = 0
        valoreAcquistoDict= {}
        valoreAcquisto = 0
        quantitaVendutaTotale = 0
        valoreAcquistoTotale= 0
        valoreVenditaDict = {}
        valoreVendita = 0
        valoreVenditaTotale = 0
        ricaricomedioDict = {}
        incidenzaAcquistoDict = {}
        incidenzaVenditaDict = {}
        righeArticoloMovimentate= Environment.params["session"]\
                    .query(RigaMovimento, TestataMovimento)\
                    .filter(TestataMovimento.data_movimento.between(daData, aData))\
                    .filter(TestataMovimento.id_cliente.in_(idsCliente))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Riga.id_magazzino.in_(self.magazzinoId))\
                    .filter(Riga.id_articolo.in_(idsArticoli))\
                    .all()

        for arto in self.cateArticoloId:
            nomeCategoria = CategoriaArticolo().getRecord(id=arto)
            articoli = Articolo().select(idCategoria = arto,
                                    produttore = produt,  batchSize=None)
            for art in articoli:
                for  rig in righeArticoloMovimentate:
                    if art.id == rig[0].id_articolo:
                        forni=  leggiFornitura(art.id)
                        quantitaVenduta += rig[0].quantita
                        quantitaVendutaTotale += rig[0].quantita
                        valoreAcquisto += forni["prezzoNetto"]
                        valoreAcquistoTotale += forni["prezzoNetto"]
                        ope = leggiOperazione(rig[1].operazione)
                        if ope["fonteValore"] =="vendita_iva":
                            # devo scorporare l'iva dal prezzo finale di vendita
                            imponibile = Decimal(str(float(rig[0].valore_unitario_netto)/(1+float(rig[0].percentuale_iva)/100)))
                        elif ope["fonteValore"] =="vendita_senza_iva":
                            imponibile = Decimal(str(float(rig[0].valore_unitario_netto)))
                        else:
                            print "TIPO DI FONTE VALORE NN RICONOSCIUTO"
                        valoreVendita += imponibile
                        valoreVenditaTotale += imponibile
            if valoreAcquisto!=0:
                ricaricomedioDict[nomeCategoria.denominazione] = ((valoreVendita - valoreAcquisto )/ valoreAcquisto) *100
            else:
                ricaricomedioDict[nomeCategoria.denominazione] = 0
            quantitaVendutaDict[nomeCategoria.denominazione] = quantitaVenduta or Decimal("0")
            valoreAcquistoDict[nomeCategoria.denominazione] = valoreAcquisto or Decimal("0")
            valoreVenditaDict[nomeCategoria.denominazione] = valoreVendita or Decimal("0")
            quantitaVenduta = 0
            valoreAcquisto = 0
            valoreVendita = 0
        for k,v in valoreVenditaDict.items():
            incidenzaVenditaDict[k] = v*100 / valoreVenditaTotale
        for k,v in valoreAcquistoDict.items():
            incidenzaAcquistoDict[k] = v*100 / valoreAcquistoTotale
        print tempo()

        pageData = {
                "file": "statistica_ricarico_medio_e_influenza_vendite.html",
                "categorieArticolo": self.cateArticoloDen,
                "quantitaVendutaDict":quantitaVendutaDict,
                "valoreAcquistoDict":valoreAcquistoDict,
                "valoreVenditaDict":valoreVenditaDict,
                "ricaricomedioDict":ricaricomedioDict,
                "incidenzaVenditaDict": incidenzaVenditaDict,
                "incidenzaAcquistoDict": incidenzaAcquistoDict,
                "quantitaVendutaTotale": quantitaVendutaTotale,
                "valoreAcquistoTotale": valoreAcquistoTotale,
                "valoreVenditaTotale": valoreVenditaTotale,
                "daData": self.da_data_entry.get_text(),
                "aData":self.a_data_entry.get_text(),
                "produttore": produt,
                "cateclienti": self.cateClienteDen,
                "magazzini": self.magazzinoDen,
                "nomestatistica":self.nomestatistica}

        view = HtmlViewer(pageData)
        return
