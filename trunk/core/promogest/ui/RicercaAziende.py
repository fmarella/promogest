# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>

import gtk
import gobject
from Ricerca import Ricerca, RicercaFilter

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Azienda
from promogest.dao.Azienda import Azienda

from utils import *


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
                               'anagrafica_aziende_filter_table',
                               fileName='_anagrafica_aziende_elements.glade')

    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._ricerca.ricerca_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Indirizzo', renderer,text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'indirizzo')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita', renderer,text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
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
