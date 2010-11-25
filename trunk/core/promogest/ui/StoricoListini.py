# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>

import gtk
import gobject
from Visualizzazione import Visualizzazione, VisualizzazioneFilter

from promogest import Environment
import promogest.dao.ListinoArticolo
from promogest.dao.ListinoArticolo import ListinoArticolo

from utils import *

class StoricoListini(Visualizzazione):
    """ Visualizzazione listini """

    def __init__(self, idArticolo = None, idListino = None,
                       daDataListino = None, aDataListino = None):
        self._idArticolo = idArticolo
        self._idListino = idListino
        Visualizzazione.__init__(self, 'Promogest - Visualizzazione storico prezzi di vendita',
                                StoricoListiniFilter(self))
#        Visualizzazione.__init__(self, 'Promogest - Visualizzazione storico prezzi di vendita',
#                                None)


class StoricoListiniFilter(VisualizzazioneFilter):
    """ Filtro per la visualizzazione dei listini """

    def __init__(self, visualizzazione):
        VisualizzazioneFilter.__init__(self,
                                    visualizzazione,
                                    'storico_listini_articoli_filter_table')
        self.orderBy = 'data_listino'


    def on_filter_treeview_selection_changed(self, treeview):
        pass


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._visualizzazione.visualizzazione_filter_treeview

        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data listino', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'data_listino')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio (ivato)', rendererDx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'prezzo_dettaglio')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Ricarico', rendererDx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Margine', rendererDx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso (non ivato)', rendererDx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'prezzo_dettaglio')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Ricarico', rendererDx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Margine', rendererDx, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Costo base (non ivato)', rendererDx, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'ultimo_costo')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str)
        self._visualizzazione.visualizzazione_filter_treeview.set_model(self._treeViewModel)

        returnWindow = self._visualizzazione.getTopLevel()
        self.id_articolo_filter_customcombobox1.setId(self._visualizzazione._idArticolo)
        self.id_articolo_filter_customcombobox1.setSingleValue()
        fillComboboxListini(self.id_listino_filter_combobox1, True)
        self.id_listino_filter_combobox1.set_active(0)

        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.id_articolo_filter_customcombobox1.set_active(0)
        self.id_listino_filter_combobox1.set_active(0)
        self.da_data_listino_filter_entry.set_text('')
        self.a_data_listino_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self.id_articolo_filter_customcombobox1.getId()
        if idArticolo is None:
            self._treeViewModel.clear()
            dialog = gtk.MessageDialog(self._visualizzazione.getTopLevel(),
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                                       'Selezionare un articolo !')
            dialog.run()
            dialog.destroy()
            return

        idListino = findIdFromCombobox(self.id_listino_filter_combobox1)
        daDataListino = stringToDate(self.da_data_listino_filter_entry.get_text())
        aDataListino = stringToDate(self.a_data_listino_filter_entry.get_text())

        self.numRecords = ListinoArticolo().count(idArticolo=idArticolo,
                                                            idListino=idListino,
                                                            listinoAttuale=None,
                                                            daDataListino=daDataListino,
                                                            aDataListino=aDataListino)

        self._refreshPageCount()

        liss = ListinoArticolo().select(orderBy=self.orderBy,
                                                    idArticolo=idArticolo,
                                                    idListino=idListino,
                                                    listinoAttuale=None,
                                                    daDataListino=daDataListino,
                                                    aDataListino=aDataListino,
                                                    offset = self.offset,
                                                    batchSize = self.batchSize)


        self._treeViewModel.clear()

        for l in liss:
            przDet = ('%14.' + Environment.conf.decimals + 'f') % (l.prezzo_dettaglio or 0)
            przIngr = ('%14.' + Environment.conf.decimals + 'f') % (l.prezzo_ingrosso or 0)
            ricDett = '%-6.3f' % calcolaRicarico(float(l.ultimo_costo or 0),
                                                 float(l.prezzo_dettaglio or 0),
                                                 float(l.percentuale_iva or 0))
            margDett = '%-6.3f' % calcolaMargine(float(l.ultimo_costo or 0),
                                                 float(l.prezzo_dettaglio or 0),
                                                 float(l.percentuale_iva or 0))
            ricIngr = '%-6.3f' % calcolaRicarico(float(l.ultimo_costo or 0),
                                                 float(l.prezzo_ingrosso or 0))
            margIngr = '%-6.3f' % calcolaMargine(float(l.ultimo_costo or 0),
                                                 float(l.prezzo_ingrosso or 0))

            self._treeViewModel.append((l,
                                        (l.denominazione or ''),
                                        dateToString(l.data_listino),
                                        przDet, ricDett, margDett,
                                        przIngr, ricIngr, margIngr,
                                        (l.ultimo_costo or 0)))
