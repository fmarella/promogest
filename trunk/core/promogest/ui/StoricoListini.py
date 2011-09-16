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

from promogest.ui.gtk_compat import *
from promogest.ui.Visualizzazione import Visualizzazione, VisualizzazioneFilter
from sqlalchemy.orm import mapper, join
from promogest import Environment
from promogest.dao.ListinoArticolo import ListinoArticolo

from promogest.ui.utils import stringToDate, fillComboboxListini, findIdFromCombobox,\
            calcolaRicarico, calcolaMargine, dateToString, setconf, mN, messageInfo


class StoricoListini(Visualizzazione):
    """ Visualizzazione listini """

    def __init__(self, idArticolo = None, idListino = None,
                       daDataListino = None, aDataListino = None):
        self._idArticolo = idArticolo
        self._idListino = idListino
        Visualizzazione.__init__(self,
                    'Promogest - Visualizzazione storico prezzi di vendita',
                                StoricoListiniFilter(self))


class StoricoListiniFilter(VisualizzazioneFilter):
    """ Filtro per la visualizzazione dei listini """

    def __init__(self, visualizzazione):
        VisualizzazioneFilter.__init__(self,
                                    visualizzazione,
                                    'storico_listini_articoli_filter_table')
#        self.orderBy = 'data_listino'

    def on_filter_treeview_selection_changed(self, treeview):
        pass

    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._visualizzazione.visualizzazione_filter_treeview

        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Listino', rendererSx, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
#        column.set_clickable(True)
#        column.connect("clicked", self._changeOrderBy,
#                                        (self.joinT, Listino.denominazione))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data listino', rendererSx, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
#        column.set_clickable(True)
#        column.connect("clicked", self._changeOrderBy,
#                                        (self.joinT, Listino.data_listino))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo dettaglio (ivato)',
                                                        rendererDx, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,
                                                (None, 'prezzo_dettaglio'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Ricarico', rendererDx, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Margine', rendererDx, text=5)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo ingrosso (non ivato)',
                                                    rendererDx, text=6)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,
                                                (None, 'prezzo_dettaglio'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Ricarico', rendererDx, text=7)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('% Margine', rendererDx, text=8)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Costo base (non ivato)',
                                                        rendererDx, text=9)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'ultimo_costo'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object, str, str, str,
                                            str, str, str, str, str, str)
        self._visualizzazione.visualizzazione_filter_treeview.\
                                        set_model(self._treeViewModel)

        returnWindow = self._visualizzazione.getTopLevel()
        self.id_articolo_filter_customcombobox1.\
                                setId(self._visualizzazione._idArticolo)
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
            messageInfo(transient=self._visualizzazione.getTopLevel(), msg='Selezionare un articolo !')
            return

        idListino = findIdFromCombobox(self.id_listino_filter_combobox1)
        daDataListino = stringToDate(self.da_data_listino_filter_entry.get_text())
        aDataListino = stringToDate(self.a_data_listino_filter_entry.get_text())

        self.numRecords = ListinoArticolo().count(idArticolo=idArticolo,
                                                            idListino=idListino,
                                                            listinoAttuale=None,
#                                                            daDataListino =daDataListino,
#                                                            aDataListino=aDataListino
                                                            )

        self._refreshPageCount()

        liss = ListinoArticolo().select(orderBy=self.orderBy,
                                                    idArticolo=idArticolo,
                                                    idListino=idListino,
                                                    listinoAttuale=None,
#                                                    daDataListino=daDataListino,
#                                                    aDataListino=aDataListino,
                                                    offset = self.offset,
                                                    batchSize = self.batchSize)


        self._treeViewModel.clear()

        for l in liss:
            przDet = mN(l.prezzo_dettaglio or 0)
            przIngr = mN(l.prezzo_ingrosso or 0)
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
