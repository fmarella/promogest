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

from sets import Set

from promogest.ui.GladeWidget import GladeWidget

from promogest import Environment
from promogest.dao.Dao import Dao
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from promogest.dao.ListinoComplessoArticoloPrevalente import ListinoComplessoArticoloPrevalente
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *


class CrossFilterPriceList(GladeWidget):

    def __init__(self, listino):
        GladeWidget.__init__(self, root='cross_filter_pricelist',
                            path='cross_filter_pricelist.glade')

        dialog = self.cross_filter_pricelist
        self.placeWindow(self.getTopLevel())
        self._treeViewModel = None
        self._listino = listino
        self.rowBackGround = '#E6E6FF'
        self.rowBoldFont = 'arial bold 12'
        #self.duplicatedData()
        self.duprow = []
        self.stored = []
        self.draw()
        self.remove=None
        #self.refreshDuplicated()

    def draw(self):
        """
            Creo tre treeview , degli articoli duplicati, delle opzioni e di quelli
            gestiti
        """
        self.ok_button.set_sensitive(True)
        self.ok_button.set_property("visible",True)
        self._treeViewModel_duplicated = self.duplicated_listore
        self._treeViewModel_option = self.option_listore
        self.refreshFiltered()

    def riempiTreeview(self,l, treeview):
        """
            tutte le treeview hanno la stessa liststore,
            funzione di riempiriga
        """
        treeview.append((l,
                        (l.denominazione or ''),
                        (l.codice_articolo or ''),
                        (l.articolo or ''),
                        dateToString(l.data_listino_articolo),
                        str(mN(l.prezzo_dettaglio) or 0),
                        str(mN(l.prezzo_ingrosso) or 0)))


    def refreshFiltered(self, dao=None, remove=None):
        """
            Aggiornamento TreeView degli articoli già gestiti
        """
        if dao:
            l = dao
            self.riempiTreeview(l, self.filtered_listore)
        elif remove:
            self.filtered_listore.clear()
            for l in self.stored:
                if l == remove:
                    pass
                else:
                    self.riempiTreeview(l, self.filtered_listore)
        elif not self.stored:
            self.stored = self.filteredData()
            self._treeViewModel_option.clear()
            if not self.stored:
                self.refreshDuplicated()
                return
            for l in self.stored:
                self.riempiTreeview(l, self.filtered_listore)


    def refreshDuplicated(self,stored=[]):
        """
            Aggiornamento TreeView degli articoli duplicati
        """
        self.duplicated_listore.clear()
        if not self.duprow:
            self.duprow = self.duplicatedData()
        for l in self.duprow:
            if l in self.stored:
                pass
            else:
                self.riempiTreeview(l,self.duplicated_listore)


    def refreshOption(self, daos=None):
        """
            Aggiornamento TreeView delle opzioni possibili
        """
        self.option_listore.clear()
        for l in daos:
            self.riempiTreeview(l,self.option_listore)

    def duplicatedData(self):
        """
            crea la lista dei Dao listinoArticolo degli articoli duplicati
        """
        sottolistini = self._listino._sottoListiniIDD()
        dueid = []

        allArt= ListinoArticolo().select(idListino = sottolistini,listinoAttuale=True, batchSize=None)
        dupli2 = []
        if allArt:
            for a in allArt:
                dueid.append(a.id_articolo)
            dupli = [ x for x in dueid if dueid.count(x) > 1]
            dupli = list(set(dupli))
            if dupli:
                for art in dupli:
                    for l in sottolistini:
                        d = ListinoArticolo().select(idListino = l,listinoAttuale=True,
                                    idArticolo = art,
                                    batchSize=None,
                                    orderBy=ListinoArticolo.data_listino_articolo)
                        if d:
                            dupli2.append(d[-1])
        return dupli2 or []

    def filteredData(self):
        """
            Crea la lista di Dao Listino articolo degli articoli già gestiti
            prelevati dal DB ListinoComplessoArticoloPrevalente
        """
        filtrow =[]
        lcaps = ListinoComplessoArticoloPrevalente().select(idListinoComplesso=self._listino.id, batchSize=None)
        if lcaps:
            for lc in lcaps:
                riga= ListinoArticolo().select(idListino=lc.id_listino,
                                    idArticolo=lc.id_articolo,
                                    listinoAttuale = True,
                                    #dataListinoArticolo=lc.data_listino_articolo,
                                    batchSize=None)
                if riga:
                    filtrow.append(riga[0])
        return filtrow

    def on_filtered_treeview_row_activated(self, widget, path, column): #quello in alto
        model = self.filtered_listore
        dao = model[path][0]
        self.remove = dao
        self.refreshFiltered(remove=dao)
        daos = ListinoArticolo().select(idArticolo=dao.id_articolo,idListino =self._listino.sottoListiniID,listinoAttuale=True, batchSize=None)
        self.optionData(daos)

    def on_duplicated_treeview_row_activated(self, widget, path, column): # quello in basso
        model = self.duplicated_listore
        dao = model[path][0]
        daos = ListinoArticolo().select(idArticolo=dao.id_articolo,idListino=self._listino.sottoListiniID,listinoAttuale=True, batchSize=None)
        self.optionData(daos)

    def on_option_treeview_row_activated(self, widget, path, column): #quello in centro
        self.on_allocation_button_clicked(widget)

    def optionData(self, daos):
        self.refreshOption(daos)

    def on_column_selected_edited(self, cell, path, treeview,value, editNext=True):
        """ Function ti set the value quantita edit in the cell"""
        model = treeview.get_model()
        model[path][1] = not model[path][1]
        #self.option_treeview.clear()

    def on_cancel_button_clicked(self, button):
        self.destroy()

    def on_azzera_button_clicked(self, button):
        self.option_listore.clear()
        self.duplicated_listore.clear()
        self.filtered_listore.clear()
        lcaps = ListinoComplessoArticoloPrevalente().select(idListinoComplesso=self._listino.id, batchSize=None)
        for row in lcaps:
            Environment.session.delete(row)
        Environment.session.commit()
        self.stored = []
        self.duprow = []
        self.refreshDuplicated()

    def on_allocation_button_clicked(self, button):
        """
            gestiamo la selezione dell'articolo tra le diverse opzioni
        """
        sel = self.option_treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.rigaIter = model[iterator]
        row = self.rigaIter[0]

        self.refreshFiltered(row)
        for r in self.option_listore:
            self.stored.append(r[0])

        self.option_listore.clear()
        if not self.remove:
            self.refreshDuplicated(stored=self.stored)
            residui= len(self.duplicated_listore)
        else:
            residui = 0
        #if residui==0:
            #self.ok_button.set_sensitive(True)
            #self.ok_button.set_property("visible",True)

    def on_ok_button_clicked(self, button):
        if ListinoComplessoArticoloPrevalente().select(idListinoComplesso= self._listino.id, batchSize=None):
            for a in ListinoComplessoArticoloPrevalente().select(idListinoComplesso= self._listino.id, batchSize=None):
                a.delete()
        for r in self.filtered_listore:
            lcap=  ListinoComplessoArticoloPrevalente()
            lcap.id_listino_complesso = self._listino.id
            lcap.id_listino = r[0].id_listino
            lcap.id_articolo = r[0].id_articolo
            lcap.data_listino_articolo = r[0].data_listino_articolo
            lcap.persist()
        self.destroy()
