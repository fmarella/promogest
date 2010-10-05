# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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

import gtk
import gobject
from GladeWidget import GladeWidget

from promogest import Environment
#from promogest.dao.Dao import Dao
#import promogest.dao.Listino
from promogest.dao.Listino import Listino

from utils import *



class ElencoListini(GladeWidget):
    """ Elenco listini """

    def __init__(self, mainWindow, aziendaStr):
        self._mainWindow = mainWindow
        self.aziendaStr = aziendaStr
        self._currentDao = None
        GladeWidget.__init__(self, 'elenco_listini_frame', fileName='_elenco_listini_elements.glade')
        self.orderBy = 'denominazione'
        self.draw()


    def draw(self):
        # Colonne della Treeview dell' elenco
        treeview = self.elenco_listini_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'descrizione')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data listino', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'data_listino')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)

        model = gtk.ListStore(object, str, str, str)
        treeview.set_model(model)

        self.refresh()


    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura dell'elenco """
        self._elenco_listini_elements.show_all()


    def refresh(self):
        # Aggiornamento Treeview
        model = self.elenco_listini_treeview.get_model()
        model.clear()

        liss = Listino().select(orderBy='denominazione',
                                            batchSize=None,
                                            offset=None)
        if (not "pan" in Environment.modulesList) and \
            (not "basic" in  Environment.modulesList) and \
                Listino().count() >1 \
                and Environment.tipodb =="sqlite"\
                and not Environment.listini:
            if len(liss) >1:
                liss = [liss[0]]
        for l in liss:
            model.append((l,
                          (l.denominazione or ''),
                          (l.descrizione or ''),
                          dateToString(l.data_listino)))


    def _changeOrderBy(self, widget, campi):
        print "CAMBI L'ORDINE", campi
        self.orderBy = campi
        self.refresh()


    def on_elenco_listini_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            self._currentDao = model.get_value(iterator,0)


    def on_elenco_listini_treeview_row_activated(self, treeview, path, column):
        self.articoli_listino_togglebutton.set_active(True)


    def on_stampa_frontaline_togglebutton_clicked(self, toggleButton):
        if ("Label" in Environment.modulesList) or \
            ("pan" in Environment.modulesList):
            from promogest.modules.Label.ui.ManageLabelsToPrint import ManageLabelsToPrint
            a = ManageLabelsToPrint(mainWindow=self,daos=[])
            anagWindow = a.getTopLevel()
            returnWindow = self.getTopLevel().get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.show_all()
        else:
            fenceDialog()

    def on_listini_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        denominazione = None
        if self._currentDao is not None:
            denominazione = self._currentDao.denominazione
        from AnagraficaListini import AnagraficaListini
        anag = AnagraficaListini(denominazione, self.aziendaStr)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self._mainWindow, anagWindow, toggleButton, self.refresh)


    def on_articoli_listino_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        idListino = None
        if self._currentDao is not None:
            idListino = self._currentDao.id
        from AnagraficaListiniArticoli import AnagraficaListiniArticoli
        anag = AnagraficaListiniArticoli(None, idListino, self.aziendaStr)
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self._mainWindow, anagWindow, toggleButton, self.refresh)

    def on_importazione_listini_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if ("ImportPriceList" in Environment.modulesList) or \
            ("pan" in Environment.modulesList):
            from promogest.modules.ImportPriceList.ui.ImportPriceList import ImportPriceList
            idListino = None
            if self._currentDao:
                idListino = self._currentDao.id
            anag = ImportPriceList(self._mainWindow)
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(self._mainWindow, anagWindow, toggleButton)
        else:
            fenceDialog()
            toggleButton.set_active(False)
