# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>
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
from GladeWidget import GladeWidget
from promogest.ui.SendEmail import SendEmail

class FatalErrorDialog(GladeWidget):
    """ Dialog for showing a fatal error message """
    def __init__(self, message):
        self.message = message
        #if "duplicate key value violates unique constraint" or "una chiave duplicata viola il vincolo" in self.message:
            #msg="""Il Valore inserito è già presente nel database!"""
            #dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               #gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            #dialog.run()
            #dialog.destroy()
            #return
        #else:
        msg ="""ATTENZIONE !!
Si è verificato un errore non recuperabile
e l'applicazione verrà chiusa, si prega di contattare
l'assistenza o di inviare il traceback usando la finestra
di email dopo aver configurato i parametri smtp nel file
"configure" o tramite interfaccia dal menu opzioni

Grazie"""
        GladeWidget.__init__(self, 'fatal_error_dialog')
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