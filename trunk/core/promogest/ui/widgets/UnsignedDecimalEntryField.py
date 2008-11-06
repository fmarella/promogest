# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
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
import gobject
import pygtk
import locale
from CustomEntryField import CustomEntryField

class UnsignedDecimalEntryField(CustomEntryField):
# Effettua la validazione per decimali senza segno

    def __init__(self, str1=None, str2=None, int1=None, int2=None):
        CustomEntryField.__init__(self)

        self._lunghezza = int1
        self._precisione = int2
        self._default = str1
        self.acceptedKeys = self.controlKeys + self.numberKeys + self.delimiterKeys


    def do_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname not in self.acceptedKeys:
            return True
        s = self.get_text()
        # verifica che non sia gia' stato inserito un separatore decimale
        if (',' in s or '.' in s) and (keyname in self.delimiterKeys):
            return True


    def do_focus_out_event(self, widget, event):
        try:
            f = "%-" + str(self._lunghezza) + "." + str(self._precisione) + "f"
            d = float(self.get_text())
            self.set_text(f % d)
        except Exception:
            if self._default is None:
                d = 0
                self.set_text(f % d)
            elif self._default == "<blank>":
                # empty
                self.set_text('')
            else:
                self.set_text(self._default)


#gobject.type_register(UnsignedDecimalEntryField)
