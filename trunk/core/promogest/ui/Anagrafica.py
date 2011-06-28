# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Alceste Scalas <alceste@promotux.it>

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

from promogest.ui.gtk_compat import *
from GladeWidget import GladeWidget
import Login



class Anagrafica(GladeWidget):
    """ Classe base per le anagrafiche di Promogest """

    def __init__(self, windowTitle, recordMenuLabel,
                 filterElement, detailElement):
        GladeWidget.__init__(self, 'anagrafica_window')
        Environment.windowGroup.append(self.getTopLevel)
        self._setFilterElement(filterElement)
        self._setDetailElement(detailElement)

        self.anagrafica_window.set_title(windowTitle)

        self.record_menu.get_child().set_label(recordMenuLabel)

        self.anagrafica_current_page_entry.set_alignment(xalign=1)

        self.anagrafica_filter_treeview.set_headers_clickable(True)

        self.filter.draw()
        self.detail.draw()

        self.anagrafica_hpaned.set_position(self.anagrafica_filter_frame.get_allocation().width + 50)
        self.set_focus(self.filter._widgetFirstFocus)


    def _setFilterElement(self, gladeWidget):
        self.filter = gladeWidget
        self.filterTopLevel = gladeWidget.getTopLevel()
        self.anagrafica_filter_vbox.pack_start(self.filterTopLevel, True, True, 0)
        self.filter.setSensitive(True)


    def _setDetailElement(self, gladeWidget):
        self.detail = gladeWidget
        self.detailTopLevel = gladeWidget.getTopLevel()
        self.anagrafica_detail_viewport.add(self.detailTopLevel)
        self.detail.setSensitive(False)


    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura dell'anagrafica """
        self.anagrafica_window.show_all()


    def on_anagrafica_filter_search_button_clicked(self, widget):
        self.filter.gotoFirstPage()


    def on_anagrafica_filter_clear_button_clicked(self, widget):
        self.filter.clear()
        self.filter.gotoFirstPage()


    def gotoPage(self):
        self.filter.gotoPage(self)


    def on_anagrafica_filter_first_button_clicked(self, widget):
        self.filter.gotoFirstPage()


    def on_anagrafica_filter_prev_button_clicked(self, widget):
        self.filter.gotoPrevPage()


    def on_anagrafica_filter_next_button_clicked(self, widget):
        self.filter.gotoNextPage()


    def on_anagrafica_filter_last_button_clicked(self, widget):
        self.filter.gotoLastPage()


    def on_anagrafica_current_page_entry_key_press_event(self, widget, event):
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            pagina = int(self.anagrafica_current_page_entry.get_text())
            self.filter.gotoPage(int(pagina))


    def on_record_new_activate(self, widget):
        self.detail.setSensitive(True)
        self.filter.setSensitive(False)

        self.detail.setDao(None)

        self.record_new_button.set_sensitive(False)
        self.record_new_menu.set_sensitive(False)

        self.record_save_button.set_sensitive(True)
        self.record_save_menu.set_sensitive(True)

        self.record_cancel_button.set_sensitive(True)
        self.record_cancel_menu.set_sensitive(True)

        self.record_undo_button.set_sensitive(False)
        self.record_undo_menu.set_sensitive(False)

        self.record_delete_button.set_sensitive(False)
        self.record_delete_menu.set_sensitive(False)

        self.set_focus(self.detail._widgetFirstFocus)


    def on_record_delete_activate(self, widget):
        if not YesNoDialog(msg='Confermi l\'eliminazione ?', transient=self.getTopLevel()):
            return

        self.detail.deleteDao()
        self.filter.refresh()

        self.detail.setSensitive(False)
        self.filter.setSensitive(True)

        self.record_new_button.set_sensitive(True)
        self.record_new_menu.set_sensitive(True)

        self.record_save_button.set_sensitive(False)
        self.record_save_menu.set_sensitive(False)

        self.record_cancel_button.set_sensitive(False)
        self.record_cancel_menu.set_sensitive(False)

        self.record_undo_button.set_sensitive(False)
        self.record_undo_menu.set_sensitive(False)

        self.record_delete_button.set_sensitive(False)
        self.record_delete_menu.set_sensitive(False)

        self.set_focus(self.filter._widgetFirstFocus)


    def on_record_save_activate(self, widget, path=None, column=None):
        self.detail.saveDao()
        self.filter.refresh()

        self.detail.setSensitive(False)
        self.filter.setSensitive(True)

        self.record_new_button.set_sensitive(True)
        self.record_new_menu.set_sensitive(True)

        self.record_save_button.set_sensitive(False)
        self.record_save_menu.set_sensitive(False)

        self.record_cancel_button.set_sensitive(False)
        self.record_cancel_menu.set_sensitive(False)

        self.record_undo_button.set_sensitive(False)
        self.record_undo_menu.set_sensitive(False)

        self.record_delete_button.set_sensitive(False)
        self.record_delete_menu.set_sensitive(False)

        self.set_focus(self.filter._widgetFirstFocus)


    def on_record_cancel_activate(self, widget):
        if YesNoDialog(msg='Abbandonare le modifiche ?', transient=self.getTopLevel()):
            return

        self.detail.clear()

        self.detail.setSensitive(False)
        self.filter.setSensitive(True)

        self.record_new_button.set_sensitive(True)
        self.record_new_menu.set_sensitive(True)

        self.record_save_button.set_sensitive(False)
        self.record_save_menu.set_sensitive(False)

        self.record_cancel_button.set_sensitive(False)
        self.record_cancel_menu.set_sensitive(False)

        self.record_undo_button.set_sensitive(False)
        self.record_undo_menu.set_sensitive(False)

        self.record_delete_button.set_sensitive(False)
        self.record_delete_menu.set_sensitive(False)

        self.set_focus(self.filter._widgetFirstFocus)


    def on_record_undo_activate(self, widget):
        if YesNoDialog(msg='Cancellare le modifiche ?', transient=self.getTopLevel()):
            return

        self.detail.setSensitive(True)
        self.filter.setSensitive(False)

        self.detail.updateDao()

        self.record_new_button.set_sensitive(False)
        self.record_new_menu.set_sensitive(False)

        self.record_save_button.set_sensitive(True)
        self.record_save_menu.set_sensitive(True)

        self.record_cancel_button.set_sensitive(True)
        self.record_cancel_menu.set_sensitive(True)

        self.record_undo_button.set_sensitive(True)
        self.record_undo_menu.set_sensitive(True)

        self.record_edit_button.set_sensitive(False)
        self.record_edit_menu.set_sensitive(False)

        self.duplica_button.set_sensitive(False)

        self.set_focus(self.detail._widgetFirstFocus)


    def on_record_edit_activate(self, widget, path=None, column=None, dao=None):
        print "SEIIIIIIIIIIIIIIIIIIIIIIITUUUU", dao
        self.detail.setSensitive(True)
        self.filter.setSensitive(False)

        self.detail.updateDao()

        self.record_new_button.set_sensitive(False)
        self.record_new_menu.set_sensitive(False)

        self.record_save_button.set_sensitive(True)
        self.record_save_menu.set_sensitive(True)

        self.record_cancel_button.set_sensitive(True)
        self.record_cancel_menu.set_sensitive(True)

        self.record_undo_button.set_sensitive(True)
        self.record_undo_menu.set_sensitive(True)

        self.record_delete_button.set_sensitive(True)
        self.record_delete_menu.set_sensitive(True)

        self.record_edit_button.set_sensitive(False)
        self.record_edit_menu.set_sensitive(False)
        self.duplica_button.set_sensitive(False)
        self.set_focus(self.detail._widgetFirstFocus)


    def set_focus(self, widget):
        if widget is not None:
            widget.grab_focus()


    def on_toggle_filter_button_clicked(self, widget):
        if self.toggle_filter_button.get_active():
            if self.anagrafica_hpaned.get_position() == 0:
                self.anagrafica_hpaned.set_position(self.anagrafica_filter_frame.get_allocation().width + 50)
        else:
            self.anagrafica_hpaned.set_position(0)


    def on_anagrafica_filter_treeview_cursor_changed(self, treeview):
        sel = self.anagrafica_filter_treeview.get_selection()
        (model, iterator) = sel.get_selected()

        if iterator is None:
            print 'Anagrafica.on_anagrafica_filter_treeview_cursor_changed(): FIXME: iterator is None!'
            return

        dao = model.get_value(iterator, 0)

        self.detail.setDao(dao)

        self.duplica_button.set_sensitive(True)
        self.record_edit_button.set_sensitive(True)
        self.record_edit_menu.set_sensitive(True)


    def on_anagrafica_window_close(self, widget, event=None):
        if self.detail._isSensitive:
            if YesNoDialog(msg='Confermi la chiusura ?', transient=self.getTopLevel()):
                self.anagrafica_window.destroy()
            else:
                return True
        else:
            self.anagrafica_window.destroy()



class AnagraficaFilter(GladeWidget):
    """ Filtro per la ricerca nell'anagrafica articoli """

    def __init__(self, anagrafica, rootWidget,isModule=False):
        GladeWidget.__init__(self, rootWidget,isModule=isModule)
        self._anagrafica = anagrafica
        self._widgetFirstFocus = None
        self._isSensitive = True

        self.batchSize = 30
        self.offset = 0
        self.numRecords = 0
        self.orderBy = None


    def draw(self):
        """
        Disegna i contenuti del filtro anagrafica.  Metodo invocato
        una sola volta, dopo la costruzione dell'oggetto
        """
        raise NotImplementedError


    def setSensitive(self, isSensitive, currWidget=None):
        """
        Set sensitive/insensitive status
        """
        if currWidget is None:
            currWidget = self.getTopLevel()
            self._isSensitive = isSensitive
            # We also change our treeview, since we're strictly coupled
            self._anagrafica.anagrafica_filter_main_vbox.set_sensitive(isSensitive)


    def clear(self):
        """ Ripulisci il filtro di ricerca e aggiorna la ricerca stessa """
        raise NotImplementedError


    def refresh(self):
        """ Aggiorna il filtro di ricerca in base ai parametri impostati """
        raise NotImplementedError


    def gotoFirstPage(self):
        self.offset = 0
        self._refreshCurrentPage()


    def gotoPrevPage(self):
        if self.offset > 0:
            self.offset -= self.batchSize
        self._refreshCurrentPage()


    def gotoPage(self, pagina):
        if pagina <= math.ceil(float(self.numRecords)
                               / float(self.batchSize)):
            self.offset = (pagina - 1) * self.batchSize
            self._refreshCurrentPage()


    def gotoNextPage(self):
        if self.offset < (self.numRecords-self.batchSize):
            self.offset += self.batchSize
        self._refreshCurrentPage()


    def gotoLastPage(self):
        self.offset = (self._getPageCount() - 1) * self.batchSize
        self._refreshCurrentPage()


    def _getCurrentPage(self):
        return self.offset / self.batchSize + 1


    def _getPageCount(self):
        return int(math.ceil(float(self.numRecords)
                             / float(self.batchSize)))



    def _refreshCurrentPage(self):
        currPage = self._getCurrentPage()
        self._anagrafica.anagrafica_current_page_entry.set_sensitive(True)
        self._anagrafica.anagrafica_current_page_entry.set_text(str(currPage))
        self.refresh()


    def _refreshPageCount(self):
        self._anagrafica.anagrafica_filter_total_count.set_text(str(self._getPageCount()))


    def on_campo_filter_entry_key_press_event(self, widget, event):
        """ Conferma o eliminazione parametri filtro da tastiera"""
        keyname = gdk_keyval_name(event.keyval)

        if keyname == 'Escape':
            self._anagrafica.on_anagrafica_filter_clear_button_clicked(widget)
        elif keyname == 'Return' or keyname == 'KP_Enter':
            self._anagrafica.on_anagrafica_filter_search_button_clicked(widget)


    def _changeOrderBy(self, widget, campi):
        #print "CAMBIO L'ORDINE DEI RISULTATI ORDINANDO PER ", campi
        self.orderBy = campi
        self.refresh()



class AnagraficaDetail(GladeWidget):
    """ Dettaglio dell'anagrafica articoli """

    def __init__(self, anagrafica, rootWidget):
        GladeWidget.__init__(self, rootWidget)
##        Login.windowGroup.append(self.getTopLevel())
        self._anagrafica = anagrafica
        self._widgetFirstFocus = None
        self._isSensitive = True


    def draw(self):
        """
        Disegna i contenuti del dettaglio anagrafica.  Metodo invocato
        una sola volta, dopo la costruzione dell'oggetto
        """
        raise NotImplementedError


    def setSensitive(self, isSensitive, currWidget=None):
        """
        Set sensitive/insensitive status
        """
        if currWidget is None:
            currWidget = self.getTopLevel()
            self._isSensitive = isSensitive

        # FIXME: a better way to find a widget going to be enabled/disabled?
        if isinstance(currWidget, (gtk.ComboBox, gtk.TreeView,
                                   gtk.Editable, gtk.Button, gtk.TextView)):
            currWidget.set_sensitive(isSensitive)
        elif isinstance(currWidget, gtk.Container):
            for child in currWidget.get_children():
                self.setSensitive(isSensitive, child)


    def clear(self):
        """ Svuota tutti i campi di input del dettaglio anagrafica """
        raise NotImplementedError


    def setDao(self, dao):
        """ Visualizza il Dao specificato """
        raise NotImplementedError


    def updateDao(self):
        """ Aggiorna il dao selezionato all'ultima versione sul DB """
        raise NotImplementedError


    def saveDao(self, dao):
        """ Salva il Dao attualmente selezionato """
        raise NotImplementedError


    def deleteDao(self):
        """ Elimina il dao selezionato """
        raise NotImplementedError
