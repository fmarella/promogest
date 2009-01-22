# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# license GNU GPL see LICENSE file

import gtk
import gobject

from AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter

from promogest import Environment
from promogest.dao.Imballaggio import Imballaggio

from utils import *


class AnagraficaImballaggi(Anagrafica):
    """ Anagrafica imballaggi """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica imballaggi',
                            '_Imballaggi',
                            AnagraficaImballaggiFilter(self),
                            AnagraficaImballaggiDetail(self))


    def draw(self):
        """ Colonne della Treeview per il filtro"""
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str)
        treeview.set_model(self._treeViewModel)

        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())

        self.numRecords = Imballaggio().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Imballaggio().select(denominazione=denominazione,
                                                    orderBy=self.orderBy,
                                                    offset=self.offset,
                                                    batchSize=self.batchSize)

        self._filterClosure = filterClosure

        imbs = self.runFilter()

        self._treeViewModel.clear()

        for i in imbs:
            self._treeViewModel.append((i,
                                        (i.denominazione or '')))



class AnagraficaImballaggiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli imballaggi """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_imballaggi_filter_table',
                                  gladeFile='_anagrafica_imballaggi_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()



class AnagraficaImballaggiDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica degli imballaggi """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica, gladeFile='_anagrafica_imballaggi_elements.glade')


    def setDao(self, dao):
        if dao is None:
            self.dao = Imballaggio()
            #self.dao = self.imb.record
            self._anagrafica._newRow((self.dao, ''))
            self._refresh()
        else:
            self.dao = dao


    def updateDao(self):
        self.dao = Imballaggio().getRecord(id=self.dao.id)
        #self.dao = self.imb.record
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
