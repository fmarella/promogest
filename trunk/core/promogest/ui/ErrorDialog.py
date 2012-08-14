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

from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.SendEmail import SendEmail

class ErrorDialog(GladeWidget):
    """ Dialog for showing a fatal error message """
    def __init__(self, message):
        self.message = message
        GladeWidget.__init__(self, root='error_dialog',
                                path="error_dialog.glade")
        self.error_dialog_label.set_text(message)

    def on_email_send_clicked(self,button):
        sendemail = SendEmail(string = self.message, d=True)
        self.getTopLevel().destroy()

    def on_ok_button_clicked(self, button):
        self.getTopLevel().destroy()
