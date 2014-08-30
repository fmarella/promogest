# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                  di Francesco Meloni snc - http://www.promotux.it/

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

try:
    import pysvn
except ImportError:
    pysvn = None
import threading
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.gtk_compat import *
from promogest.lib.utils import get_local_version, get_web_remote_version


class UpdateDialog(GladeWidget):
    '''
    Finestra di aggiornamento
    '''

    def __init__(self, parent):
        '''
        Inizializza la finestra di aggiornamento
        '''
        GladeWidget.__init__(self, root='update_progress_dialog', path='update_progress_dialog.glade')
        self._parent = parent
        self._rev_locale = None
        self._rev_remota = None
        self.__stop = False
        self.__aggiornato=False

    def aggiornaLabel(self):

        def fetchThread(data):
            data.msg_label.set_text("Lettura versioni locale e remota in corso...")
            data._rev_locale = get_local_version()
            data._rev_remota = get_web_remote_version()

        def refreshUI():
            if self.__stop:
                return False

            if self._rev_locale and self._rev_remota:
                if self._rev_locale < self._rev_remota:
                    #TODO: usare ngettext
                    num = self._rev_remota - self._rev_locale
                    if num == 1:
                        self.msg_label.set_text('E\' disponibile un aggiornamento.')
                    else:
                        self.msg_label.set_text('Sono disponibili %d aggiornamenti.' % num)

                    self.update_button.set_sensitive(True)
                    self.cancel_button.set_sensitive(True)
                    self.update_progress_bar.set_fraction(1.0)
                    return False
                else:
                    self.msg_label.set_text('PromoGest è aggiornato all\'ultima versione')
                    self.cancel_button.set_sensitive(True)
                    self.update_progress_bar.set_fraction(1.0)
                    return False
            self.update_progress_bar.pulse()
            return True
        gobject.timeout_add(100, refreshUI)

        self.t = threading.Thread(group=None, target=fetchThread,
                        name='Data rendering thread', args=([self]),
                        kwargs={})
        self.t.start()


    def sync(self):

        def updateThread(data):
            if not pysvn:
                data.__stop = True
                return
            try:
                client = pysvn.Client()
                data.msg_label.set_text("Aggiornamento in corso...")
                data.update_button.set_sensitive(False)
                data.__stop = client.update('.')
            except:
                data.msg_label.set_text("Si è verificato un problema in aggiornamento, PromoGest verrà ripristinato...")
                client = pysvn.Client()
                client.cleanup('.')
                data.__stop = True
                data.update_progress_bar.set_fraction(1.0)
                data.cancel_button.set_sensitive(True)
                data.msg_label.set_text("Ripristino completato, riavviare PromoGest.")
            else:
                data.update_progress_bar.set_fraction(1.0)
                data.msg_label.set_text("Aggiornamento eseguito con successo, riavvio.")
                data.cancel_button.set_sensitive(True)
                self.__aggiornato=True

        def refreshUI():
            if self.__stop:
                return False
            else:
                self.update_progress_bar.pulse()
                return True
        gobject.timeout_add(100, refreshUI)

        self.t = threading.Thread(group=None, target=updateThread,
                        name='Data rendering thread', args=([self]),
                        kwargs={})
        self.t.start()


    def show(self):
        self.update_progress_dialog.set_transient_for(self._parent.getTopLevel())
        self.update_progress_dialog.show()
        self.aggiornaLabel()

    def on_update_button_clicked(self, widget):
        self.sync()


    def on_cancel_button_clicked(self, widget):
        self.t.join()
        self.update_progress_dialog.destroy()
        if self.__aggiornato:
            Environment.restart_program()
