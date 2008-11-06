# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
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

from promogest.ui.AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.modules.Stampalux.dao.CarattereStampa
from promogest.modules.Stampalux.dao.CarattereStampa import CarattereStampa

from promogest.ui.utils import *

class AnagraficaCaratteriStampa(Anagrafica):
    """ Anagrafica codici a barre """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica Caratteri per la stampa',
                            '_Caratteri stampa',
                            AnagraficaCaratteriStampaFilter(self),
                            AnagraficaCaratteriStampaDetail(self))

    def draw(self):
        # Colonne della Treeview per il filtro/modifica
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)
        
        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str)
        treeview.set_model(self._treeViewModel)

        treeview.set_search_column(1)
        self.refresh()
    
    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())
        self.numRecords = promogest.modules.Stampalux.dao.CarattereStampa.count(Environment.connection,
                                                                   denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return promogest.modules.Stampalux.dao.CarattereStampa.select(Environment.connection,
                                                             denominazione=denominazione,
                                                             orderBy=self.orderBy,
                                                             offset=self.offset,
                                                             batchSize=self.batchSize)

        self._filterClosure = filterClosure

        bars = self.runFilter()

        self._treeViewModel.clear()

        for b in bars:
            self._treeViewModel.append((b,
                                        (b.denominazione or '')))


class AnagraficaCaratteriStampaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei Colori di Stampa """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                                anagrafica,
                                                '_anagrafica_caratteri_stampa_filter_table', \
                                                gladeFile='Stampalux/gui/stampalux_plugins.glade', \
                                                module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()

class AnagraficaCaratteriStampaDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica dei codici a barre """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                                anagrafica, \
                                                gladeFile='Stampalux/gui/stampalux_plugins.glade', \
                                                module=True)

    def setDao(self, dao):
        if dao is None:
            self.dao = CarattereStampa(Environment.connection)
            self._anagrafica._newRow((self.dao, ''))
            self._refresh()
        else:
            self.dao = dao


    def updateDao(self):
        self.dao = CarattereStampa(Environment.connection, self.dao.id)
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

        self.dao.denominazione= denominazione
        self.dao.persist()


    def deleteDao(self):
        self.dao.delete()
