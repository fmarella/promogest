# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 2011
#by Promotux di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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

from decimal import *
from promogest.ui.gtk_compat import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.DaoUtils import giacenzaArticolo, giacenzaSel
from promogest.dao.Articolo import Articolo
from promogest.dao.Listino import Listino
from promogest.dao.Fornitura import Fornitura
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura

class DettaglioGiacenzaWindow(GladeWidget):

    def __init__(self, mainWindow=None,riga=None):
        """Widget di transizione per visualizzare e confermare gli oggetti
            preparati per la stampa ( Multi_dialog.glade tab 1)
        """
        GladeWidget.__init__(self, 'dettaglio_giacenza_window',
                        fileName= 'dettaglio_giacenza_window.glade',
                        isModule=False)
        self.mainWindow = mainWindow
        self.idRiga = riga["idRiga"]
        self.quantita = riga["quantita"]
        self.idArticolo = riga["idArticolo"]
        self.idMagazzino = riga["idMagazzino"]
        self.rigamovimentofornituralist = riga["rigaMovimentoFornituraList"]
        self.draw()

    def draw(self):
        """Creo una treeviewper la visualizzazione degli articoli che
            andranno poi in stampa
        """
        self.__refresh()

    #def selectFilter(self, model, path, iter):
        ##lista = []
        #check = model.get_value(iter, 1)
        #fatherPath = model.get_path(iter)
        #if check:
            #if len(fatherPath) ==1:
                #return
            #oggetto = model.get_value(iter, 0)
            #quantita = model.get_value(iter, 5)
            #for ogg in range(0,int(quantita)):
                #oggetto.codice_a_barre = model.get_value(iter, 4)
                #self.resultList.append(oggetto)

    #def get_active_text(self, combobox):
        #model = combobox.get_model()
        #active = combobox.get_active()
        #if active < 0:
            #return None
        #return model[active][0]

    def on_dg_ok_button_clicked(self,button):

        model = self.dettaglio_giacenza_listore
        for m in model:
            if m[0] and m[7] not in self.rigamovimentofornituralist:
                print "DA AGGIUNGERE", m, m[7]
                self.rigamovimentofornituralist.append(m[7])
        self.mainWindow._righe[0]["rigaMovimentoFornituraList"] = self.rigamovimentofornituralist
        self.getTopLevel().destroy()

    def on_selezionato_toggle_toggled(self, cell, path):
        """ Function to set the value quantita edit in the cell"""
        model = self.dettaglio_giacenza_listore
        model[path][0] = not model[path][0]

    def __refresh(self):
        # Aggiornamento TreeView
        self.dettaglio_giacenza_listore.clear()
        arti = RigaMovimentoFornitura().select(idArticolo=self.idArticolo, batchSize=None)
        print "artttttti", arti
        a = leggiArticolo(self.idArticolo)
        for i in arti:
            boleann = False
            if i.id_riga_movimento_vendita and self.idRiga == i.id_riga_movimento_vendita:
                boleann = True
            elif i.id_riga_movimento_vendita and self.idRiga != i.id_riga_movimento_vendita:
                print "CONTINUE"
                continue
            print  boleann
            idrigamov = RigaMovimento().getRecord(i.id_riga_movimento_acquisto)
            movi = TestataMovimento().getRecord(id= idrigamov.id_testata_movimento)
            if i in self.rigamovimentofornituralist:
                boleann = True
            self.dettaglio_giacenza_listore.append((boleann,
                                        i.forni.numero_lotto,
                                        dateToString(i.forni.data_scadenza),
                                        str(movi.numero),
                                        dateToString(i.forni.data_fornitura),
                                        dateToString(i.forni.data_produzione),
                                        "",i))
        print dir(self.dettaglio_giacenza_listore)
        testo = a["codice"]+"-"+a["denominazione"] +"\n\n STAI VENDENDO " + str(int(self.quantita)) +" ARTICOLI \n CE NE SONO " + str(int(len(self.dettaglio_giacenza_listore)))
        self.articolo_info_label.set_text(testo)

        ##self.dettaglio_giacenza_treeview.set_model(self.dettaglio_giacenza_listore)


    def on_dg_annulla_button_clicked(self, button):
        self.getTopLevel().destroy()
