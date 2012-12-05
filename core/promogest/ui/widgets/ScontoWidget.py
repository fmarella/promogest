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
from SignedDecimalEntryField import SignedDecimalEntryField


class ScontoWidget(gtk.HBox):
# entryfield numerica con segno con possibilita' di scelta del tipo di sconto
    __gtype_name__ = 'ScontoWidget'
    discountTypeChars = ('p', 'P', 'v', 'V')

    def __init__(self, str1=None, str2=None, int1=None, int2=None):
        gtk.HBox.__init__(self)
        self.entry = SignedDecimalEntryField(str1, str2, int1, int2)
        self.entry.connect("key_press_event", self.do_key_press_event)
        self.entry.connect("focus_out_event", self.do_focus_out_event)
        self.buttonPerc = gtk.RadioButton(label='%')
        self.buttonPerc.connect('clicked', self._setFocus)
        self.buttonPerc.set_mode(False)
        self.buttonPerc.set_size_request(20, -1)
        self.buttonPerc.set_property('can-focus', False)
        self.buttonVal = gtk.RadioButton(group=self.buttonPerc, label='E')
        self.buttonVal.connect('clicked', self._setFocus)
        self.buttonVal.set_mode(False)
        self.buttonVal.set_size_request(20, -1)
        self.buttonVal.set_property('can-focus', False)
        self.pack_start(self.entry, True, True, 0)
        self.pack_start(self.buttonPerc, False, False, 0)
        self.pack_start(self.buttonVal, False, False, 0)
        self.connect("show", self.on_show)

        self.buttonPerc.set_active(True)
        self.entry.acceptedKeys += self.discountTypeChars


    def do_key_press_event(self, widget, event):
        keyname = gdk_keyval_name(event.keyval)
#        print "AHAHAAHAHAHAHAAHAH", keyname
        if keyname not in self.entry.acceptedKeys:
            return True
        if keyname == 'p' or keyname == 'P':
            self.tipoSconto = 'percentuale'
            return True
        elif keyname == 'v' or keyname == 'V':
            self.tipoSconto = 'valore'
            return True

#    def do_focus_out_event(self, widget, entry):
#        self.emit('focus_out_event', widget, entry)

    def _getTipoSconto(self):
        if self.buttonPerc.get_active():
            return 'percentuale'
        elif self.buttonVal.get_active():
            return 'valore'
        else:
            return ''

    def _setTipoSconto(self, value):
        if value == 'valore':
            self.buttonVal.set_active(True)
        else:
            self.buttonPerc.set_active(True)

    tipoSconto = property(_getTipoSconto, _setTipoSconto)


    def set_text(self, value):
        self.entry.set_text(value)


    def get_text(self):
        return self.entry.get_text()


    def getTipoScontoString(self):
        if self.tipoSconto == 'valore':
            return '€'
        else:
            return '%'

    def _setFocus(self, button):
        self.entry.grab_focus()

    def on_show(self, event):
        (width, heigth) = self.get_size_request()
        if width == -1:
            self.setSize()


    def setSize(self, size=None):
        if size is None:
            size = -1
            parent = self.get_parent()
            if parent is not None:
                if parent.__class__ is gtk.Alignment:
                    (width, heigth) = parent.get_size_request()
                    size = width

        self.set_size_request(size, -1)


#gobject.type_register(ScontoWidget)
