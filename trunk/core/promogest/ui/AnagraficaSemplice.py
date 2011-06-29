# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

from promogest.ui.gtk_compat import *
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.widgets.FilterWidget import FilterWidget
from promogest.ui.SendEmail import SendEmail
import Login
from promogest.ui.utils import setconf, YesNoDialog
from promogest import Environment


class Anagrafica(GladeWidget):
    """ Classe base per le anagrafiche semplici """

    def __init__(self, windowTitle, recordMenuLabel,
                 filterElement, detailElement, gladeFile=None):
        GladeWidget.__init__(self, 'anagrafica_semplice_window',
                                fileName= 'anagrafica_semplice_window.glade')
        Environment.windowGroup.append(self.anagrafica_semplice_window)
        self.anagrafica_semplice_window.set_title(windowTitle)
        self.record_menu.get_child().set_label(recordMenuLabel)

        self.bodyWidget = FilterWidget(owner=self, filtersElement=filterElement)
        #self.anagrafica_scrolledwindow.add(self.bodyWidget.getTopLevel())
        self.anagrafica_viewport.add(self.bodyWidget.getTopLevel())
        self.bodyWidget.filter_body_label.set_no_show_all(True)
        self.bodyWidget.filter_body_label.set_property('visible', False)
        self.bodyWidget.generic_button.set_no_show_all(True)
        self.bodyWidget.generic_button.set_property('visible', False)

        self.filter = self.bodyWidget.filtersElement

        self.filterTopLevel = self.filter.getTopLevel()
        self.filterTopLevel.set_sensitive(True)

        self.detail = detailElement

        self.anagrafica_treeview = self.bodyWidget.resultsElement
        self._treeViewModel = None
        self._rowEditingPath = None
        self._tabPressed = False

        # mapping fields and methods from bodyWidget to this class
        self.anagrafica_filter_navigation_hbox = self.bodyWidget.filter_navigation_hbox
        self.anagrafica_filter_frame = self.bodyWidget.filter_frame
        self._widgetFirstFocus = self.bodyWidget._firstFocusWidget
        self._changeOrderBy = self.bodyWidget._changeOrderBy
        self.orderBy = self.bodyWidget.orderBy = None
        self.batchSize = self.bodyWidget.batchSize = int(setconf("Numbers", "batch_size"))
        self.offset = self.bodyWidget.offset = 0
        self.numRecords = self.bodyWidget.numRecords = 0
        self._filterClosure = None

        self.placeWindow(self.anagrafica_semplice_window)
        self.draw()
        self.setFocus()


    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura dell'anagrafica """
        self.anagrafica_semplice_window.show_all()

    def on_credits_menu_activate(self, widget):
        creditsDialog = GladeWidget('credits_dialog', callbacks_proxy=self)
        creditsDialog.getTopLevel().set_transient_for(self.getTopLevel())
        creditsDialog.getTopLevel().show_all()
        response = creditsDialog.credits_dialog.run()
        if response == GTK_RESPONSE_OK:
            creditsDialog.credits_dialog.destroy()

    def on_send_Email_activate(self, widget):
        sendemail = SendEmail()


    def on_licenza_menu_activate(self, widget):
        licenzaDialog = GladeWidget('licenza_dialog', callbacks_proxy=self)
        licenzaDialog.getTopLevel().set_transient_for(self.getTopLevel())
        licenseText = ''
        try:
            lines = open('./LICENSE').readlines()
            for l in lines:
                licenseText += l
        except:
            licenseText = 'Lavori in corso ....'
            print 'License file not found (LICENSE).'
        textBuffer = licenzaDialog.licenza_textview.get_buffer()
        textBuffer.set_text(licenseText)
        licenzaDialog.licenza_textview.set_buffer(textBuffer)
        licenzaDialog.getTopLevel().show_all()
        response = licenzaDialog.licenza_dialog.run()
        if response == GTK_RESPONSE_OK:
            licenzaDialog.licenza_dialog.destroy()


    def on_seriale_menu_activate(self, widget):
        try:
            fileName = Environment.conf.guiDir + 'logo_promogest.png'
            f = open(fileName,'rb')
            content = f.read()
            f.close()
            msg = 'Codice installazione:\n\n' + str(md5.new(content).hexdigest().upper())
        except:
            msg = 'Impossibile generare il codice !!!'
        messageInfo(msg=msg)

    def on_record_new_activate(self, widget,codice=None):
        """ Nuovo record """
        if codice:
            self.detail.setDao(None, codice=codice)
        else:
            self.detail.setDao(None)
        if self._windowName == 'AnagraficaBanche':
            from AnagraficaBancheEdit import AnagraficaBancheEdit
            anag = AnagraficaBancheEdit(self, codice=codice)
            return
        self.filterTopLevel.set_sensitive(False)
        self.anagrafica_filter_navigation_hbox.set_sensitive(False)
        self.anagrafica_filter_frame.set_sensitive(False)
        self.anagrafica_treeview_set_edit(True)
        self.anagrafica_treeview.set_headers_clickable(False)
        self.anagrafica_treeview.set_enable_search(False)

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


    def on_record_delete_activate(self, widget):
        """ Eliminazione record """
        if not YesNoDialog(msg='Confermi l\'eliminazione ?', transient=None):
            self.anagrafica_treeview.grab_focus()
            return
        self.detail.deleteDao()
        self.refresh()

        self.filterTopLevel.set_sensitive(True)
        self.anagrafica_filter_navigation_hbox.set_sensitive(True)
        self.anagrafica_filter_frame.set_sensitive(True)
        self.anagrafica_treeview_set_edit(False)
        self.anagrafica_treeview.set_headers_clickable(True)
        self.anagrafica_treeview.set_enable_search(True)

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

        self.setFocus()


    def on_record_save_activate(self, widget, path=None, column=None):
        """ Salvataggio record """
        self.anagrafica_treeview.grab_focus()
        try:
            self.detail.saveDao()
        except Exception:
            self.anagrafica_treeview_set_edit(True)
            return

        self.filterTopLevel.set_sensitive(True)
        self.anagrafica_filter_navigation_hbox.set_sensitive(True)
        self.anagrafica_filter_frame.set_sensitive(True)
        self.anagrafica_treeview_set_edit(False)
        self.anagrafica_treeview.set_headers_clickable(True)
        self.anagrafica_treeview.set_enable_search(True)

        self.refresh()

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

        self.setFocus()


    def on_record_cancel_activate(self, widget):
        """ Annullamento modifiche record """

        if self._rowEditingPath is None:
            return
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                                   GTK_DIALOG_MESSAGE_QUESTION,
                                   GTK_BUTTON_YES_NO,
                                   'Abbandonare le modifiche ?')

        response = dialog.run()
        dialog.destroy()
        if response != GTK_RESPONSE_YES:
            self.anagrafica_treeview.grab_focus()
            return

        self.anagrafica_treeview.grab_focus()
        self.detail.updateDao()

        self.filterTopLevel.set_sensitive(True)
        self.anagrafica_filter_navigation_hbox.set_sensitive(True)
        self.anagrafica_filter_frame.set_sensitive(True)
        self.anagrafica_treeview_set_edit(False)
        self.anagrafica_treeview.set_headers_clickable(True)
        self.anagrafica_treeview.set_enable_search(True)

        self.refresh()

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

        self.setFocus()

    def on_export_csv_button_clicked(self, button):
        dao = self.detail.setDao(None)
        from ExportCsv import ExportCsv
        anag = ExportCsv(self, dao=dao)
        dao=None
        return


    def on_record_undo_activate(self, widget):
        """ Rilettura record """
        if self._rowEditingPath is None:
            return
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                                   GTK_DIALOG_MESSAGE_QUESTION,
                                   GTK_BUTTON_YES_NO,
                                   'Cancellare le modifiche ?')

        response = dialog.run()
        dialog.destroy()
        if response != GTK_RESPONSE_YES:
            self.anagrafica_treeview.grab_focus()
            self.anagrafica_treeview_set_edit(True)
            return

        self.anagrafica_treeview.grab_focus()
        self.detail.updateDao()

        self.filterTopLevel.set_sensitive(False)
        self.anagrafica_filter_navigation_hbox.set_sensitive(False)
        self.anagrafica_filter_frame.set_sensitive(False)
        self.anagrafica_treeview.set_headers_clickable(False)
        self.anagrafica_treeview.set_enable_search(False)

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


    def on_record_edit_activate(self, widget):
        """ Modifica record """
        self.detail.updateDao()
        if self._windowName == 'AnagraficaBanche':
            from AnagraficaBancheEdit import AnagraficaBancheEdit
            anag = AnagraficaBancheEdit(self, dao=self.detail.dao)
            return
        self.filterTopLevel.set_sensitive(False)
        self.anagrafica_filter_navigation_hbox.set_sensitive(False)
        self.anagrafica_filter_frame.set_sensitive(False)
        self.anagrafica_treeview_set_edit(True)
        self.anagrafica_treeview.set_headers_clickable(False)
        self.anagrafica_treeview.set_enable_search(False)

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


    def setFocus(self, widget=None):
        """ Da il fuoco al widget indicato o al primo widget """
        if widget is None:
            self.filter._widgetFirstFocus.grab_focus()
        else:
            widget.grab_focus()


    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ Gestisce la conferma della riga """
        if self._rowEditingPath is None:
            self.on_record_edit_activate(self.record_edit_button)


    def on_filter_treeview_cursor_changed(self, treeview):
        """ Gestisce lo spostamento tra le righe """
        sel = self.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if self._rowEditingPath is not None:
            if iterator:
                row = model[iterator]
                if row.path != self._rowEditingPath:
                    sel.select_path(self._rowEditingPath)
                return
        else:
            if iterator is None:
                return

            dao = model.get_value(iterator, 0)

            self.detail.setDao(dao)

            self.record_edit_button.set_sensitive(True)
            self.record_edit_menu.set_sensitive(True)

    def on_filter_treeview_selection_changed(self, selection):
        pass

    def _newRow(self, modelRow):
        """ Crea una nuova riga """
        sel = self.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        iterator = model.append(modelRow)
        sel.select_iter(iterator)


    def _getRowEditingPath(self, model, iterator):
        """ Restituisce il path relativo alla riga che e' in modifica """
        if iterator is not None:
            row = model[iterator]
            self._rowEditingPath = row.path


    def on_filter_treeview_keypress_event(self, treeview, event):
        """ Gestisce la pressione del tab su una cella """
        if event.keyval == 65289:
            self._tabPressed = True


    def on_column_edited(self, cell, path, value, treeview, editNext=True, column = None):
        """ Gestisce l'immagazzinamento dei valori nelle celle """
        model = treeview.get_model()
        iterator = model.get_iter(path)
        if column is None:
            column = cell.get_data('column')
        row = model[iterator]
        if row.path == self._rowEditingPath:
            if cell.__class__ is gtk.CellRendererText:
                try:
                    length = cell.get_data('max_length')
                    model.set_value(iterator, column+1, value[:length])
                except:
                    model.set_value(iterator, column+1, value)
            elif cell.__class__ is gtk.CellRendererToggle:
                model.set_value(iterator, column+1, not cell.get_active())

        columns = treeview.get_columns()
        if column+1 <= columns:
            if self._tabPressed:
                self._tabPressed = False
            if Environment.pg3:
                gobject.timeout_add(1, treeview.set_cursor, gtk.TreePath(str(path)), treeview.get_column(column+1), editNext)
            else:
                gobject.timeout_add(1, treeview.set_cursor,path, treeview.get_column(column+1), editNext)


    def anagrafica_treeview_set_edit(self, flag):
        """ Mette la riga corrente della treeview in stato di edit / browse """
        sel = self.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        columns = self.anagrafica_treeview.get_columns()
        for c in columns:
            renderers = c.get_cells()
            for r in renderers:
                if r.__class__ is gtk.CellRendererText:
                    r.set_property('editable', flag)
                elif r.__class__ is gtk.CellRendererToggle:
                    r.set_property('activatable', flag)
        if flag:
            self._getRowEditingPath(model, iterator)
            row = model[iterator]
            column = self.anagrafica_treeview.get_column(0)
            self.anagrafica_treeview.grab_focus()
            if Environment.pg3:
                self.anagrafica_treeview.set_cursor(row.path, column, True)
            else:
                self.anagrafica_treeview.set_cursor(row.path, column, start_editing=True)
        else:
            self._rowEditingPath = None


    def on_anagrafica_window_close(self, widget, event=None):
        """ Gestisce la richiesta di uscita dall'anagrafica """
        if self._rowEditingPath is not None:
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                       GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                                       GTK_DIALOG_MESSAGE_QUESTION,
                                       GTK_BUTTON_YES_NO,
                                       'Confermi la chiusura ?')
            response = dialog.run()
            dialog.destroy()
            if response != GTK_RESPONSE_YES:
                return True

        self.destroy()


    def draw(self):
        """
        Disegna i contenuti dell'elenco dell' anagrafica. Metodo invocato
        una sola volta, dopo la costruzione dell'oggetto
        """
        raise NotImplementedError


    def refresh(self):
        """ Aggiorna il l'elenco dell'anagrafica in base ai parametri impostati """
        raise NotImplementedError


    def clear(self):
        """ Annulla i parametri impostati per la ricerca """
        self.filter.clear()


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



class AnagraficaFilter(GladeWidget):
    """ Filtro per la ricerca nell'anagrafica """

    def __init__(self, anagrafica, rootWidget,
                                    gladeFile=None,module=False):
        GladeWidget.__init__(self, rootWidget,
                        fileName=gladeFile,isModule=module)

        self._anagrafica = anagrafica
        self._widgetFirstFocus = None

    def on_column_edited(self,cellrenderertext, path, new_text ,editNext=True):
        """ Tentativo di automazzare il calcolo del posizionamento
        della colonna dentro la treeview, apparentemente non si sa
        quando si edita una cella a quale colonna appartenga e cmq
        in che posizione quella colonna si trovi, andrea a suo tempo
        aveva forzato il posizionamento con una property ad hoc.
        Soluzione che sembra funzionare anche con pygi
        col.cell_get_position(cellrenderertext) restituisce None
        su pygtk quando non è la colonna in cui è presente la cellrenderer
        mentre su pygi c'è sempre una tupla di due valori
        quando però non è la colonna coinvola sono a zero o negativi
        per cui mi basta verificare che uno o entrambi  ivalori siano
        maggiori di zero per considerare la colonna corretta
        MONITORARE"""
        column = None
        colonne = self.anagrafica_semplice_treeview.get_columns()
        for col in colonne:
            if col.cell_get_position(cellrenderertext) and (col.cell_get_position(cellrenderertext)[0] > 0 or col.cell_get_position(cellrenderertext)[1] > 0) :
                column = colonne.index(col)
                break
        #column = cellrenderertext.get_data('column') or 0
        self._anagrafica.on_column_edited(cell=cellrenderertext,
                path=path,
                value=new_text,
                treeview=self.anagrafica_semplice_treeview,
                editNext=True,
                column=column)

    def refresh(self):
        """ Aggiorna il l'elenco dell'anagrafica in base ai parametri impostati """
        self._anagrafica.refresh()


    def clear(self):
        """ Annulla i parametri impostati per la ricerca """
        raise NotImplementedError


    def _filterClosure(self, offset, batchSize):
        """ Closure implemented by derived class """
        raise NotImplementedError


    def on_campo_filter_entry_key_press_event(self, widget, event):
        return self._anagrafica.bodyWidget.on_filter_element_key_press_event(widget, event)



class AnagraficaDetail(object):
    """ Dettaglio dell'anagrafica """

    def __init__(self, anagrafica, gladeFile=None,module=False):
        self._anagrafica = anagrafica
        self._widgetFirstFocus = None


    def draw(self):
        """
        Disegna i contenuti del dettaglio anagrafica.  Metodo invocato
        una sola volta, dopo la costruzione dell'oggetto
        """
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
