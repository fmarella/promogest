# -*- coding: utf-8 -*-

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
#        else:
#            lunghezza = 10
#        self.set_max_length(lunghezza)
        return lunghezza


    def my_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname not in self.acceptedKeys:
            return True


    def my_focus_out_event(self, widget, event):
        """ TODO: comportamento anomalo ...da verificare per il momento
        resta disattivata"""
        return
#        lunghezza = self.proprieta()
#        try:
#            i = int(self.get_text())
#            if lunghezza > 0:
#                f = "%0" + str(lunghezza) + "d"
#                self.set_text(f % i)
#            else:
#                self.set_text(str(self.get_text()))
#        except Exception:
#            self.set_text('')
