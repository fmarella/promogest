# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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

import math

import gtk
import gobject
from GladeWidget import GladeWidget
from promogest.ui.widgets.FilterWidget import FilterWidget
import Login
from utils import *


class RicercaComplessa(GladeWidget):
    """ Classe base per le ricerche avanzate di Promogest """

    def __init__(self, windowTitle, filtersElement):
        GladeWidget.__init__(self, 'ricerca_window')

        #self.ricerca_html.destroy()
        self.dao = None
        self.window = self.ricerca_window

        self.filter = FilterWidget(owner=self, filtersElement=filtersElement)
        filtersElement.filter = self.filter

        self.filterTopLevel = self.filter.getTopLevel()
        self.filters = self.filter.filtersElement
        self.results = self.filter.resultsElement

        self.filter.filter_body_label.set_no_show_all(True)
        self.filter.filter_body_label.set_property('visible', False)
        self.filter.filter_scrolledwindow.set_policy(hscrollbar_policy = gtk.POLICY_AUTOMATIC,
                                                     vscrollbar_policy = gtk.POLICY_AUTOMATIC)

        self.window.set_title(windowTitle)

        self.placeWindow(self.window)

    def on_filter_treeview_selection_changed(self,selection):
        pass


    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura della ricerca """
        if self.window not in Environment.windowGroup:
            Environment.windowGroup.append(self.window)
        self.window.show_all()


    def insert(self, toggleButton, returnWindow):
        """ Richiama l'anagrafica per l'inserimento """
        raise NotImplementedError


    def on_inserimento_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        anagReturn = self.getTopLevel()
        self.insert(toggleButton, anagReturn)


    def on_confirm_button_clicked(self, widget):
        """ Riga confermata """
        if self.ricerca_window in Environment.windowGroup:
            Environment.windowGroup.remove(self.ricerca_window)
        self.ricerca_window.hide()


    def on_ricerca_window_close(self, widget, event=None):
        if self.ricerca_window in Environment.windowGroup:
            Environment.windowGroup.remove(self.ricerca_window)
        self.hide()
        return True



def analyze_treeview_key_press_event(treeview, keyname, insertCall, deleteCall, refreshCall=None):
    """ Gestione della pressione di tasti all'interno di una treeview """
    if keyname == 'Insert' or keyname == 'KP_Insert':
        insertCall()
    elif keyname == 'Delete' or keyname == 'KP_Delete':
        deleteCall()
    elif keyname in ('plus','KP_Add'):
        selection = treeview.get_selection()
        (model, iterator) = selection.get_selected()
        if iterator is not None:
            row = model[iterator]
            row[0] = not row[0]
            row[1] = False
    elif keyname in ('minus','KP_Subtract'):
        selection = treeview.get_selection()
        (model, iterator) = selection.get_selected()
        if iterator is not None:
            row = model[iterator]
            row[1] = not row[1]
            row[0] = False

    if refreshCall is not None:
        refreshCall()
    return True


def parseModel(model, operation, index):
    """ Esegue una operazione sugli elementi di un model qualunque """
    def analyzeTreeStoreRow(model, path, iter, (operation, index)):
        row = model[iter]
        operation(row, index)

    def analyzeListStoreRow(model, row, operation, index):
        operation(row, index)

    if model.__class__ is gtk.TreeStore:
        model.foreach(analyzeTreeStoreRow, (operation, index))
    elif model.__class__ is gtk.ListStore:
        for r in model:
            analyzeListStoreRow(model, r, operation, index)


def optimizeString(stringa):
    """ Trattamento caratteri e sequenze particolari """
    # previene errata interpretazione sequenze di escape
    stringa = stringa.replace('\'', '\\\'')
    # sostituzione caratteri jolly
    stringa = stringa.replace('*', '%')
    return stringa


def columnSelectAll(column, treeview, refreshCall=None):
    """
    Gestisce la selezione/deselezione alternata delle colonne
    di inclusione/esclusione valori
    """

    def setStateRow(row, index):
        if index == 0:
            row[0] = treeview.selectAllIncluded
            row[1] = False
        elif index == 1:
            row[1] = treeview.selectAllExcluded
            row[0] = False

    model = treeview.get_model()
    renderer = column.get_cell_renderers()[0]
    index = renderer.get_data('model_index')
    if index == 0:
        if treeview.selectAllIncluded is None:
            treeview.selectAllIncluded = True
        else:
            treeview.selectAllIncluded = not treeview.selectAllIncluded
        if treeview.selectAllIncluded:
            treeview.selectAllExcluded = False
    elif index == 1:
        if treeview.selectAllExcluded is None:
            treeview.selectAllExcluded = True
        else:
            treeview.selectAllExcluded = not treeview.selectAllExcluded
        if treeview.selectAllExcluded:
            treeview.selectAllIncluded = False
    else:
        return

    parseModel(model, setStateRow, index)
    if refreshCall is not None:
        refreshCall()


def onColumnEdited(cell, path, value, treeview, editNext=False, refreshCall=None):
    """ Gestione del salvataggio dei valori impostati nelle colonne di una treeview """
    def setChild(model, iterator, index, value):
        if iterator is None:
            return

        while iterator is not None:
            if index == 0:
                model.set_value(iterator, 0, value)
                model.set_value(iterator, 1, False)
            elif index == 1:
                model.set_value(iterator, 1, value)
                model.set_value(iterator, 0, False)

            if model.iter_has_child(iterator):
                iter = model.iter_children(iterator)
                setChild(model, iter, index, value)
            iterator = model.iter_next(iterator)

    model = treeview.get_model()
    iterator = model.get_iter(path)
    index = cell.get_data('model_index')
    row = model[iterator]
    if cell.__class__ is gtk.CellRendererText:
        if value == '':
            model.remove(iterator)
            return
        else:
            model.set_value(iterator, index, value)
    elif cell.__class__ is gtk.CellRendererToggle:
        model.set_value(iterator, index, not cell.get_active())
        checked = model.get_value(iterator, index)
        if checked:
            if index == 0:
                model.set_value(iterator, 1, False)
            elif index == 1:
                model.set_value(iterator, 0, False)
        if model.__class__ is gtk.TreeStore:
            setChild(model, model.iter_children(iterator), index, checked)

    column = cell.get_data('column')
    columns = treeview.get_columns()
    if column <= columns:
        gobject.timeout_add(1, treeview.set_cursor, path, treeview.get_column(column), editNext)

    if refreshCall is not None:
        refreshCall()


def insertTreeViewRow(treeview, value=''):
    """ Inserimento nuova riga nella treeview """
    if value is None:
        return

    model = treeview.get_model()
    iterator = model.append((True, False, value))
    column = treeview.get_column(2)
    row = model[iterator]
    treeview.set_cursor(row.path, column, True)


def deleteTreeViewRow(treeview):
    """ Eliminazione riga dalla treeview """
    sel = treeview.get_selection()
    (model, iterator) = sel.get_selected()

    if iterator is not None:
        model.remove(iterator)

def clearWhereString(wherestring):
    wherestring = []
    return wherestring
