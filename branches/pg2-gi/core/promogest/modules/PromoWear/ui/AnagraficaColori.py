# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Alessandro Scano <alessandro@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

import gtk
from promogest.ui.AnagraficaSemplice import Anagrafica,\
                                     AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.ui.utils import *


class AnagraficaColori(Anagrafica):
    """ Anagrafica colori """

    def __init__(self):
        Anagrafica.__init__(self, 'Promowear - Anagrafica colori',
                            '_Colori',
                            AnagraficaColoreFilter(self),
                            AnagraficaColoreDetail(self))

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

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 1)
        renderer.set_data('max_length', 10)
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=2,
                                                                sensitive=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,
                                                    'denominazione_breve'))
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
        self.numRecords = Colore().count(denominazione=denominazione)
        self._refreshPageCount()
        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Colore().select(denominazione=denominazione,
                                               orderBy = self.orderBy,
                                               offset = self.offset,
                                               batchSize = self.batchSize)
        self._filterClosure = filterClosure
        cols = self.runFilter()
        self._treeViewModel.clear()
        for c in cols:
            self._treeViewModel.append((c, c.denominazione,
                                        c.denominazione_breve,
                                        True))


class AnagraficaColoreFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei colori """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                anagrafica,
                'anagrafica_colore_filter_table',
                gladeFile='PromoWear/gui/_anagrafica_colore_elements.glade',
                module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaColoreDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica dei colori """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica)

    def setDao(self, dao):
        if dao is None:
            self.dao = Colore()
            self._anagrafica._newRow((self.dao, '', '', True))
            self._refresh()
        else:
            self.dao = dao

    def updateDao(self):
        if self.dao:
            self.dao = Colore().getRecord(id=self.dao.id)
            self._refresh()
        else:
            raise Exception, 'Update not possible'

    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)
        model.set_value(iterator, 2, self.dao.denominazione_breve)

    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.dao.denominazione = model.get_value(iterator, 1)
        self.dao.denominazione_breve = model.get_value(iterator, 2)
        if Environment.tipo_eng == "sqlite":
            if Colore().count() >= 5:
                return
        self.dao.persist()

    def deleteDao(self):
        self.dao.delete()
