# -*- coding: iso-8859-15 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
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

from promogest.ui.Anagrafica import Anagrafica, AnagraficaFilter, AnagraficaDetail

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.StatoArticolo
from promogest.dao.StatoArticolo import StatoArticolo

from promogest.ui.utils import *
from promogest.ui.gtk_compat import *


class AnagraficaStatiArticoli(Anagrafica):
    """ Anagrafica stati articolo """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica stati articolo',
                            '_Stati Articolo',
                            AnagraficaStatiArticoliFilter(self),
                            AnagraficaStatiArticoliDetail(self))




class AnagraficaStatiArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli stati articolo """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_stati_articoli_filter_table')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def draw(self):
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Descrizione', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self.refresh()


    def clear(self):
        self.denominazione_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())

        self.numRecords = StatoArticolo().count(denominazione=denominazione)

        self._refreshPageCount()

        stas = StatoArticolo().select(denominazione=denominazione,
                                                  orderBy = self.orderBy,
                                                  offset = self.offset,
                                                  batchSize = self.batchSize)
        model = gtk.ListStore(object, str)
        for s in stas:
            model.append((s,
                          (s.denominazione or '')))

        self._anagrafica.anagrafica_filter_treeview.set_model(model)



class AnagraficaStatiArticoliDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica degli stati articolo """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica,
                                  'anagrafica_stati_articoli_detail_table')
        self._widgetFirstFocus = self.denominazione_entry


    def draw(self):
        pass


    def clear(self):
        self.dao.denominazione = ''
        self._refresh()


    def setDao(self, dao):
        if dao is None:
            self.dao = StatoArticolo()
        else:
            self.dao = dao
        self._refresh()


    def updateDao(self):
        self.dao = StatoArticolo().getRecord(id=self.dao.id)
        self._refresh()


    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')


    def saveDao(self):
        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.persist()


    def deleteDao(self):
        self.dao.delete()
        self.clear()
