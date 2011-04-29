# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
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

from AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.dao.Banca import Banca
from promogest.lib.ControlloIBAN import *
from GladeWidget import GladeWidget
from utils import *
from utilsCombobox import *

class AnagraficaBanche(Anagrafica):
    """ Anagrafica banche """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica banche',
                            '_Banche',
                            AnagraficaBancheFilter(self),
                            AnagraficaBancheDetail(self))


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 1)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Agenzia', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'agenzia'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 2)
        renderer.set_data('max_length', 30)
        column = gtk.TreeViewColumn('IBAN', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'iban'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str, str, str)
        treeview.set_model(self._treeViewModel)

        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())
        agenzia = prepareFilterString(self.filter.agenzia_filter_entry.get_text())
        iban = prepareFilterString(self.filter.iban_filter_entry.get_text())
        self.numRecords = Banca().count( denominazione=denominazione,
                                                    agenzia=agenzia,
                                                    iban=iban)
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Banca().select(denominazione=denominazione,
                                            agenzia=agenzia,
                                            iban=iban,
                                            orderBy=self.orderBy,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        self._filterClosure = filterClosure

        bans = self.runFilter()

        self._treeViewModel.clear()

        for b in bans:
            iban = IBAN(b.iban)

            self._treeViewModel.append((b,
                                        (b.denominazione or ''),
                                        (b.agenzia or ''),
                                        (b.iban or '')))

class AnagraficaBancheFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle banche """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_banche_filter_table',
                                  gladeFile='_anagrafica_banche_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.agenzia_filter_entry.set_text('')
        self.iban_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()

class AnagraficaBancheDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle banche """

    def __init__(self, anagrafica):
        pass


    def setDao(self, dao):
        if dao is None:
            self.dao = Banca()
        else:
            self.dao = dao

    def updateDao(self):
        self.dao = Banca().getRecord(id= self.dao.id)

