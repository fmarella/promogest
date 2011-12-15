# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author: vete <info@promotux.it>

import gtk
from promogest.ui.AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest.modules.SchedaLavorazione.dao.ColoreStampa import ColoreStampa
from promogest.ui.utils import *


class AnagraficaColoriStampa(Anagrafica):
    """ Anagrafica pagamenti """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica colori stampe',
                            '_Colori stampe',
                            AnagraficaColoriStampaFilter(self),
                            AnagraficaColoriStampaDetail(self))

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
        column.connect("clicked", self._changeOrderBy, 'denominazione')
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

        self.numRecords = ColoreStampa().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return ColoreStampa().select(denominazione=denominazione,
                                        orderBy=self.orderBy,
                                        offset=self.offset,
                                        batchSize=self.batchSize)

        self._filterClosure = filterClosure

        pags = self.runFilter()

        self._treeViewModel.clear()

        for p in pags:
            self._treeViewModel.append((p,
                                        (p.denominazione or '')))


class AnagraficaColoriStampaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei pagamenti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  '_anagrafica_colori_stampa_filter_table',
                          gladeFile='SchedaLavorazione/gui/schedalavorazione_plugins.glade',
                          module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaColoriStampaDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica dei pagamenti """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica,
                  gladeFile='SchedaLavorazione/gui/schedalavorazione_plugins.glade',module=True)

    def setDao(self, dao):
        if dao is None:
            self.dao = ColoreStampa()
            self._anagrafica._newRow((self.dao, ''))
            self._refresh()
        else:
            self.dao = dao

    def updateDao(self):
        self.dao = ColoreStampa().getRecord(id=self.dao.id)
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