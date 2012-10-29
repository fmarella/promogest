# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 2011
#    by Promotux di Francesco Meloni snc - http://www.promotux.it/

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
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.DaoUtils import giacenzaArticolo, giacenzaDettaglio
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
        GladeWidget.__init__(self, root='dettaglio_giacenza_window',
                        path='dettaglio_giacenza_window.glade',
                        isModule=False)
        self.mainWindow = mainWindow
        self.idRiga = riga["idRiga"]
        self.quantita = riga["quantita"]
        self.idArticolo = riga["idArticolo"]
        self.idMagazzino = riga["idMagazzino"]
        self.rigamovimentofornituralist = riga["rigaMovimentoFornituraList"]
        #treeselection = self.dettaglio_giacenza_treeview.get_selection()
        #treeselection.set_mode(GTK_SELECTIONMODE_MULTIPLE)
        self.draw()

    def draw(self):
        """Creo una treeviewper la visualizzazione degli articoli che
            andranno poi in stampa
        """
        self.__refresh()

    def on_dg_ok_button_clicked(self,button):
        self.rigamovimentofornituralist = []
        sel = self.dettaglio_giacenza_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        riga = model[iterator]
        self.mainWindow._righe[0]["rigaMovimentoFornituraList"] = [riga[6]]
        self.getTopLevel().destroy()


    def __refresh(self):
        # Aggiornamento TreeView
        self.dettaglio_giacenza_listore.clear()
        rmf = RigaMovimentoFornitura().select(idArticolo=self.idArticolo, idRigaMovimentoAcquistoBool=True, batchSize=None)
        a = leggiArticolo(self.idArticolo)
        idForni = [ x.id_fornitura for x in rmf if x.id_fornitura]
        idForni = set(idForni)
        print len (rmf)
        for i in idForni:
            rmfv = RigaMovimentoFornitura().select(idArticolo=self.idArticolo, idFornitura=i, batchSize=None)
            quantita_evasa = 0
            quantita_totale = 0
            quantita_residua = 0
            for r in rmfv:
                #print r.__dict__  , r.rigamovven.quantita, quantita_evasa
                if r.id_riga_movimento_vendita:
                    quantita_evasa += r.rigamovven.quantita
                if r.id_riga_movimento_acquisto:
                    quantita_totale = r.rigamovacq.quantita
            quantita_residua = quantita_totale - quantita_evasa
            ff = Fornitura().getRecord(id=i)
            self.dettaglio_giacenza_listore.append((
                        str(mN(quantita_totale,1)) +" - " + str(mN(quantita_evasa,1)) + " - " + str(mN(quantita_residua,1)),
                        ff.numero_lotto,
                        dateToString(ff.data_fornitura),
                        dateToString(ff.data_scadenza),
                        dateToString(ff.data_produzione),
                        "",i))
        testo = a["codice"]+"-"+a["denominazione"] +"\n\n STAI VENDENDO " + str(int(self.quantita)) +" ARTICOLI \n CE NE SONO " + str(int(len(self.dettaglio_giacenza_listore)))
        self.articolo_info_label.set_text(testo)


    def on_column_quantita_edited(self, cell, path, value):
        """ Set the value "quantita" edit in the cell """
        value=value.replace(",",".")
        value = mN(value,1)
        self.dettaglio_giacenza_listore[path][0] = value


    def on_dg_annulla_button_clicked(self, button):
        self.getTopLevel().destroy()
