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


from promogest.ui.Visualizzazione import Visualizzazione, VisualizzazioneFilter
from promogest import Environment
import promogest.dao.Fornitura
from promogest.dao.Fornitura import Fornitura
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *


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
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
#        column.set_clickable(True)
#        column.connect("clicked", self._changeOrderBy, ("Articolo", 'codice_articolo'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Denominazione', rendererSx, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
#        column.set_clickable(True)
#        column.connect("clicked", self._changeOrderBy, ("Articolo", 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo lordo', rendererDx, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'prezzo_lordo'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo Netto', rendererDx, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'prezzo_netto'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data prezzo', rendererSx, text=5)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'data_prezzo'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data fornitura', rendererSx, text=6)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'data_fornitura'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice fornitore', rendererSx, text=7)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'codice_fornitore'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ragione sociale', rendererSx, text=8)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'fornitore'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', rendererSx, text=9)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
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
            przLordo = mN(f.prezzo_lordo or 0)
            przNetto = mN(f.prezzo_netto or 0)
            self._treeViewModel.append((f,
                                        (f.codice_articolo or ''),
                                        (f.articolo or ''),
                                        str(przLordo),
                                        str(przNetto),
                                        dateToString(f.data_prezzo),
                                        dateToString(f.data_fornitura),
                                        (f.codice_fornitore or ''),
                                        (f.fornitore or ''),
                                        (str(f.codice_articolo_fornitore) or '')))
