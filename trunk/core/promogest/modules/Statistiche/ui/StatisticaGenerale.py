# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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

import os
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
from promogest.ui.gtk_compat import *
from promogest.dao.DaoUtils import *
from promogest.lib.HtmlViewer import HtmlViewer
from promogest.lib.relativedelta import relativedelta


class StatisticaGenerale(GladeWidget):
    """ Questa classe nasce con l'intenzione di gestire una interfaccia di
    creazione delle statistiche più generale possibile,per il momento ne
    gestisce una
    TODO: Scorporare la parte logica dalla gestione della pura interfaccia
    """
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
        """ Disegnamo le colonne della treeview delle statistiche """
        self.treeview = self.show_treeview

        cellspin = gtk.CellRendererToggle()
        cellspin.set_property('activatable', True)
        cellspin.connect('toggled', self.on_column_selected_edited, self.treeview, True)
        column = gtk.TreeViewColumn('Seleziona', cellspin)
        column.add_attribute( cellspin, "active", 1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_resizable(True)
        self.treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Descrizione', renderer, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
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

    def on_column_selected_edited(self, cell, path, treeview,value, editNext=True):
        """ Function to set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][1] = not model[path][1]
        for a in  model[path].iterchildren():
             a[1] = model[path][1]

    def on_statistica_dialog_destroy(self, widget):
        self.a_data_entry.destroy()
        self.da_data_entry.destroy()
        self.getTopLevel().destroy()

    def on_ok_button_clicked(self, button):
        """ cb del bottone ELABORA """
        if posso("STA"):
            self.exportss(self)
        else:
            fenceDialog()

    def on_tutti_button_clicked(self, button):
        for m in self._treeViewModel:
            m[1] = True

    def on_nessuno_button_clicked(self, button):
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
        """ cb del bottone magazzino """
        self._treeViewModel.clear()
        mag = Magazzino().select(batchSize=None)
        for c in mag:
            self._treeViewModel.append([c,False, c.denominazione])
        self.treeview.set_model(self._treeViewModel)

    def on_famiglia_articolo_clicked(self, button):
        return

    def on_aggiungi_regola_button_clicked(self, button):
        """ cb del bottone aggiungi regola """
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
        # Prelevo i dati dalla ui
        daData = stringToDate(self.da_data_entry.get_text())
        aData = stringToDate(self.a_data_entry.get_text())
        produt = self.produttore_entry.get_text()
        # Id dei clienti
        clienti = ClienteCategoriaCliente().select(idCategoria = self.cateClienteId, batchSize=None)
        for cli in clienti:
            idsCliente.append(cli.id_cliente)

        # id degli articoli
        articoli = Articolo().select(idCategoria = self.cateArticoloId,
                                    produttore = produt,  batchSize=None)
        for art in articoli:
            idsArticoli.append(art.id)
        # inizializzo un po' di variabili e dizionari
        quantitaVendutaDict = {}
        quantitaAcquistata = 0
        quantitaAcquistataTotale = 0
        valoreAcquistoDict= {}
        valoreAcquisto = 0
        quantitaVenduta = 0
        quantitaVendutaTotale = 0
        valoreAcquistoTotale= 0
        valoreVenditaDict = {}
        valoreVendita = 0
        valoreVenditaTotale = Decimal("0")
        ricaricomedioDict = {}
        incidenzaAcquistoDict = {}
        incidenzaVenditaDict = {}

        # smisto i dati  secondo categoriaArticolo
        print " ID CATEGORIE", self.cateArticoloId
        for arto in self.cateArticoloId:
            # INIZIO livello categoria
            nomeCategoria = CategoriaArticolo().getRecord(id=arto)
            articoli = Articolo().select(idCategoria = arto,
                                    produttore = produt,  batchSize=None)
            print "ARTICOLI IN QUELLA CATEGORIA", len(articoli)
            for art in articoli:
                # INIZIO livello articolo
                print "INIZIO AD ELABORARE L'ARTICOLO ", art.id
                quantitaVendutaUNO = 0
                quantitaVendutaTotaleUNO = 0
                quantitaAcquistataUNO = 0
                quantitaAcquistataTotaleUNO = 0
                # tutte le righe movimento per la vendita
                righeArticoloMovimentate= Environment.params["session"]\
                    .query(RigaMovimento, TestataMovimento)\
                    .filter(TestataMovimento.data_movimento.between(daData, aData))\
                    .filter(TestataMovimento.id_cliente.in_(idsCliente))\
                    .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                    .filter(Riga.id_magazzino.in_(self.magazzinoId))\
                    .filter(Riga.id_articolo == art.id)\
                    .all()
                print "RIGHE DI MOVIMENTO VENDITA", righeArticoloMovimentate
                for  rig in righeArticoloMovimentate:
                    # Quanti ne ho venduti IN TOTALE

                    quantitaVendutaUNO += rig[0].quantita
                    quantitaVendutaTotaleUNO += rig[0].quantita
                    quantitaVendutaTotale += rig[0].quantita


                    quantitaAcquistataUNO = 0
                    rigaArticoloMovimentata= Environment.params["session"]\
                                .query(RigaMovimento, TestataMovimento)\
                                .filter(TestataMovimento.data_movimento.between(daData+relativedelta(months=-4), aData))\
                                .filter(TestataMovimento.id_cliente == None)\
                                .filter(TestataMovimento.id_fornitore != None)\
                                .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                                .filter(Riga.id_magazzino.in_(self.magazzinoId))\
                                .filter(Riga.id_articolo == art.id)\
                                .all()
                    print "RIGHE DI MOVIMENTO ACQUISTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", rigaArticoloMovimentata
                    if not rigaArticoloMovimentata:
                        forni=  leggiFornitura(art.id)
                        valoreAcquisto += (forni["prezzoNetto"]*quantitaVendutaUNO)
                        valoreAcquistoTotale += (forni["prezzoNetto"]*quantitaVendutaUNO)
                        print " PREZZO DA FORNITURA"
                    else:
#                        for r in rigaArticoloMovimentata:
                            valoreAcquisto += (rigaArticoloMovimentata[0][0].valore_unitario_netto*quantitaVendutaUNO)
                            valoreAcquistoTotale += (rigaArticoloMovimentata[0][0].valore_unitario_netto*quantitaVendutaUNO)

                            quantitaAcquistataUNO += rigaArticoloMovimentata[0][0].quantita
                            quantitaAcquistataTotaleUNO += rigaArticoloMovimentata[0][0].quantita
    #                        quantitaAcquistataTotale += r[0].quantita
                    print " VALORE ACQUISTO", valoreAcquisto

                    ope = leggiOperazione(rig[1].operazione)
                    if ope["fonteValore"] =="vendita_iva":
                    # devo scorporare l'iva dal prezzo finale di vendita
                        imponibile = Decimal(str(float(rig[0].valore_unitario_netto)/(1+float(rig[0].percentuale_iva)/100)))
                    elif ope["fonteValore"] =="vendita_senza_iva":
                        imponibile = Decimal(str(float(rig[0].valore_unitario_netto)))
                    else:
                        print "TIPO DI FONTE VALORE PER LA VENDITA NN RICONOSCIUTO"
                    valoreVendita += (imponibile*quantitaVendutaUNO)
                    valoreVenditaTotale += (imponibile*quantitaVendutaUNO)



                    # QUESTO LIVELLO ARTICOLO

                if quantitaVendutaTotaleUNO <= quantitaAcquistataTotaleUNO:
                    print "ARTICOLO %s OK", str(art.id), quantitaVendutaTotaleUNO,quantitaAcquistataTotaleUNO
                else:
                    print " SERVE TROVARE UN PREZZO ACQUISTO", str(art.id),quantitaVendutaTotaleUNO,quantitaAcquistataTotaleUNO

            # Questo livello categoria
            quantitaVenduta =+quantitaVendutaTotale
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
        # Questo livello fuori da tutto
        for k,v in valoreVenditaDict.items():
            if v:
                incidenzaVenditaDict[k] = v*100 / valoreVenditaTotale
            else:
                incidenzaVenditaDict[k]  = 0
        for k,v in valoreAcquistoDict.items():
            if v:
                incidenzaAcquistoDict[k] = v*100 / valoreAcquistoTotale
            else:
                incidenzaAcquistoDict[k] = 0

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
