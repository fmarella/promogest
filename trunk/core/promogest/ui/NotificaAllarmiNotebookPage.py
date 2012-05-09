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

from promogest.ui.gtk_compat import *
from promogest.lib.utils import *
#from promogest.dao.Setconf import SetConf
from promogest import Environment
from GladeWidget import GladeWidget
import promogest.dao.Promemoria
from promogest.dao.Promemoria import Promemoria
from promogest.ui.anagPromemoria.AnagraficaPromemoria import AnagraficaPromemoria


class NotificaAllarmiNotebookPage(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, maino, azienda):
        GladeWidget.__init__(self, 'notifica_allarmi_frame',
                                    'notifica_allarmi_notebook.glade')
#        self.placeWindow(self.getTopLevel())
        self.rowBackGround = None
        self.maino = maino
        self.aziendaStr = azienda or ""
        model = self.alarm_notify_treeview.get_model()
        model.clear()
        #get the current alarms from db
        allarmi = promogest.dao.Promemoria.getScadenze()
        #fill again the model of the treeview (a gtk.ListStore)
        for dao in allarmi:
            #dao = Promemoria().getRecord(id=idAllarme)
            model.append((dao, dateToString(dao.data_scadenza),
                                dao.oggetto,
                                dao.descrizione,
                                dao.incaricato,
                                dao.autore,
                                dao.annotazione))


    def on_alarm_notify_treeview_row_activated(self, treeview, path, column):
        model = treeview.get_model()
        dao = model[path][0]
        a = AnagraficaPromemoria()
        a.on_record_edit_activate(a, dao=dao)

    def on_cancel_alarm_button_clicked(self, button):
        """
        viene(vengono) eliminato(i) l'allarme(i) selezionato(i) nella treeview
        """
        count = self.maino.notifica_allarmi.alarm_notify_treeview.get_selection().count_selected_rows()
        msg= 'Sono stati selezionati '+str(count)+' allarmi.\nConfermi l\'eliminazione?'
        if YesNoDialog(msg=msg, transient=None):
            (model, indexes)= self.maino.notifica_allarmi.alarm_notify_treeview.get_selection().get_selected_rows()
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
        (model, indexes)= self.maino.notifica_allarmi.alarm_notify_treeview.get_selection().get_selected_rows()
        rows = []
        for index in indexes:
            iter = model.get_iter(index)
            dao = model.get(iter,0)[0]
            dao.giorni_preavviso += -1
            dao.in_scadenza = False
            dao.persist()
            model.remove(iter)
