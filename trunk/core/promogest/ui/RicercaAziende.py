# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from promogest.ui.Ricerca import Ricerca, RicercaFilter
from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Azienda
from promogest.dao.Azienda import Azienda

from promogest.lib.utils import *
from promogest.ui.gtk_compat import *


class RicercaAziende(Ricerca):
    """ Ricerca azienda """

    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca aziende',
                         RicercaAziendeFilter(self))
        self.inserimento_togglebutton.set_sensitive(False)
        #self.ricerca_html.destroy()

    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza
        pass


class RicercaAziendeFilter(RicercaFilter):
    """ Filtro per la ricerca delle aziende """

    def __init__(self, ricerca):
        RicercaFilter.__init__(self, ricerca,
                               root='anagrafica_aziende_filter_table',
                               path='_anagrafica_aziende_elements.glade')

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

        self.numRecords = Azienda().count(denominazione=denominazione)

        self._refreshPageCount()

        azis = Azienda().select(orderBy=self.orderBy,
                                            denominazione=denominazione,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        model = gtk.ListStore(object, str, str, str)

        for a in azis:
            model.append((a,
                          (a.denominazione or ''),
                          (a.sede_operativa_indirizzo or ''),
                          (a.sede_operativa_localita or '')))

        self._ricerca.ricerca_filter_treeview.set_model(model)

    def on_filter_treeview_selection_changed(self, treeview):
        #TODO: <fmarl> da implementare
        pass
