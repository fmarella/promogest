# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni  <francesco@promotux.it>
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

from promogest.ui.gtk_compat import *
from CustomEntryField import CustomEntryField
from promogest import Environment
from promogest.ui.utils import mN, setconf


class UnsignedDecimalEntryField(CustomEntryField):
# Effettua la validazione per decimali senza segno
    __gtype_name__ = 'UnsignedDecimalEntryField'
    def __init__(self, str1=None, str2=None, int1=None, int2=None):
        CustomEntryField.__init__(self)

        self._lunghezza = 10
        #self._precisione = int2
        #if self._precisione =="0":
        self._precisione = int(setconf(key="decimals", section="Numbers"))
        self._default = str1
        self.acceptedKeys = self.controlKeys + self.numberKeys + self.delimiterKeys


    def my_key_press_event(self, widget, event):
        keyname = gdk_keyval_name(event.keyval)
        if keyname not in self.acceptedKeys:
            return True
        s = widget.get_text()
        # verifica che non sia gia' stato inserito un separatore decimale
        if (',' in s or '.' in s) and (keyname in self.delimiterKeys):
            return True

    def my_focus_out_event(self, widget, event):
        s = widget.get_text()
        r = s.replace(",",".")
        widget.set_text("")
        widget.set_text(r)
        try:
            f = "%-" + str(self._lunghezza) + "." + str(self._precisione) + "f"
            if self.get_text():
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