# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010,2011 by Promotux
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
from promogest.ui.AnagraficaSemplice import Anagrafica,\
                                    AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.modules.GestioneCommesse.dao.StadioCommessa import StadioCommessa
from promogest.ui.utils import *


class AnagraficaStadioCommessa(Anagrafica):
    """ Anagrafica colori """

    def __init__(self):
        Anagrafica.__init__(self, 'Gestione Commessa - Anagrafica Stadio Commessa',
                            '_Stadio_Commessa',
                            AnagraficaStadioCommessaFilter(self),
                            AnagraficaStadioCommessaDetail(self))

    def draw(self):
        # Colonne della Treeview per il filtro

        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Denominazione', renderer, text=1,
                                    sensitive=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(1)

        # Model: Dao, denominazione, denominazione_breve, sensitive
        self._treeViewModel = gtk.ListStore(object, str)
        treeview.set_model(self._treeViewModel)

        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())

        self.numRecords = StadioCommessa().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return StadioCommessa().select(denominazione=denominazione,
                                               orderBy = self.orderBy,
                                               offset = self.offset,
                                               batchSize = self.batchSize)

        self._filterClosure = filterClosure

        models = self.runFilter()

        self._treeViewModel.clear()

        for m in models:
            self._treeViewModel.append((m, m.denominazione
                                ))


class AnagraficaStadioCommessaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica deistadi commessa """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                anagrafica,
                'anagrafica_stadio_commessa_filter_table',
                gladeFile='GestioneCommesse/gui/_anagrafica_stadio_commessa_elements.glade',
                module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaStadioCommessaDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica degli imballaggi """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica)

    def setDao(self, dao):
        if dao is None:
            self.dao = StadioCommessa()
            self._anagrafica._newRow((self.dao, ''))
            self._refresh()
        else:
            self.dao = dao
        return self.dao

    def updateDao(self):
        if self.dao is not None:
            self.dao = StadioCommessa().getRecord(id=self.dao.id)
            self._refresh()
        else:
            raise Exception, 'Update not possible dao is none'

    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator and self.dao:
            model.set_value(iterator, 0, self.dao)
            model.set_value(iterator, 1, self.dao.denominazione)

    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.dao.denominazione = model.get_value(iterator, 1)
        if self.dao.denominazione == '' or self.dao.denominazione == None:
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        self.dao.persist()
