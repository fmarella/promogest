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

from promogest.ui.Ricerca import Ricerca, RicercaFilter
from promogest import Environment
from promogest.dao.Magazzino import Magazzino
from promogest.ui.utils import *
from promogest.ui.gtk_compat import *


class RicercaMagazzini(Ricerca):
    """ Ricerca magazzini """

    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca magazzini',
                         RicercaMagazziniFilter(self))
        #self.ricerca_html.destroy()

    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza

        def refresh():
            self.filter.refresh()
            self.filter.denominazione_filter_entry.grab_focus()

        from promogest.ui.AnagraficaMagazzini import AnagraficaMagazzini
        anag = AnagraficaMagazzini()
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)

        anag.on_record_new_activate(anag.record_new_button)



class RicercaMagazziniFilter(RicercaFilter):
    """ Filtro per la ricerca dei magazzini """

    def __init__(self, ricerca):
        RicercaFilter.__init__(self, ricerca,
                               'anagrafica_magazzini_filter_table',
                               fileName='_anagrafica_magazzini_elements.glade')

    def on_filter_treeview_selection_changed(self, treeview):
        pass

    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._ricerca.ricerca_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Indirizzo', renderer,text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'indirizzo')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita', renderer,text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'localita')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self.clear()


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())

        self.numRecords = Magazzino().count(denominazione=denominazione)

        self._refreshPageCount()

        mags = Magazzino().select(orderBy=self.orderBy,
                                              denominazione=denominazione,
                                              offset=self.offset,
                                              batchSize=self.batchSize)


        model = gtk.ListStore(object, str, str, str)

        for m in mags:
            model.append((m,
                          (m.denominazione or ''),
                          (m.indirizzo or ''),
                          (m.localita or '')))

        self._ricerca.ricerca_filter_treeview.set_model(model)
