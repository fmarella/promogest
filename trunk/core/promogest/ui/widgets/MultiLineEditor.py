# -*- coding: iso-8859-15 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.gtk_compat import *


class MultiLineEditor(GladeWidget):

    def __init__(self, desc=None):
        self.string = desc
        window = gtk.Window(GTK_WINDOWTYPE_TOPLEVEL)
        self.window = window
        window.set_resizable(True)
        window.connect("destroy", self.close_application)
        window.set_title("Multi Line Editor")
        window.set_border_width(0)

        box1 = gtk.VBox()
        box1.set_homogeneous(False)
        box1.set_spacing(0)
        window.add(box1)
        box1.show()

        box2 = gtk.VBox()
        box2.set_homogeneous(False)
        box2.set_spacing(10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()

        sw = gtk.ScrolledWindow()
        sw.set_policy(GTK_POLICYTYPE_AUTOMATIC, GTK_POLICYTYPE_AUTOMATIC)
        self.textview = gtk.TextView()
        self.textview.set_justification(GTK_JUSTIFICATION_LEFT)
        textbuffer = self.textview.get_buffer()
        sw.add(self.textview)
        sw.show()
        self.textview.show()
        box2.pack_start(sw, True, True, 0)
        textbuffer.set_text(self.string)

        hbox = gtk.HButtonBox()
        box2.pack_start(hbox, False, False, 0)
        hbox.show()

        vbox = gtk.VBox()
        vbox.show()
        hbox.pack_start(vbox, False, False, 0)
        # check button to toggle editable mode
        check = gtk.CheckButton("Editable")
        vbox.pack_start(check, False, False, 0)
        check.connect("toggled", self.toggle_editable, self.textview)
        check.set_active(True)
        check.show()
        # check button to toggle cursor visiblity
        check = gtk.CheckButton("Cursor Visible")
        vbox.pack_start(check, False, False, 0)
        check.connect("toggled", self.toggle_cursor_visible, self.textview)
        check.set_active(True)
        check.show()
        vbox = gtk.VBox()
        vbox.show()
        hbox.pack_start(vbox, False, False, 0)
        radio = gtk.RadioButton(None, "WRAP__WORD")
        vbox.pack_start(radio, False, True, 0)
        radio.connect("toggled", self.new_wrap_mode, self.textview, GTK_WRAPMODE_WORD)
        radio.show()
        separator = gtk.HSeparator()
        box1.pack_start(separator, False, True, 0)
        separator.show()

        box2 = gtk.VBox()
        box2.set_homogeneous(False)
        box2.set_spacing(10)
        box2.set_border_width(10)
        box1.pack_start(box2, False, True, 0)
        box2.show()

        button = gtk.Button("OK")
        button.connect("clicked", self.close_application)
        box2.pack_start(button, True, True, 0)
        button.set_can_default(True)
        button.grab_default()
        button.show()
        #window.placeWindow(window)
        window.set_modal(modal=True)
        #window.set_transient_for(self.getTopLevel())
        window.show_all()

    def toggle_editable(self, checkbutton, textview):
        textview.set_editable(checkbutton.get_active())

    def toggle_cursor_visible(self, checkbutton, textview):
        textview.set_cursor_visible(checkbutton.get_active())

    def toggle_left_margin(self, checkbutton, textview):
        if checkbutton.get_active():
            textview.set_left_margin(50)
        else:
            textview.set_left_margin(0)

    def toggle_right_margin(self, checkbutton, textview):
        if checkbutton.get_active():
            textview.set_right_margin(50)
        else:
            textview.set_right_margin(0)

    def new_wrap_mode(self, radiobutton, textview, val):
        if radiobutton.get_active():
            textview.set_wrap_mode(val)

    def new_justification(self, radiobutton, textview, val):
        if radiobutton.get_active():
            textview.set_justification(val)

    def close_application(self, widget):
        textBuffer = self.textview.get_buffer()
        Environment.mltext = textBuffer.get_text(textBuffer.get_start_iter(),
                                            textBuffer.get_end_iter(),True)
        self.window.destroy()

