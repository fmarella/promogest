# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco "M3nt0r3" Meloni  <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import gtk
import gobject
from AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.dao.Pagamento import Pagamento

from utils import *



class AnagraficaPagamenti(Anagrafica):
    """ Anagrafica pagamenti """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica pagamenti',
                            '_Pagamenti',
                            AnagraficaPagamentiFilter(self),
                            AnagraficaPagamentiDetail(self))


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str)
        treeview.set_model(self._treeViewModel)

        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())
        self.numRecords = Pagamento().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Pagamento().select(denominazione=denominazione,
                                                orderBy=self.orderBy,
                                                offset=self.offset,
                                                batchSize=self.batchSize)

        self._filterClosure = filterClosure

        pags = self.runFilter()

        self._treeViewModel.clear()

        for p in pags:
            self._treeViewModel.append((p,
                                        (p.denominazione or '')))



class AnagraficaPagamentiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei pagamenti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_pagamenti_filter_table',
                                  gladeFile='_anagrafica_pagamenti_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaPagamentiDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica dei pagamenti """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica, gladeFile='_anagrafica_pagamenti_elements.glade')

    def setDao(self, dao):
        if dao is None:
            if Environment.engine.name =="sqlite" and Pagamento().count() >= 3:
                fenceDialog()
                return
            else:
                self.dao = Pagamento()
                self._anagrafica._newRow((self.dao, ''))
                self._refresh()
        else:
            self.dao = dao


    def updateDao(self):
        self.dao = Pagamento().getRecord(id=self.dao.id)
        self._refresh()


    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)


    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        denominazione = model.get_value(iterator, 1) or ''
        if (denominazione == ''):
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        self.dao.denominazione = denominazione
        self.dao.persist()


    def deleteDao(self):
        self.dao.delete()
