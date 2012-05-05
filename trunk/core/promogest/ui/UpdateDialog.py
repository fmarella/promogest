# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                  di Francesco Meloni snc - http://www.promotux.it/

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

try:
    import pysvn
except:
    pysvn = None
import threading
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.gtk_compat import *
from promogest.lib.utils import messageWarning


class UpdateDialog(GladeWidget):
    '''
    Finestra di aggiornamento
    '''

    def __init__(self, parent):
        '''
        Inizializza la finestra di aggiornamento
        '''
        GladeWidget.__init__(self, 'update_progress_dialog')
        self._parent = parent
        self._rev_locale = None
        self._rev_remota = None
        self.__stop = False

    def aggiornaLabel(self):

        def fetchThread(data):
            try:
                client = pysvn.Client()
                data.msg_label.set_text("Lettura versioni locale e remota in corso...")
                data._rev_locale = client.info('.').revision.number
                data._rev_remota = pysvn.Client().info2("http://svn.promotux.it/svn/promogest2/trunk/", recurse=False)[0][1]["rev"].number
            except:
                data.__stop = True
                data.msg_label.set_text("Si è verificato un errore nella lettura della revisioni,\nattendere alcuni minuti e riprovare")
                self.cancel_button.set_sensitive(True)

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

                    # client = pysvn.Client()
                    # critico = False

                    # rev_locale = client.info('.').revision.number

                    # logs  = client.log(
                        # "http://svn.promotux.it/svn/promogest2/trunk/",
                        # revision_start=pysvn.Revision( pysvn.opt_revision_kind.number, rev_locale),
                        # revision_end=pysvn.Revision( pysvn.opt_revision_kind.number, self._rev_remota),
                        # strict_node_history=True,
                        # limit=0,
                        # include_merged_revisions=False,
                        # )

                    # for commit in logs:
                        # if 'DBWARN' in commit.message:
                            # critico = True

                    # if critico:
                        # messageWarning("Attenzione: E' necessario chiudere PromoGest su tutte le postazioni collegate prima di premere Aggiorna.\n\nNel caso non sia possibile consigliamo di rinviare l'aggiornamento.")
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

        t = threading.Thread(group=None, target=fetchThread,
                        name='Data rendering thread', args=([self]),
                        kwargs={})
        t.start()


    def sync(self):

        def updateThread(data):
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
                data.msg_label.set_text("Aggiornamento eseguito con successo, riavviare PromoGest.")
                data.cancel_button.set_sensitive(True)
                import sys
                sys.exit(0)

        def refreshUI():
            if self.__stop:
                return False
            else:
                self.update_progress_bar.pulse()
                return True
        gobject.timeout_add(100, refreshUI)

        t = threading.Thread(group=None, target=updateThread,
                        name='Data rendering thread', args=([self]),
                        kwargs={})
        t.start()


    def show(self):
        self.update_progress_dialog.set_transient_for(self._parent.getTopLevel())
        self.update_progress_dialog.show()
        self.aggiornaLabel()

    def on_update_button_clicked(self, widget):
        self.sync()

    def on_cancel_button_clicked(self, widget):
        self.update_progress_dialog.destroy()
