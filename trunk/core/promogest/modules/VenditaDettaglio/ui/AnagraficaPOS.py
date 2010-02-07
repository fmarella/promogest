# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

import gtk
from promogest.ui.AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.modules.VenditaDettaglio.dao.Pos import Pos

from promogest.ui.utils import *


class AnagraficaPos(Anagrafica):
    """ Anagrafica dei punti cassa """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica Pos',
                            '_Pos',
                            AnagraficaPosFilter(self),
                            AnagraficaPosDetail(self))


    def draw(self):
        # Colonne della Treeview per il filtro/modifica
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Descrizione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 1)
        renderer.set_data('max_length', 10)
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'denominazione_breve'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str, str)
        treeview.set_model(self._treeViewModel)

        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())
        self.numRecords = Pos().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Pos().select(denominazione=denominazione,
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



class AnagraficaPosFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei punti cassa """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_pos_filter_table',
                                  gladeFile='VenditaDettaglio/gui/_anagrafica_pos_elements.glade', module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()



class AnagraficaPosDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle punti cassa """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica,
                                  gladeFile='VenditaDettaglio/gui/_anagrafica_pos_elements.glade', module=True)


    def setDao(self, dao):
        if dao is None:
            self.dao = Pos()
            self._anagrafica._newRow((self.dao, '', ''))
            self._refresh()
        else:
            self.dao = dao


    def updateDao(self):
        self.dao = Pos().getRecord(id=self.dao.id)
        self._refresh()


    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)
        model.set_value(iterator, 2, self.dao.denominazione_breve)


    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        denominazione = model.get_value(iterator, 1) or ''
        denominazioneBreve = model.get_value(iterator, 2) or ''
        if (denominazione == ''):
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        if (denominazioneBreve == ''):
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        self.dao.denominazione = denominazione
        self.dao.denominazione_breve = denominazioneBreve
        self.dao.persist()


    def deleteDao(self):
        self.dao.delete()
