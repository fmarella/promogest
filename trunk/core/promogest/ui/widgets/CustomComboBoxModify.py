# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
#    Author: Francesco Marella  <francesco.marella@gmail.com>
#
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
from promogest import Environment


class CustomComboBoxModify(gtk.HBox):
    __gtype_name__ = 'CustomComboBoxModify'
    __gsignals__ = {'clicked' : (GOBJECT_SIGNAL_RUNLAST,
                                 gobject.TYPE_OBJECT,
                                 (gobject.TYPE_OBJECT, ) )}

    def __init__(self):
        from promogest.ui.utils import setconf
        gtk.HBox.__init__(self)
        self.combobox = gtk.ComboBox()
        self.combobox.set_property("can-focus", True)
        self.button = gtk.ToggleButton()
        self.button.set_property("can-focus", True)
        image = gtk.Image()
        pbuf = GDK_PIXBUF_NEW_FROM_FILE(Environment.conf.guiDir + 'modifica16x16.png')
        image.set_from_pixbuf(pbuf)
        self.button.add(image)
        self.pack_start(self.combobox, True, True, 0)
        self.pack_start(self.button, False, False, 0)
        self.set_property("can-focus", True)
        self.button.connect('clicked',
                            self.do_button_clicked)
        self.combobox.connect('key_press_event',
                              self.do_combobox_key_press_event)

        self.combobox.set_wrap_width(int(setconf("Numbers", "combo_column")))
        renderer = gtk.CellRendererText()
        self.combobox.pack_start(renderer, True)
        self.combobox.add_attribute(renderer, 'text', 0)
        self.connect("show", self.on_show)


    def do_button_clicked(self, button):
        self.emit('clicked', button)


    def do_combobox_key_press_event(self, combobox, event):
        keyname = gdk_keyval_name(event.keyval)
        if keyname == 'Escape':
            combobox.set_active(-1)


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

        self.combobox.set_size_request(size, -1)


gobject.type_register(CustomComboBoxModify)
