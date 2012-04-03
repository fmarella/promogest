# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Alceste Scalas <alceste@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni <francesco@promotux.it>
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

from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.gtk_compat import *
from promogest.ui.utils import setconf


class AnagraficaFilter(GladeWidget):
    """ Filtro per la ricerca nell'anagrafica articoli """

    def __init__(self, anagrafica, rootWidget,
                                    gladeFile=None,
                                    module=False):
        GladeWidget.__init__(self, rootWidget, fileName=gladeFile, isModule=module)
        self._anagrafica = anagrafica
        self._widgetFirstFocus = None
        self._isSensitive = True
        self._treeViewModel = None

        # A closure that returns a list of Dao's that match the
        # current filter parameters.  It is invoked through
        # self.runFilter() (unless the derived classes redefine it)
        #
        # This closure takes two parameters: offset and batchSize
        def __defaultFilterClosure(offset, batchSize):
            raise NotImplementedError
        self._filterClosure = __defaultFilterClosure

        # Same concept as above, but this closure counts filter results
        def __defaultFilterCountClosure():
            raise NotImplementedError
        self._filterCountClosure = __defaultFilterCountClosure


    def build(self):
        """ reindirizza alcuni campi e metodi dal filterWidget """
        self.bodyWidget = self._anagrafica.bodyWidget
        # mapping fields and methods from bodyWidget to this class
        self._changeOrderBy = self.bodyWidget._changeOrderBy
        self.orderBy = self.bodyWidget.orderBy = None
        self.join =self.bodyWidget.join =None
        self.batchSize = setconf("Numbers", "batch_size")
        model = self._anagrafica.batchsize_combo.get_model()
        for r in model:
            if r[0] == int(self.batchSize):
                self._anagrafica.batchsize_combo.set_active_iter(r.iter)

        self.offset = self.bodyWidget.offset = 0
        self.numRecords = self.bodyWidget.numRecords = 0

    def draw(self):
        """
        Disegna i contenuti del filtro anagrafica.  Metodo invocato
        una sola volta, dopo la costruzione dell'oggetto
        """
        raise NotImplementedError

    def clear(self):
        """ Ripulisci il filtro di ricerca e aggiorna la ricerca stessa """
        raise NotImplementedError

    def on_filter_entry_changed(self, text):
        # stringa = text.get_text()
        def bobo():
            self.refresh()
        gobject.idle_add(bobo)

    def refresh(self):
        """ Aggiorna il filtro di ricerca in base ai parametri impostati """
        raise NotImplementedError

    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ Gestisce la conferma ed apertura della anagrafica """
        self._anagrafica.on_anagrafica_filter_treeview_row_activated(treeview, path, column)


    def on_filter_treeview_cursor_changed(self, treeview):
        """ Gestisce lo spostamento tra le righe """
        self._anagrafica.on_anagrafica_filter_treeview_cursor_changed(treeview)

    def on_filter_treeview_selection_changed(self, treeSelection):
        """
        Gestisce le selezioni multiple (se attive)
        """
        self._anagrafica.on_anagrafica_filter_treeview_selection_changed(treeSelection)

    def runFilter(self, offset='__default__', batchSize='__default__',
                                      progressCB=None, progressBatchSize=0):
        """ Recupera i dati """
        self.bodyWidget.orderBy = self.orderBy
        if batchSize == '__default__' and  self._anagrafica.batchsize_combo.get_active_iter():
            iterator = self._anagrafica.batchsize_combo.get_active_iter()
            model = self._anagrafica.batchsize_combo.get_model()
            if iterator is not None:
                batchSize = model.get_value(iterator, 0)
        return self.bodyWidget.runFilter(offset=offset, batchSize=batchSize,
                                         progressCB=progressCB, progressBatchSize=progressBatchSize,
                                         filterClosure=self._filterClosure)

    def countFilterResults(self):
        """ Conta i dati """
        totale_daos = self.bodyWidget.countFilterResults(self._filterCountClosure)
        self._anagrafica.tot_daos_label.set_markup(" <b>"+str(totale_daos or "Nessuno")+"</b>")
        return totale_daos

    def _refreshPageCount(self):
        """ Aggiorna la paginazione """
        self.bodyWidget.numRecords = self.numRecords
        self.bodyWidget._refreshPageCount()

    def selectCurrentDao(self):
        """ Select the dao currently shown in the HTML detail (if possible) """
        def foreach_handler(model, path, iter, selection):
            # Get value from current row, column 1
            dao = model.get_value(iter, 0)
            if dao.sameRecord(self._anagrafica._selectedDao):
                selection.select_path(path)
                self._anagrafica.on_anagrafica_filter_treeview_cursor_changed(self._anagrafica.anagrafica_filter_treeview)
                return True
            else:
                return False

        treeView = self._anagrafica.anagrafica_filter_treeview
        selection = treeView.get_selection()
        if selection:
            selection.unselect_all()
            model = treeView.get_model()

            model.foreach(foreach_handler, selection)

    def getSelectedDao(self):
        treeViewSelection = self._anagrafica.anagrafica_filter_treeview.get_selection()
        if not treeViewSelection:
            return None
        if treeViewSelection.get_mode() != GTK_SELECTIONMODE_MULTIPLE:
            (model, iterator) = treeViewSelection.get_selected()
            if iterator is not None:
                dao = model.get_value(iterator, 0)
            else:
                dao = None
        else:
            model, iterator = treeViewSelection.get_selected_rows()
            count = treeViewSelection.count_selected_rows()
            if count == 1:
                dao = model[iterator[0]][0]
                # daoSelection = None
            else:
                dao = None
        return dao
            
    def getSelectedDaos(self):
        treeViewSelection = self._anagrafica.anagrafica_filter_treeview.get_selection()
        if not treeViewSelection:
            return None
        if treeViewSelection.get_mode() == GTK_SELECTIONMODE_MULTIPLE:
            model, iterator = treeViewSelection.get_selected_rows()
            daos = []
            for i in iterator:
                daos.append(model[i][0])
            return daos
        else:
            return None

    def getTreeViewModel(self):
        return self._treeViewModel

    def on_campo_filter_entry_key_press_event(self, widget, event):
        return self._anagrafica.bodyWidget.on_filter_element_key_press_event(widget, event)

    def setFocus(self, widget=None):
        self._anagrafica.bodyWidget.setFocus(widget)
