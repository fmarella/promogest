# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
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
from promogest.ui.utils import *
from promogest.ui.gtk_compat import *


class CrossFilterPriceList(GladeWidget):

    def __init__(self, listino):
        GladeWidget.__init__(self, 'cross_filter_pricelist',
                            'cross_filter_pricelist.glade')

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
        #parte dei duplicati
        treeview_duplicated = self.duplicated_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'id_listino')
        column.set_resizable(False)
        column.set_expand(True)
        column.set_min_width(250)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'codice_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'id_articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Data variazione', rendererSx, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'data_listino_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio', rendererDx, text=5)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_dettaglio')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_duplicated.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso', rendererDx, text=6)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_ingrosso')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_duplicated.append_column(column)
        self._treeViewModel_duplicated = gtk.ListStore(object, str, str, str, str, str, str)
        treeview_duplicated.set_model(self._treeViewModel_duplicated)

        #parte delle opzioni possibili
        treeview_option = self.option_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'id_listino')
        column.set_resizable(False)
        column.set_expand(True)
        column.set_min_width(250)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'codice_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'id_articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Data variazione', rendererSx, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'data_listino_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio', rendererDx, text=5)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_dettaglio')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_option.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso', rendererDx, text=6)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_ingrosso')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_option.append_column(column)

        self._treeViewModel_option = gtk.ListStore(object, str, str, str, str, str, str)
        treeview_option.set_model(self._treeViewModel_option)

        #parte degli articoli filtrati
        treeview_filtered = self.filtered_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'id_listino')
        column.set_resizable(False)
        column.set_expand(True)
        column.set_min_width(250)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'codice_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, 'id_articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Data variazione', rendererSx, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'data_listino_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio', rendererDx, text=5)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_dettaglio')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_filtered.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso', rendererDx, text=6)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, 'prezzo_ingrosso')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview_filtered.append_column(column)

        self._treeViewModel_filtered = gtk.ListStore(object, str, str, str, str, str, str)
        treeview_filtered.set_model(self._treeViewModel_filtered)

        self.refreshFiltered()

    def riempiTreeview(self,l, treeview):
        """
            tutte le treeview hanno la stessa liststore, funzione di riempiriga
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
        #self._treeViewModel_option.clear()
        if dao:
            l = dao
            self.riempiTreeview(l, self._treeViewModel_filtered)
        elif remove:
            self._treeViewModel_filtered.clear()
            for l in self.stored:
                if l == remove:
                    pass
                else:
                    self.riempiTreeview(l, self._treeViewModel_filtered)
        elif not self.stored:
            self.stored = self.filteredData()
            self._treeViewModel_option.clear()
            if not self.stored:
                self.refreshDuplicated()
                return
            for l in self.stored:
                self.riempiTreeview(l, self._treeViewModel_filtered)


    def refreshDuplicated(self,stored=[]):
        """
            Aggiornamento TreeView degli articoli dupplicati
        """
        self._treeViewModel_duplicated.clear()
        if not self.duprow:
            self.duprow = self.duplicatedData()
        for l in self.duprow:
            if l in self.stored:
                pass
            else:
                self.riempiTreeview(l,self._treeViewModel_duplicated)


    def refreshOption(self, daos=None):
        """
            Aggiornamento TreeView delle opzioni possibili
        """
        self._treeViewModel_option.clear()
        for l in daos:
            self.riempiTreeview(l,self._treeViewModel_option)

    def duplicatedData(self):
        """
            crea la lista dei Dao listinoArticolo degli articoli duplicati
        """
        sottolistini = self._listino.sottoListiniID
        dueid = []

        allArt= ListinoArticolo().select(idListino = sottolistini, batchSize=None)
        dupli2 = []
        if allArt:
            for a in allArt:
                dueid.append(a.id_articolo)
            dupli = [ x for x in dueid if dueid.count(x) > 1]
            if dupli:
                dupli2 = ListinoArticolo().select(idListino = sottolistini, idArticolo = dupli, batchSize=None)
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
                                    batchSize=None)[0]
                filtrow.append(riga)
        return filtrow

    def on_filtered_treeview_row_activated(self, widget, path, column):
        model = self.filtered_treeview.get_model()
        dao = model[path][0]
        self.remove = dao
        self.refreshFiltered(remove=dao)
        daos = ListinoArticolo().select(idArticolo=dao.id_articolo, batchSize=None)
        self.optionData(daos)

    def on_duplicated_treeview_row_activated(self, widget, path, column):
        model = self.duplicated_treeview.get_model()
        dao = model[path][0]
        daos = ListinoArticolo().select(idArticolo=dao.id_articolo, batchSize=None)
        self.optionData(daos)

    def on_option_treeview_row_activated(self, widget, path, column):
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
        self._treeViewModel_option.clear()
        self._treeViewModel_duplicated.clear()
        self._treeViewModel_filtered.clear()
        lcaps = ListinoComplessoArticoloPrevalente().select(idListinoComplesso=self._listino.id, batchSize=None)
        for row in lcaps:
            row.delete()
        self.stored = []
        self.duprow = []
        self.refreshDuplicated()

    def on_allocation_button_clicked(self, button):
        """
            gestiamo la selezione dell'articolo tra le diverse opzioni
        """
        selected = self.option_treeview.get_selection()
        row_model = selected.get_selected()
        row = row_model[0].get_value(row_model[1], 0)

        self.refreshFiltered(row)
        rows = self.option_treeview.get_model()
        for r in rows:
            self.stored.append(r[0])

        self._treeViewModel_option.clear()
        if not self.remove:
            self.refreshDuplicated(stored=self.stored)
            residui= len(self.duplicated_treeview.get_model())
        else:
            residui = 0
        if residui==0:
            self.ok_button.set_sensitive(True)
            self.ok_button.set_property("visible",True)

    def on_ok_button_clicked(self, button):
        goodrows = self.filtered_treeview.get_model()
        if ListinoComplessoArticoloPrevalente().select(idListinoComplesso= self._listino.id, batchSize=None):
            for a in ListinoComplessoArticoloPrevalente().select(idListinoComplesso= self._listino.id, batchSize=None):
                a.delete()
        for r in goodrows:
            lcap=  ListinoComplessoArticoloPrevalente()
            lcap.id_listino_complesso = self._listino.id
            lcap.id_listino = r[0].id_listino
            lcap.id_articolo = r[0].id_articolo
            lcap.data_listino_articolo = r[0].data_listino_articolo
            lcap.persist()
        self.destroy()

