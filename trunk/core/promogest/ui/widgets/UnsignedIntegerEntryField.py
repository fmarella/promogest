# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni  <francesco@promotux.it>
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

from promogest.ui.gtk_compat import *
from CustomEntryField import CustomEntryField


class UnsignedIntegerEntryField(CustomEntryField):
# Effettua la validazione per interi senza segno o virgole
    __gtype_name__ = 'UnsignedIntegerEntryField'
    def __init__(self, str1=None, str2=None, int1=None, int2=None):
        CustomEntryField.__init__(self)
        self._lunghezza = None
        self._default = str1
        if self._lunghezza > 0:
            self.set_max_length(self._lunghezza)
        self.acceptedKeys = self.controlKeys + self.numberKeys

    def proprieta(self):
        lunghezza = 10
        if "partita_iva" in self.nomee:
            lunghezza = 11
        elif "cap" in self.nomee:
            lunghezza = 5
        return lunghezza


    def my_key_press_event(self, widget, event):
        keyname = gdk_keyval_name(event.keyval)
        if keyname not in self.acceptedKeys:
            return True


    def my_focus_out_event(self, widget, event):
        """ TODO: comportamento anomalo ...da verificare per il momento
        resta disattivata"""
        return

