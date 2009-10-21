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
import gobject
from promogest import Environment

class CustomComboBoxModify(gtk.HBox):
    __gtype_name__ = 'CustomComboBoxModify'
    __gsignals__ = {'clicked' : (gobject.SIGNAL_RUN_LAST,
                                 gobject.TYPE_OBJECT,
                                 (gobject.TYPE_OBJECT, ) )}

    def __init__(self):
        gtk.HBox.__init__(self, False, 0)
        self.combobox = gtk.ComboBox()
        self.combobox.set_property("can-focus", True)
        self.button = gtk.ToggleButton()
        self.button.set_property("can-focus", True)
        image = gtk.Image()
        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'modifica16x16.png')
        image.set_from_pixbuf(pbuf)
        self.button.add(image)
        self.pack_start(self.combobox, True, True, 0)
        self.pack_start(self.button, False, False, 0)
        self.set_property("can-focus", True)
        self.button.connect('clicked',
                            self.do_button_clicked)
        self.combobox.connect('key_press_event',
                              self.do_combobox_key_press_event)
        if hasattr(Environment.conf,'Numbers'):
            self.combo_column = int(getattr(Environment.conf.Numbers,'combo_column',5))
            if self.combo_column:
                self.combobox.set_wrap_width(self.combo_column)
        renderer = gtk.CellRendererText()
        self.combobox.pack_start(renderer, True)
        self.combobox.add_attribute(renderer, 'text', 0)
        self.connect("show", self.on_show)


    def do_button_clicked(self, button):
        self.emit('clicked', button)


    def do_combobox_key_press_event(self, combobox, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
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
