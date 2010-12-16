# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: francesco meloni <francesco@promotux.it>

import gtk
from GladeWidget import GladeWidget
from promogest.ui.widgets.FilterWidget import FilterWidget

from utils import *



class Visualizzazione(GladeWidget):
    """ Classe base per le visualizzazioni di Promogest """

    def __init__(self, windowTitle, filterElement):
        GladeWidget.__init__(self, 'visualizzazione_window', 'visualizzazione_window.glade')
        print "AKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK", self.visualizzazione_window, filterElement
        self.visualizzazione_window.set_title(windowTitle)
        self.dao = None
        self._setFilterElement(filterElement)

        self.placeWindow(self.visualizzazione_window)
        self.filter.draw()


    def _setFilterElement(self, gladeWidget):
        self.bodyWidget = FilterWidget(owner=gladeWidget, filtersElement=gladeWidget)

        self.visualizzazione_viewport.add(self.bodyWidget.getTopLevel())
        self.bodyWidget.filter_body_label.set_no_show_all(True)
        self.bodyWidget.filter_body_label.set_property('visible', False)

        self.filter = self.bodyWidget.filtersElement
        self.filterTopLevel = self.filter.getTopLevel()
        self.filterTopLevel.set_sensitive(True)

        self.visualizzazione_filter_treeview = self.bodyWidget.resultsElement
        self._treeViewModel = None

        gladeWidget.build()

        accelGroup = gtk.AccelGroup()
        self.getTopLevel().add_accel_group(accelGroup)
        self.bodyWidget.filter_clear_button.add_accelerator('clicked', accelGroup, gtk.keysyms.Escape, 0, gtk.ACCEL_VISIBLE)
        self.bodyWidget.filter_search_button.add_accelerator('clicked', accelGroup, gtk.keysyms.F3, 0, gtk.ACCEL_VISIBLE)


    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura della visualizzazione """
        self.visualizzazione_window.show_all()


    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ Gestisce la conferma della riga """
        self.visualizzazione_window.hide()


    def on_filter_treeview_cursor_changed(self, treeview):
        """ Gestisce lo spostamento tra le righe """
        sel = self.visualizzazione_filter_treeview.get_selection()
        (model, iterator) = sel.get_selected()

        if iterator is None:
            #print 'visualizzazione.on_filter_treeview_cursor_changed(): FIXME: iterator is None!'
            return

        self.dao = model.get_value(iterator, 0)


    def on_confirm_button_clicked(self, widget):
        """ Riga confermata """
        self.visualizzazione_window.hide()


    def on_visualizzazione_window_close(self, widget, event=None):
        """ Uscita """
        self.destroy()
        return None



class VisualizzazioneFilter(GladeWidget):
    """ Filtro per la visualizzazione """

    def __init__(self, visualizzazione, rootWidget):
#        print "666666666666666666666666666", rootWidget, visualizzazione
        GladeWidget.__init__(self, rootWidget)
        self._visualizzazione = visualizzazione


    def build(self):
        """ reindirizza alcuni campi e metodi dal filterWidget """
        self.bodyWidget = self._visualizzazione.bodyWidget

        # mapping fields and methods from bodyWidget to this class
        self._changeOrderBy = self.bodyWidget._changeOrderBy
        print  "VEDIAMO UN PO", self.bodyWidget._changeOrderBy
        self.orderBy = self.bodyWidget.orderBy = None
        self.batchSize = self.bodyWidget.batchSize = 30
        self.offset = self.bodyWidget.offset = 0
        self.numRecords = self.bodyWidget.numRecords = 0
        self._filterClosure = None


    def draw(self):
        """
        Disegna i contenuti del filtro visualizzazione.  Metodo invocato
        una sola volta, dopo la costruzione dell'oggetto
        """
        raise NotImplementedError


    def clear(self):
        """ Ripulisci il filtro di visualizzazione e aggiorna la visualizzazione stessa """
        raise NotImplementedError


    def refresh(self):
        """ Aggiorna il filtro di visualizzazione in base ai parametri impostati """
        raise NotImplementedError


    def on_campo_filter_entry_key_press_event(self, widget, event):
        return self._visualizzazione.bodyWidget.on_filter_element_key_press_event(widget, event)


    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ Gestisce la conferma della riga """
        self._visualizzazione.on_filter_treeview_row_activated(treeview, path, column)


    def on_filter_treeview_cursor_changed(self, treeview):
        """ Gestisce lo spostamento tra le righe """
        self._visualizzazione.on_filter_treeview_cursor_changed(treeview)


    def runFilter(self, offset='__default__', batchSize='__default__',
                  progressCB=None, progressBatchSize=0):
        """ Recupera i dati """
        self.bodyWidget.orderBy = self.orderBy
        return self.bodyWidget.runFilter(offset=offset, batchSize=batchSize,
                                         progressCB=progressCB, progressBatchSize=progressBatchSize,
                                         filterClosure=self._filterClosure)


    def _refreshPageCount(self):
        """ Aggiorna la paginazione """
        self.bodyWidget.numRecords = self.numRecords
        self.bodyWidget._refreshPageCount()
