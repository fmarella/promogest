# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from promogest.ui.AnagraficaSemplice import Anagrafica,\
                                    AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.modules.PromoWear.dao.Modello import Modello
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *


class AnagraficaModelli(Anagrafica):
    """ Anagrafica colori """

    def __init__(self):
        Anagrafica.__init__(self, 'Promowear - Anagrafica modelli',
                            '_Modelli',
                            AnagraficaModelliFilter(self),
                            AnagraficaModelliDetail(self))

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
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=2,
                                    sensitive=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,
                                        (None, 'denominazione_breve'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        # Model: Dao, denominazione, denominazione_breve, sensitive
        self._treeViewModel = gtk.ListStore(object, str, str, bool)
        treeview.set_model(self._treeViewModel)

        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())

        self.numRecords = Modello().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Modello().select(denominazione=denominazione,
                                               orderBy = self.orderBy,
                                               offset = self.offset,
                                               batchSize = self.batchSize)

        self._filterClosure = filterClosure

        models = self.runFilter()

        self._treeViewModel.clear()

        for m in models:
            self._treeViewModel.append((m, m.denominazione,
                                m.denominazione_breve, True))


class AnagraficaModelliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei modelli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                anagrafica,
                'anagrafica_modello_filter_table',
                gladeFile='PromoWear/gui/_anagrafica_modello_elements.glade',
                module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaModelliDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica degli imballaggi """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica)

    def setDao(self, dao):
        if dao is None:
            self.dao = Modello()
            self._anagrafica._newRow((self.dao, '', '', True))
            self._refresh()
        else:
            self.dao = dao
        return self.dao

    def updateDao(self):
        if self.dao is not None:
            self.dao = Modello().getRecord(id=self.dao.id)
            self._refresh()
        else:
            raise Exception, 'Update not possible dao is none'

    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if not iterator:
            return
        if not self.dao:
            return
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)
        model.set_value(iterator, 2, self.dao.denominazione_breve)

    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.dao.denominazione = model.get_value(iterator, 1)
        self.dao.denominazione_breve = model.get_value(iterator, 2)
        if self.dao.denominazione == '' or self.dao.denominazione == None:
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        if self.dao.denominazione_breve == '' or self.dao.denominazione_breve == None:
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        self.dao.persist()
