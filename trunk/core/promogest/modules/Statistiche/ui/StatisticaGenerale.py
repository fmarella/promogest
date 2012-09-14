# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
try:
    from collections import OrderedDict
except:
    from promogest.lib.ordereddict import OrderedDict
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Riga import Riga
from promogest.dao.Articolo import Articolo
from promogest.dao.Cliente import Cliente
from promogest.dao.Magazzino import Magazzino
from promogest.dao.CategoriaCliente import CategoriaCliente
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.ClienteCategoriaCliente import ClienteCategoriaCliente
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *
from promogest.dao.DaoUtils import *
from promogest.lib.HtmlViewer import HtmlViewer
from promogest.lib.relativedelta import relativedelta
from promogest.dao.CachedDaosDict import CachedDaosDict


class StatisticaGenerale(GladeWidget):
    """ Questa classe nasce con l'intenzione di gestire una interfaccia di
    creazione delle statistiche più generale possibile,per il momento ne
    gestisce una
    TODO: Scorporare la parte logica dalla gestione della pura interfaccia
    """
    def __init__(self, idMagazzino=None, nome=""):

        GladeWidget.__init__(self, root='statistica_dialog',
                path='Statistiche/gui/statistiche_dialog.glade',
                isModule=True)
        self.placeWindow(self.getTopLevel())
        self.da_data_entry.set_text('01/01/' + Environment.workingYear)
        self.a_data_entry.set_text(dateToString(datetime.datetime.now()))
#        self._idMagazzino = idMagazzino
        self.da_data_entry.show_all()
        self.a_data_entry.show_all()

        tree_iter = self.tipo_statistica_combo.get_active_iter()
        if tree_iter != None:
            model = self.tipo_statistica_combo.get_model()
            self.nomestatistica = model[tree_iter][1]
        self.cateCliente = ["CATEGORIA CLIENTE", [], [],False, object]
        self.cateArticolo = ["CATEGORIA ARTICOLO", [], [],False, object]
        self.magazzino = ["MAGAZZINO", [], [], False, object]
        self.produttore = ["PRODUTTORE", [], [], False, str]
        self.cliente = ["CLIENTE", [], [], False, object]

        self.tipo_stat = 2 # CONTROLLO FATTURATO CLIENTI
        self.__setup_view(self.tipo_stat)

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

        self._treeViewModel = gtk.ListStore(object, bool, str, str)
        self.treeview.set_model(self._treeViewModel)
        self._refresh()

    def __setup_view(self, tipo):
        self.statistica_dialog.show_all()
        if tipo == 2:
            self.fornitore_button.hide()
        elif tipo == 4:
            self.produttore_button.hide()
            self.categoria_cliente_button.hide()
            self.famiglia_articolo.hide()
            self.categoria_articolo.hide()
            self.cliente_button.hide()
            self.magazzino_button.hide()
            self.checkbutton1.hide()
            self.ordine_fattu_radio.hide()
            self.ordine_alfa_radio.hide()

    def _refresh(self):
        datata = self.da_data_entry.get_text()
        adata= self.a_data_entry.get_text()

        buf= self.sommario_textview.get_buffer()
        line_count = buf.get_line_count()

        stringa ="""
        Stiamo per creare un REPORT relativo alla statistica: %s

        Questi sono parametri utilizzati:
        Arco temporale:
        DA DATA: %s  A DATA: %s

        Criteri di ricerca e selezione:

        """%(self.nomestatistica, datata, adata)

        if self.produttore[2]:
            stringa += "\n" + self.produttore[0] + ": " + ", ".join(self.produttore[2])
        if self.produttore[3]:
            stringa += "\n" + self.produttore[0] + ": " + "TUTTI"

        if self.magazzino[2]:
            stringa += "\n" + self.magazzino[0] + ": " + ", ".join(self.magazzino[2])
        if self.magazzino[3]:
            stringa += "\n" + self.magazzino[0] + ": " + "TUTTI"

        if self.cateCliente[2]:
            stringa += "\n" + self.cateCliente[0] + ": " + ", ".join(self.cateCliente[2])
        if self.cateCliente[3]:
            stringa += "\n" + self.cateCliente[0] + ": " + "TUTTI"
        if self.cateArticolo[2]:
            stringa += "\n" + self.cateArticolo[0] + ": " + ", ".join(self.cateArticolo[2])
        if self.cateArticolo[3]:
            stringa += "\n" + self.cateArticolo[0] + ": " + "TUTTI"
        if self.cliente[2]:
            stringa += "\n" + self.cliente[0] + ": " + ", ".join(self.cliente[2])
        if self.cliente[3]:
            stringa += "\n" + self.cliente[0] + ": " + "TUTTI"

        buf.set_text(stringa)
        self.stringa = stringa

        self.sommario_textview.set_buffer(buf)

    def on_column_selected_edited(self, cell, path, treeview,value, editNext=True):
        """ Function to set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][1] = not model[path][1]
        for a in  model[path].iterchildren():
             a[1] = model[path][1]
        if self._treeViewModel[0][3].lower() =="categoria cliente":
            self.cateCliente[3] = False
        elif self._treeViewModel[0][3].lower() == "categoria articolo":
            self.cateArticolo[3] = False
        elif self._treeViewModel[0][3].lower() == "magazzino":
            self.magazzino[3] = False
        elif self._treeViewModel[0][3].lower() == "cliente":
            self.cliente[3] = False
        elif self._treeViewModel[0][3].lower() == "produttore":
            self.produttore[3] = False


    def on_statistica_dialog_destroy(self, widget):
        self.a_data_entry.destroy()
        self.da_data_entry.destroy()
        self.getTopLevel().destroy()

    def on_ok_button_clicked(self, button):
        """ cb del bottone ELABORA """
        if posso("STA"):
            if self.tipo_stat == 1:
                self.calcolo_ricarico_medio_e_influenza_sulle_vendite()
            elif self.tipo_stat == 2:
                self.controllo_fatturato_clienti()
            elif self.tipo_stat == 4:
                pass
            elif self.tipo_stat == 3:
                messageInfo(msg=" ANCORA NON GESTITO")

        else:
            fenceDialog()

    def on_tutti_button_clicked(self, button):
        for m in self._treeViewModel:
            m[1] = True
        tipo = self._treeViewModel[0][3].lower()
        self.setStatus(tipo, True)

    def setStatus(self, tipo, bo):
        if  tipo == "categoria cliente":
            self.cateCliente[3] = bo
        if tipo == "categoria articolo":
            self.cateArticolo[3] = bo
        if tipo == "cliente":
            self.cliente[3] = bo
        if tipo == "produttore":
            self.produttore[3] = bo
        if tipo == "magazzino":
            self.magazzino[3] = bo


    def on_nessuno_button_clicked(self, button):
        for m in self._treeViewModel:
            m[1] = False
        tipo = self._treeViewModel[0][3].lower()
        self.setStatus(tipo, False)

    def on_categoria_cliente_button_clicked(self, button):
        self._treeViewModel.clear()
        cate = CategoriaCliente().select(batchSize=None)
        for c in cate:
            if c.denominazione in self.cateCliente[2] or self.cateCliente[3]:
                self._treeViewModel.append([c, True, c.denominazione, self.cateCliente[0]])
            else:
                self._treeViewModel.append([c, False, c.denominazione, self.cateCliente[0]])
        self.treeview.set_model(self._treeViewModel)

    def on_categoria_articolo_clicked(self, button):
        self._treeViewModel.clear()
        cate = CategoriaArticolo().select(batchSize=None)
        for c in cate:
            if c.denominazione in self.cateArticolo[2] or self.cateArticolo[3]:
                self._treeViewModel.append([c, True, c.denominazione, self.cateArticolo[0]])
            else:
                self._treeViewModel.append([c, False, c.denominazione, self.cateArticolo[0]])
        self.treeview.set_model(self._treeViewModel)

    def on_magazzino_button_clicked(self, button):
        """ cb del bottone magazzino """
        self._treeViewModel.clear()
        mag = Magazzino().select(batchSize=None)
        for c in mag:
            if c.denominazione in self.magazzino[2] or self.magazzino[3]:
                self._treeViewModel.append([c, True, c.denominazione, self.magazzino[0]])
            else:
                self._treeViewModel.append([c, False, c.denominazione, self.magazzino[0]])
        self.treeview.set_model(self._treeViewModel)

    def on_produttore_button_clicked(self, button):
        """ cb del bottone produttore """
        self._treeViewModel.clear()

        res = Environment.params['session'].query(
                Articolo.produttore).order_by(Articolo.produttore).distinct()
        for c in res:
            if c[0].strip() is not "" :
                if c[0] in self.produttore[2] or self.produttore[3]:
                    self._treeViewModel.append([c , True, c[0], self.produttore[0]])
                else:
                    self._treeViewModel.append([c , False, c[0], self.produttore[0]])
        self.treeview.set_model(self._treeViewModel)


    def  on_cliente_button_clicked(self, button):
        self._treeViewModel.clear()
        cli = Cliente().select(batchSize=None, orderBy="ragione_sociale")
        for c in cli:
            if c.ragione_sociale in self.cliente[2] or self.cliente[3]:
                self._treeViewModel.append([c, True, c.ragione_sociale,self.cliente[0]])
            else:
                self._treeViewModel.append([c, False, c.ragione_sociale,self.cliente[0]])
        self.treeview.set_model(self._treeViewModel)


    def on_famiglia_articolo_clicked(self, button):
        return


    def on_aggiungi_regola_button_clicked(self, button):
        """ cb del bottone aggiungi regola """
        if len(self._treeViewModel) > 0:
            if self._treeViewModel[0][3].lower() =="categoria cliente":
                self.cateCliente[1] = []
                self.cateCliente[2] = []
            elif self._treeViewModel[0][3].lower() == "categoria articolo":
                self.cateArticolo[1] = []
                self.cateArticolo[2] = []
            elif self._treeViewModel[0][3].lower() == "magazzino":
                self.magazzino[1] = []
                self.magazzino[2] = []
            elif self._treeViewModel[0][3].lower() == "cliente":
                self.cliente[1] = []
                self.cliente[2] = []
            elif self._treeViewModel[0][3].lower() == "produttore":
                self.produttore[1] = []
                self.produttore[2] = []



            for riga in self._treeViewModel:
                if riga[3].lower() =="categoria cliente":
                    if self.cateCliente[3]:
                        break
                    elif riga[1] == True:
                        self.cateCliente[1].append(riga[0])
                        self.cateCliente[2].append(riga[2])
                elif riga[3].lower() == "categoria articolo":
                    if self.cateArticolo[3]:
                        break
                    elif riga[1] == True:
                        self.cateArticolo[1].append(riga[0])
                        self.cateArticolo[2].append(riga[2])

                elif riga[3].lower() == "magazzino":
                    if self.magazzino[3]:
                        break
                    elif riga[1] == True:
                        self.magazzino[1].append(riga[0])
                        self.magazzino[2].append(riga[2])
                elif riga[3].lower() == "cliente":
                    if self.cliente[3]:
                        break
                    elif riga[1] == True:
                        self.cliente[1].append(riga[0])
                        self.cliente[2].append(riga[2])
                elif riga[3].lower() == "produttore":
                    if self.produttore[3]:
                        break
                    elif riga[1] == True:
                        self.produttore[1].append(riga[0])
                        self.produttore[2].append(riga[2])

        self._refresh()

    def on_tipo_statistica_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            self.tipo_stat = model[tree_iter][0]
        self.__setup_view(self.tipo_stat)

    def calcolo_ricarico_medio_e_influenza_sulle_vendite(self):
        idsCliente = []
        idsArticoli = []
        artiID = []
        intervallo = ''
        self.res = []
        # Prelevo i dati dalla ui
        daData = stringToDate(self.da_data_entry.get_text())
        aData = stringToDate(self.a_data_entry.get_text())

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

    def controllo_fatturato_clienti(self):
        #print "I CLIENTI", self.cliente
        clienti1 = []

        if self.cateCliente[3]:
            catesCli = CategoriaCliente().select(batchSize=None)
        else:
            catesCli = self.cateCliente[1]
        idcates = [x.id for x in catesCli]
        clie = [x.id_cliente for x in ClienteCategoriaCliente().select(idCategoria = idcates, batchSize=None)]
        for c in clie:
            clienti1.append(Cliente().getRecord(id=c))
        #print "clientiiiiiiiiiiiiiiiiiiiiiiiiii", clienti

        if self.cliente[3]:
            clienti2 = Cliente().select(batchSize=None)
        #elif not self.cliente[2]:
            #messageError(msg="NESSUN CLIENTE SELEZIONATO")
        else:
            clienti2 = self.cliente[1]
        clienti = clienti1+clienti2





        daData = stringToDate(self.da_data_entry.get_text())
        aData = stringToDate(self.a_data_entry.get_text())
        #print self.cateArticolo
        #print self.produttore

        diz = OrderedDict()
        cache = CachedDaosDict()
        for c in clienti:
            pbar(self.pbar,parziale=clienti.index(c), totale=len(clienti),text="GEN DATI", noeta = True)
            docu = TestataDocumento().select(idCliente = c.id,daData=daData, aData=aData, batchSize=None)
            rowDiz = OrderedDict()
            for d in docu:
                if d.operazione not in Environment.hapag:
                    continue
                for r in d.righe:
                    if r.id_articolo:
                        if r.id_articolo in rowDiz:
                            a = rowDiz[r.id_articolo]
                            a.append(r)
                        else:
                            rowDiz[r.id_articolo] = [r]

            artCatArt = []
            dizcate = OrderedDict()
            dizprod = OrderedDict()

            #Categorie Articolo
            if self.cateArticolo[3]:
                cates = CategoriaArticolo().select(batchSize=None)
            elif self.cateArticolo[1]:
                cates = self.cateArticolo[1]
            else:
                cates = []

            for cate in cates:
                artCatArt = Articolo().select(idCategoria= cate.id, batchSize=None)
                idArt = [x.id for x in artCatArt]
                pezzi = 0
                totRiga = 0
                for d in rowDiz:
                    categoria = Articolo().getRecord(id=d).denominazione_categoria
                    if d in idArt:
                        for cc in rowDiz[d]:
                            if str(cc.testata_movimento.opera.segno) == "-":
                                if cc.testata_movimento.opera.fonte_valore == "vendita_iva":
                                    # scorporo l'iva per avere tutti valori imponibili
                                    idAliquotaIva = cc.id_iva
                                    daoiva = cache['aliquotaiva'][idAliquotaIva][0]
                                    aliquotaIvaRiga = daoiva.percentuale
                                    totRigaImponibile = cc.valore_unitario_netto/(1+aliquotaIvaRiga/100)
                                    totRiga += totRigaImponibile
                                else:
                                    totRiga += cc.totaleRiga
                            pezzi += cc.quantita * cc.moltiplicatore
                        dizcate[categoria] = [totRiga,pezzi, categoria]
            #Produttore
            if self.produttore[3]:
                produts = Environment.params['session'].query(
                        Articolo.produttore).order_by(Articolo.produttore).distinct()
            elif self.produttore[1]:
                produts = self.produttore[1]
            else:
                produts = []

            for prod in produts:
                artProd = Articolo().select(produttoreEM=prod[0], batchSize=None)
                idArt = [x.id for x in artProd]
                pezzi = 0
                totRiga = 0
                for d in rowDiz:
                    if d in idArt:
                        for cc in rowDiz[d]:
                            if str(cc.testata_movimento.opera.segno) == "-":
                                if cc.testata_movimento.opera.fonte_valore == "vendita_iva":
                                    # scorporo l'iva per avere tutti valori imponibili
                                    idAliquotaIva = cc.id_iva
                                    daoiva = cache['aliquotaiva'][idAliquotaIva][0]
                                    aliquotaIvaRiga = daoiva.percentuale
                                    totRigaImponibile = cc.valore_unitario_netto/(1+aliquotaIvaRiga/100)
                                    totRiga += totRigaImponibile
                                else:
                                    totRiga += cc.totaleRiga
                            pezzi += cc.quantita * cc.moltiplicatore
                        dizprod[prod[0]] = [totRiga,pezzi, prod[0]]

            diz[c.id] = [c, calcolaTotali(docu, pbarr = self.pbarr), len(docu), dizcate, dizprod]
            #print "DIZZZZZZZZZZ", diz
        pbar(self.pbar,stop=True)
        pageData = {
                "file": "statistica_controllo_fatturato.html",
                "diz": diz,
                "nomestatistica":self.nomestatistica,
                "ricerca_stringa" : self.stringa.replace("\n","<br />"),

                }

        view = HtmlViewer(pageData)
