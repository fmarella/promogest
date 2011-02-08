# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import gtk
from promogest.ui.utils import *
from promogest.dao.Setconf import SetConf
from promogest import Environment
from GladeWidget import GladeWidget
import promogest.dao.Promemoria
from promogest.dao.Promemoria import Promemoria
from promogest.ui.AnagraficaPromemoria import AnagraficaPromemoria


class NotificaAllarmiNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, mainnn, azienda):
        GladeWidget.__init__(self, 'notifica_allarmi_frame',
                                    'notifica_allarmi_notebook.glade')
#        self.placeWindow(self.getTopLevel())
        self.rowBackGround = None
        self.main = mainnn
        self.aziendaStr = azienda or ""
        gobject.idle_add(self.create_allarmi_frame)

    def drawAllarmi(self):
        """
        disegna questo frame nella finestra principale
        """
        treeview = self.alarm_notify_treeview
        renderer = gtk.CellRendererText()
        rendererCtr = gtk.CellRendererText()
        rendererCtr.set_property('xalign', 0.5)

        column = gtk.TreeViewColumn('Data Scadenza', rendererCtr, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(120)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Oggetto', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Incaricato', rendererCtr, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Autore', rendererCtr, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Annotazioni', renderer, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        model = gtk.ListStore(object, str, str, str, str, str, str)
        treeview.set_model(model)

    def on_alarm_notify_treeview_row_activated(self, treeview, path, column):
        model = treeview.get_model()
        dao = model[path][0]
        a = AnagraficaPromemoria()
        a.on_record_edit_activate(a, dao=dao)

    def on_cancel_alarm_button_clicked(self, button):
        """
        viene(vengono) eliminato(i) l'allarme(i) selezionato(i) nella treeview
        """
        count = self.alarm_notify_treeview.get_selection().count_selected_rows()
        dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Sono stati selezionati '+str(count)+' allarmi.\nConfermi l\'eliminazione?')

        response = dialog.run()
        dialog.destroy()
        if response ==  gtk.RESPONSE_YES:
            (model, indexes)= self.alarm_notify_treeview.get_selection().get_selected_rows()
            rows = []
            for index in indexes:
                iter = model.get_iter(index)
                dao = model.get(iter,0)[0]
                dao.scaduto = True
                dao.completato = True
                dao.in_scadenza = False
                dao.persist()
                model.remove(iter)
        else:
            return

    def on_snooze_alarm_button_clicked(self, button):
            (model, indexes)= self.alarm_notify_treeview.get_selection().get_selected_rows()
            rows = []
            for index in indexes:
                iter = model.get_iter(index)
                dao = model.get(iter,0)[0]
                dao.giorni_preavviso += -1
                dao.in_scadenza = False
                dao.persist()
                model.remove(iter)

    def create_allarmi_frame(self):
        """ creiamo il tab degli allarmi"""
        self.drawAllarmi()
        model = self.alarm_notify_treeview.get_model()
        model.clear()
        #get the current alarms from db
        idAllarmi = promogest.dao.Promemoria.getScadenze()
        #fill again the model of the treeview (a gtk.ListStore)
        for idAllarme in idAllarmi:
            dao = Promemoria().getRecord(id=idAllarme)
            model.append((dao, dateToString(dao.data_scadenza),
                                dao.oggetto,
                                dao.descrizione,
                                dao.incaricato,
                                dao.autore,
                                dao.annotazione))
