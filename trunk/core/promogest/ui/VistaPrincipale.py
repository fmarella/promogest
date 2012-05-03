# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

import webbrowser
from GladeWidget import GladeWidget
from utils import *
from promogest.ui.SendEmail import SendEmail


class VistaPrincipale(GladeWidget):
    """
    Frame Principale di visualizzazione principale da
    costruire all'uscita di ogni anagrafica
    alla chiamata del metodo _refresh() con update dei promemoria in scadenza.
    """

    def __init__(self, mainWindow, azs=None):
#        GladeWidget.__init__(self, 'vista_principale_frame',
#        fileName='_main_window_view_select.glade')
        self._loading = None
#        self.getfeedFromSite()

    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura del frame """
        self.vista_principale_frame.show_all()

    def on_alarm_notify_treeview_cursor_changed(self, treeview):
        if self._loading:
            return
        self.cancel_alarm_button.set_sensitive(True)

    def on_promotux_button_clicked(self, button):
        url = "http://www.promotux.it"
        webbrowser.open_new_tab(url)

    def on_promogest_button_clicked(self, button):
        url = "http://www.promogest.me"
        webbrowser.open_new_tab(url)

    def on_numero_verde_button_clicked(self, button):
        SendEmail()
