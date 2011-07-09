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

from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter

from promogest import Environment
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Fornitore import Fornitore
from promogest.dao.ScontoFornitura import ScontoFornitura
from promogest.dao.Articolo import Articolo
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaFornitureFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle forniture """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_forniture_filter_table',
                                  gladeFile='anagrafica_forniture_filter_table.glade')
        self._widgetFirstFocus = self.id_articolo_filter_customcombobox
        persona_giuridica=Table('persona_giuridica', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        #self.fornitore=Table('fornitore', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        #self.joinT = join(self.fornitore, persona_giuridica)
        fornitura=Table('fornitura',Environment.params['metadata'],schema = Environment.params['schema'],autoload=True)
        articolo=Table('articolo', Environment.params['metadata'],schema = Environment.params['schema'],autoload=True)
        self.joinT2 = join(articolo, fornitura)

    def draw(self):
        """Colonne della Treeview per il filtro
            Attenzione, alcuni order_by non funzionano, indagare ...relazione con fornitura
            non molto pulita
        """
        treeview = self._anagrafica.anagrafica_filter_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Fornitore', rendererSx, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, (self.joinT,Fornitore.ragione_sociale))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', rendererSx, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,Fornitura.codice_articolo_fornitore))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy, (self.joinT2,Articolo.codice))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        #column.connect("clicked", self._changeOrderBy,(self.joinT2,Articolo.denominazione))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data fornitura', rendererSx, text=5)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,Fornitura.data_fornitura))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo lordo', rendererDx, text=6)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,Fornitura.prezzo_lordo))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Prezzo netto', rendererDx, text=7)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,Fornitura.prezzo_netto))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)
        if posso("PW"):
            column = gtk.TreeViewColumn('Gruppo taglia', rendererSx, text=8)
            column.set_sizing(GTK_COLUMN_GROWN_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'denominazione_gruppo_taglia')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Taglia', rendererSx, text=9)
            column.set_sizing(GTK_COLUMN_GROWN_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'denominazione_taglia')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(70)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Colore', rendererSx, text=10)
            column.set_sizing(GTK_COLUMN_GROWN_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'denominazione_colore')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(70)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Anno', rendererSx, text=11)
            column.set_sizing(GTK_COLUMN_GROWN_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'anno')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(50)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Stagione', rendererSx, text=12)
            column.set_sizing(GTK_COLUMN_GROWN_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'stagione')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(100)
            treeview.append_column(column)

            column = gtk.TreeViewColumn('Genere', rendererSx, text=13)
            column.set_sizing(GTK_COLUMN_GROWN_ONLY)
            column.set_clickable(True)
            column.connect("clicked", self._changeOrderBy, 'genere')
            column.set_resizable(True)
            column.set_expand(False)
            column.set_min_width(50)
            treeview.append_column(column)
            self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str, str, str, str)
        else:
           self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str)

        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        if self._anagrafica._articoloFissato:
            self.id_articolo_filter_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_filter_customcombobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(2)
            column.set_property('visible', False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(3)
            column.set_property('visible', False)
            if posso("PW"):
                column = self._anagrafica.anagrafica_filter_treeview.get_column(7)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(8)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(9)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(10)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(11)
                column.set_property('visible', False)
                column = self._anagrafica.anagrafica_filter_treeview.get_column(12)
                column.set_property('visible', False)
        if self._anagrafica._fornitoreFissato:
            self.id_fornitore_filter_customcombobox.setId(self._anagrafica._idFornitore)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(0)
            column.set_property('visible', False)

        self.clear()


    def clear(self):
        # Annullamento filtro
        if not(self._anagrafica._articoloFissato):
            self.id_articolo_filter_customcombobox.set_active(0)
        if not(self._anagrafica._fornitoreFissato):
            self.id_fornitore_filter_customcombobox.set_active(0)
        self.da_data_fornitura_filter_entry.set_text('')
        self.a_data_fornitura_filter_entry.set_text('')
        self.da_data_prezzo_filter_entry.set_text('')
        self.a_data_prezzo_filter_entry.set_text('')
        self.codice_articolo_fornitore_filter_entry.set_text('')
        self.refresh()


    def refresh(self, join=None):
        # Aggiornamento TreeView
        idArticolo = self.id_articolo_filter_customcombobox.getId()
        idFornitore = self.id_fornitore_filter_customcombobox.getId()
        daDataFornitura = stringToDate(self.da_data_fornitura_filter_entry.get_text())
        aDataFornitura = stringToDate(self.a_data_fornitura_filter_entry.get_text())
        daDataPrezzo = stringToDate(self.da_data_prezzo_filter_entry.get_text())
        aDataPrezzo = stringToDate(self.a_data_prezzo_filter_entry.get_text())
        codiceArticoloFornitore = prepareFilterString(self.codice_articolo_fornitore_filter_entry.get_text())

        def filterCountClosure():
            return Fornitura().count(join = join,
                                    idArticolo=idArticolo,
                                    idFornitore=idFornitore,
                                    daDataFornitura=daDataFornitura,
                                    aDataFornitura=aDataFornitura,
                                    daDataPrezzo=daDataPrezzo,
                                    aDataPrezzo=aDataPrezzo,
                                    codiceArticoloFornitore=codiceArticoloFornitore)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Fornitura().select(join = join,
                                        orderBy=self.orderBy,
                                        idArticolo=idArticolo,
                                        idFornitore=idFornitore,
                                        daDataFornitura=daDataFornitura,
                                        aDataFornitura=aDataFornitura,
                                        daDataPrezzo=daDataPrezzo,
                                        aDataPrezzo=aDataPrezzo,
                                        codiceArticoloFornitore=codiceArticoloFornitore,
                                        offset=offset,
                                        batchSize=batchSize)

        self._filterClosure = filterClosure

        fors = self.runFilter()

        self._treeViewModel.clear()

        for f in fors:
            if posso("PW"):
                self._treeViewModel.append((f,
                            (f.fornitore or ''),
                            (f.codice_articolo_fornitore or ''),
                            (f.codice_articolo or ''),
                            (f.articolo or ''),
                            dateToString(f.data_fornitura),
                            str((mN(f.prezzo_lordo))),
                            str((mN(f.prezzo_netto))),
                            (f.denominazione_gruppo_taglia or ''),
                            (f.denominazione_taglia or ''),
                            (f.denominazione_colore or ''),
                            (f.anno or ''),
                            (f.stagione or ''),
                            (f.genere or '')))
            else:
                self._treeViewModel.append((f,
                            (f.fornitore or ''),
                            (f.codice_articolo_fornitore or ''),
                            (f.codice_articolo or ''),
                            (f.articolo or ''),
                            dateToString(f.data_fornitura),
                            str((mN(f.prezzo_lordo) or 0)),
                            str((mN(f.prezzo_netto) or 0))))
