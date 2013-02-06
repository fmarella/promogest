# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from promogest.ui.AnagraficaSemplice import \
                Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest.dao.CCardType import CCardType
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *


class AnagraficaCCardType(Anagrafica):
    """ Anagrafica dei tipi di carta di credito  """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica Tipi Credit Card',
                            '_CCardType',
                            AnagraficaCCardTypeFilter(self),
                            AnagraficaCCardTypeDetail(self))

    def draw(self):
        # Colonne della Treeview per il filtro/modifica
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Descrizione', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 1)
        renderer.set_data('max_length', 10)
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,
                                (None, 'denominazione_breve'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str, str)
        treeview.set_model(self._treeViewModel)

        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(
            self.filter.denominazione_filter_entry.get_text())
        self.numRecords = CCardType().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return CCardType().select(denominazione=denominazione,
                                            orderBy=self.orderBy,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        self._filterClosure = filterClosure

        cats = self.runFilter()

        self._treeViewModel.clear()

        for c in cats:
            self._treeViewModel.append((c,
                                        (c.denominazione or ''),
                                        (c.denominazione_breve or '')))


class AnagraficaCCardTypeFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei tipi di carta di credito """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          root='anagrafica_ccardtype_filter_table',
                          path='_anagrafica_ccardtype_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaCCardTypeDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica dei tipi di carta di credito """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                              anagrafica,
                              path='_anagrafica_ccardtype_elements.glade')

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            self.dao = CCardType()
            self._anagrafica._newRow((self.dao, '', ''))
            #self._refresh()
        return self.dao

    def updateDao(self):
        self.dao = CCardType().getRecord(id=self.dao.id)
        self._refresh()

    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)
        model.set_value(iterator, 2, self.dao.denominazione_breve)

    def saveDao(self, tipo=None):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        denominazione = model.get_value(iterator, 1) or ''
        denominazioneBreve = model.get_value(iterator, 2) or ''
        if (denominazione == ''):
            obligatoryField(self._anagrafica.getTopLevel(),
                self._anagrafica.anagrafica_treeview)
        if (denominazioneBreve == ''):
            obligatoryField(self._anagrafica.getTopLevel(),
                self._anagrafica.anagrafica_treeview)
        self.dao.denominazione = denominazione
        self.dao.denominazione_breve = denominazioneBreve
        self.dao.persist()

    def deleteDao(self):
        self.dao.delete()
