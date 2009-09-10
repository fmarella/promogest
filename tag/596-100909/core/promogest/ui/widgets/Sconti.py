# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>

import gtk
from promogest.ui.GladeWidget import GladeWidget

from promogest import Environment
from SignedDecimalEntryField import SignedDecimalEntryField

class Sconti(GladeWidget):
    """ Classe base per l'inserimento e la modifica degli sconti """

    def __init__(self, windowTitle, sconti=None, applicazione='scalare', percentuale=True, valore=True):
        GladeWidget.__init__(self, 'sconti_window')

        self.listSconti = []
        self.stringApplicazione = ''

        self.sconti_window.set_title(windowTitle)
        self.sconti_treeview.set_headers_clickable(False)
        self.percentuale_radiobutton.set_sensitive(percentuale)
        self.valore_radiobutton.set_sensitive(valore)
        self.percentuale_radiobutton.set_active(True)
        if applicazione == 'scalare':
            self.applicazione_sconti_combobox.set_active(0)
        elif applicazione == 'non scalare' or applicazione == 'no scalare':
            self.applicazione_sconti_combobox.set_active(1)
        else:
            self.applicazione_sconti_combobox.set_active(0)

        self.valore_entry.grab_focus()

        treeview = self.sconti_treeview
        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Sconto', rendererDx, text=0)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Tipo', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        model = gtk.ListStore(str, str)
        model.clear()

        if sconti is None:
            sconti = []
        self.listSconti = sconti
        self.stringApplicazione = applicazione

        for s in self.listSconti:
            decimals = '2'
            if s["tipo"] == 'valore':
                decimals = Environment.conf.decimals
            model.append((('%.' + str(decimals) + 'f') % float(s["valore"]), s["tipo"]))
        self.sconti_treeview.set_model(model)

        self._currentIterator = None
        self.valore_entry.set_alignment(1)


    def CreateSignedMoneyEntryField(self, str1, str2, int1, int2):
        return SignedDecimalEntryField(str1, str2, int1, Environment.conf.decimals)


    def show_all(self):
        self.sconti_window.show_all()


    def on_sconti_treeview_row_activated(self, treeview, path, column):
        sel = self.sconti_treeview.get_selection()
        (model, self._currentIterator) = sel.get_selected()

        decimals = '2'
        if model.get_value(self._currentIterator, 1) == "percentuale":
            self.percentuale_radiobutton.set_active(True)
        elif model.get_value(self._currentIterator, 1) == "valore":
            self.valore_radiobutton.set_active(True)
            decimals = Environment.conf.decimals
        else:
            self.percentuale_radiobutton.set_active(False)
            self.valore_radiobutton.set_active(False)
        self.valore_entry.set_text(('%.' + str(decimals) + 'f') % float(model.get_value(self._currentIterator, 0)))
        self.valore_entry.grab_focus()


    def on_new_button_clicked(self, widget):
        self._currentIterator = None
        self.valore_entry.set_text('')
        self.valore_entry.grab_focus()


    def on_valore_entry_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.confirm_button.grab_focus()
            self.on_confirm_button_clicked(widget)


    def on_confirm_button_clicked(self, widget):
        if (float(self.valore_entry.get_text()) == 0):
            self.show_message('Inserire lo sconto !')
            self.valore_entry.grab_focus()
            return

        if (not(self.percentuale_radiobutton.get_active()) and
            not(self.valore_radiobutton.get_active())):
            self.show_message('Inserire il tipo !')
            self.self.percentuale_radiobutton.grab_focus()
            return

        model = self.sconti_treeview.get_model()
        decimals = '2'
        tipo = ''

        if self.percentuale_radiobutton.get_active():
            tipo = "percentuale"
        elif self.valore_radiobutton.get_active():
            tipo = "valore"
            decimals = Environment.conf.decimals

        valore = ('%.' + str(decimals) + 'f') % float(self.valore_entry.get_text())

        if self._currentIterator is not None:
            model.set_value(self._currentIterator, 0, valore)
            model.set_value(self._currentIterator, 1, tipo)
        else:
            model.append((valore, tipo))
        self.on_new_button_clicked(widget)


    def on_undo_button_clicked(self, widget):
        self.on_new_button_clicked(widget)


    def on_delete_button_clicked(self, widget):
        sel = self.sconti_treeview.get_selection()
        (model, self._currentIterator) = sel.get_selected()
        if self._currentIterator is not None:
            model.remove(self._currentIterator)
            self.on_new_button_clicked(widget)


    def on_conferma_button_clicked(self, widget):
        self.stringApplicazione = self.applicazione_sconti_combobox.get_active_text()
        self.listSconti = []
        model = self.sconti_treeview.get_model()
        for r in model:
            try:
                tipo = r[1]
                decimals = '2'
                if tipo == 'valore':
                    decimals = Environment.conf.decimals
                valore = ('%-10.' + str(decimals) + 'f') % float(r[0])

                self.listSconti.append({"valore": valore, "tipo": tipo})
            except:
                self.show_message('Valori non corretti:' + r[0] + ', ' + r[1] + ' !')
                return
        self.sconti_window.hide()


    def on_sconti_window_close(self, widget, event=None):
        self.sconti_window.destroy()
        return None


    def show_message(self, msg):
        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, msg)
        dialog.run()
        dialog.destroy()
