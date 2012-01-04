# -*- coding: iso-8859-15 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Alceste Scalas <alceste@promotux.it>
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

from promogest import Environment
from promogest.ui.gtk_compat import *
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.SendEmail import SendEmail

class FatalErrorDialog(GladeWidget):
    """ Dialog for showing a fatal error message """
    def __init__(self, message):
        self.message = message

        msg ="""ATTENZIONE !!
Si è verificato un errore non recuperabile
e l'applicazione verrà chiusa, si prega di contattare
l'assistenza o di inviare il traceback usando la finestra
di email dopo aver configurato i parametri smtp nel file
"configure" o tramite interfaccia dal menu opzioni

Grazie"""
        GladeWidget.__init__(self, 'fatal_error_dialog.glade')
        self.fatal_error_dialog_label.set_text(msg)

    def on_email_send_clicked(self,button):
        premessa = """ Attenzione si è verificato un errore
non recuperabile, questo comporta la chiusura dell'applicazione
Clicca su invia tramite email.
Grazie.

"""
        messaggio = premessa +self.message
        sendemail = SendEmail(string = messaggio, d=True)

    def on_ok_button_clicked(self, button):
        gtk.main_quit()
