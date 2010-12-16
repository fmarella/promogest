# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>


import gtk
import gobject
from Visualizzazione import Visualizzazione, VisualizzazioneFilter

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Fornitura
from promogest.dao.Fornitura import Fornitura

from utils import *



class StoricoForniture(Visualizzazione):
    """ Visualizzazione forniture """

    def __init__(self, idArticolo = None, idFornitore = None,
                       daDataFornitura = None, aDataFornitura = None,
                       daDataPrezzo = None, aDataPrezzo = None,
                       codiceArticoloFornitore = None):
        self._idArticolo = idArticolo
        self._idFornitore = idFornitore
        Visualizzazione.__init__(self, 'Promogest - Visualizzazione storico prezzi di costo',
                                       StoricoFornitureFilter(self))



class StoricoFornitureFilter(VisualizzazioneFilter):
    """ Filtro per la visualizzazione delle forniture """

    def __init__(self, visualizzazione):
        VisualizzazioneFilter.__init__(self, visualizzazione,
                                         'anagrafica_forniture_filter_table')
        self.orderBy = 'data_prezzo'

    def on_filter_treeview_selection_changed(self, treeview):
        pass

    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._visualizzazione.visualizzazione_filter_treeview

        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
#        column.set_clickable(True)
#        column.connect("clicked", self._changeOrderBy, ("Articolo", 'codice_articolo'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Denominazione', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
#        column.set_clickable(True)
#        column.connect("clicked", self._changeOrderBy, ("Articolo", 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo lordo', rendererDx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'prezzo_lordo'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo Netto', rendererDx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'prezzo_netto'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data prezzo', rendererSx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'data_prezzo'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data fornitura', rendererSx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'data_fornitura'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice fornitore', rendererSx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'codice_fornitore'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ragione sociale', rendererSx, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'fornitore'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', rendererSx, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'codice_articolo_fornitore'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str)
        self._visualizzazione.visualizzazione_filter_treeview.set_model(self._treeViewModel)

        self.id_articolo_filter_customcombobox.setId(self._visualizzazione._idArticolo)
        self.id_fornitore_filter_customcombobox.setId(self._visualizzazione._idFornitore)

        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.id_articolo_filter_customcombobox.set_active(0)
        self.id_fornitore_filter_customcombobox.set_active(0)
        self.da_data_fornitura_filter_entry.set_text('')
        self.a_data_fornitura_filter_entry.set_text('')
        self.da_data_prezzo_filter_entry.set_text('')
        self.a_data_prezzo_filter_entry.set_text('')
        self.codice_articolo_fornitore_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self.id_articolo_filter_customcombobox.getId()
        idFornitore = self.id_fornitore_filter_customcombobox.getId()
        daDataFornitura = stringToDate(self.da_data_fornitura_filter_entry.get_text())
        aDataFornitura = stringToDate(self.a_data_fornitura_filter_entry.get_text())
        daDataPrezzo = stringToDate(self.da_data_prezzo_filter_entry.get_text())
        aDataPrezzo = stringToDate(self.a_data_prezzo_filter_entry.get_text())
        codiceArticoloFornitore = prepareFilterString(self.codice_articolo_fornitore_filter_entry.get_text())

        self.numRecords = Fornitura().count(idArticolo=idArticolo,
                                                        idFornitore=idFornitore,
                                                        daDataFornitura=daDataFornitura,
                                                        aDataFornitura=aDataFornitura,
                                                        daDataPrezzo=daDataPrezzo,
                                                        aDataPrezzo=aDataPrezzo,
                                                        codiceArticoloFornitore=codiceArticoloFornitore)

        self._refreshPageCount()

        fors = Fornitura().select(orderBy=self.orderBy,
                                              idArticolo=idArticolo,
                                              idFornitore=idFornitore,
                                              daDataFornitura=daDataFornitura,
                                              aDataFornitura=aDataFornitura,
                                              daDataPrezzo=daDataPrezzo,
                                              aDataPrezzo=aDataPrezzo,
                                              codiceArticoloFornitore=codiceArticoloFornitore,
                                              offset=self.offset,
                                              batchSize=self.batchSize)

        self._treeViewModel.clear()

        for f in fors:
            przLordo = ('%14.' + Environment.conf.decimals + 'f') % (f.prezzo_lordo or 0)
            przNetto = ('%14.' + Environment.conf.decimals + 'f') % (f.prezzo_netto or 0)
            self._treeViewModel.append((f,
                                        (f.codice_articolo or ''),
                                        (f.articolo or ''),
                                        przLordo,
                                        przNetto,
                                        dateToString(f.data_prezzo),
                                        dateToString(f.data_fornitura),
                                        (f.codice_fornitore or ''),
                                        (f.fornitore or ''),
                                        (f.codice_articolo_fornitore or '')))
