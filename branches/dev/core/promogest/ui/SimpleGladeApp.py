# -*- coding: utf-8 -*-

"""
 SimpleGladeApp.py
 Module that provides an object oriented abstraction to pygtk and libglade.
 Copyright (C) 2004 Sandino Flores Moreno
"""

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import os
import sys
import re

import tokenize
import gtk
import gtk.glade
import weakref
import inspect
from promogest import Environment
from SimpleGladeWrapper import SimpleGladeWrapper

__version__ = "1.0"
__author__ = 'Sandino "tigrux" Flores-Moreno'

class SimpleGladeApp(SimpleGladeWrapper):

    def __init__(self, path, root=None, domain=None, **kwargs):
        """
        Load a glade file specified by glade_filename, using root as
        root widget and domain as the domain for translations.

        If it receives extra named arguments (argname=value), then they are used
        as attributes of the instance.

        path:
            path to a glade filename.
            If glade_filename cannot be found, then it will be searched in the
            same directory of the program (sys.argv[0])

        root:
            the name of the widget that is the root of the user interface,
            usually a window or dialog (a top level widget).
            If None or ommited, the full user interface is loaded.

        domain:
            A domain to use for loading translations.
            If None or ommited, no translation is loaded.

        **kwargs:
            a dictionary representing the named extra arguments.
            It is useful to set attributes of new instances, for example:
                glade_app = SimpleGladeApp("ui.glade", foo="some value", bar="another value")
            sets two attributes (foo and bar) to glade_app.
        """
        SimpleGladeWrapper.__init__(self, path, root, domain)




    def main(self):
        """
        Starts the main loop of processing events.
        The default implementation calls gtk.main()

        Useful for applications that needs a non gtk main loop.
        For example, applications based on gstreamer needs to override
        this method with gst.main()

        Do not directly call this method in your programs.
        Use the method run() instead.
        """
        gtk.gdk.threads_init()

        gtk.gdk.threads_enter()

        gtk.main()
        gtk.gdk.threads_leave()

    def on_focus_in_event(self, widget, event):
        try:
            color_base = Environment.conf.Documenti.color_base
        except:
            #print "DEFINIRE NELLA SEZIONE DOCUMENTI UN COLORE PER LE ENTRY CON color_base = #FLFLFLF"
            color_base = "#F9FBA7"
        try:
            color_text = Environment.conf.Documenti.color_text
        except:
            #print "DEFINIRE NELLA SEZIONE DOCUMENTI UN COLORE PER LE ENTRY CON color_text = #FFFFFF"
            color_text = "black"
        widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(color_base))
        widget.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse(color_text))

    def on_focus_out_event(self, widget, event):
        #widget.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
        #widget.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
        widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        widget.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))

    def insert_text_decimal(self,editable, new_text, new_text_length, position):
        stringg = editable.get_text()
        if (new_text != "." or "." in stringg.strip()) and not (new_text.replace(".","").isdigit()):
            editable.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
            editable.emit_stop_by_name("insert_text")
        else:
            editable.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#F9FBA7"))

    def on_entry_focus_in_event(self, widget, event):
        try:
            color_base = Environment.conf.Documenti.color_base
        except:
            #print "DEFINIRE NELLA SEZIONE DOCUMENTI UN COLORE PER LE ENTRY CON color_base = #FLFLFLF"
            color_base = "#F9FBA7"
        try:
            color_text = Environment.conf.Documenti.color_text
        except:
            #print "DEFINIRE NELLA SEZIONE DOCUMENTI UN COLORE PER LE ENTRY CON color_text = #FFFFFF"
            color_text = "black"
        widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(color_base))
        widget.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse(color_text))

    def on_entry_focus_out_event(self, widget, event):
        #widget.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
        #widget.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
        widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        widget.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))

    def run(self):
        """
        Starts the main loop of processing events checking for Control-C.

        The default implementation checks wheter a Control-C is pressed,
        then calls on_keyboard_interrupt().

        Use this method for starting programs.
        """
        try:
            self.main()
        except KeyboardInterrupt:
            Environment.pg2log.info("<<<<<<<<<<  CHIUSURA PROMOGEST >>>>>>>>>>>>>")
            self.on_keyboard_interrupt()
