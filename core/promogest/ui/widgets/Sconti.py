# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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
from promogest.lib.utils import *
from promogest import Environment
from SignedDecimalEntryField import SignedDecimalEntryField


class Sconti(GladeWidget):
    """ Classe base per l'inserimento e la modifica degli sconti """

    def __init__(self, windowTitle="", sconti=None, applicazione='scalare', percentuale=True, valore=True):
        GladeWidget.__init__(self, root='sconti_window', path="sconti_window.glade")

        self.listSconti = []
        self.stringApplicazione = ''
        if not windowTitle:windowTitle=""
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
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Tipo', rendererSx, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
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
                decimals = int(setconf(key="decimals", section="Numbers"))
            model.append((('%.' + str(decimals) + 'f') % float(s["valore"]), s["tipo"]))
        self.sconti_treeview.set_model(model)

        self._currentIterator = None
        self.valore_entry.set_alignment(1)


    def CreateSignedMoneyEntryField(self, str1, str2, int1, int2):
        return SignedDecimalEntryField(str1, str2, int1, int(setconf(key="decimals", section="Numbers")))


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
            decimals = int(setconf(key="decimals", section="Numbers"))
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
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Return' or keyname == 'KP_Enter':
            self.confirm_button.grab_focus()
            self.on_confirm_button_clicked(widget)


    def on_confirm_button_clicked(self, widget):
        if self.valore_entry.get_text() and float(self.valore_entry.get_text()) == 0:
            messageInfo(msg='Inserire lo sconto !')
            self.valore_entry.grab_focus()
            return

        if (not(self.percentuale_radiobutton.get_active()) and
            not(self.valore_radiobutton.get_active())):
            messageInfo(msg='Inserire il tipo !')
            self.self.percentuale_radiobutton.grab_focus()
            return

        model = self.sconti_treeview.get_model()
        decimals = '2'
        tipo = ''

        if self.percentuale_radiobutton.get_active():
            tipo = "percentuale"
        elif self.valore_radiobutton.get_active():
            tipo = "valore"
            decimals = int(setconf(key="decimals", section="Numbers"))

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
                    decimals = int(setconf(key="decimals", section="Numbers"))
                valore = ('%-10.' + str(decimals) + 'f') % float(r[0])
                self.listSconti.append({"valore": valore.strip(), "tipo": tipo})
            except:
                messageError(msg='Valori non corretti:' + r[0] + ', ' + r[1] + ' !')
                return
        self.sconti_window.hide()


    def on_sconti_window_close(self, widget, event=None):
        self.sconti_window.destroy()
        return None
