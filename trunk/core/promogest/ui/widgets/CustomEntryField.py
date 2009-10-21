# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>


import gtk

class CustomEntryField(gtk.Entry):

    controlKeys = ('Delete','KP_Delete','BackSpace','Tab','ISO_Left_Tab',
                   'Left','Right','Down','Up',
                   'KP_Left','KP_Right','KP_Down','KP_Up',
                   'Home','End','KP_Home','KP_End', 'Return', 'KP_Enter')
    delimiterKeys = ('comma', 'period', 'KP_Decimal')
    signKeys = ('minus','KP_Subtract','plus','KP_Add')
    numberKeys = ('0','1','2','3','4','5','6','7','8','9',
                  'KP_0','KP_1','KP_2','KP_3','KP_4','KP_5','KP_6','KP_7','KP_8','KP_9')
    dateKeys = ('slash', 'KP_Divide')
    dateTimeKeys = ('slash', 'KP_Divide', 'colon', 'space')
    dateChars = ('/', '-')
    dateTimeChars = ('/', '-', ':', ' ')

    def __init__(self):
        gtk.Entry.__init__(self)
        self.connect('key_press_event', self.my_key_press_event)
        self.connect('focus_out_event', self.my_focus_out_event)
        self.connect('paste_clipboard', self.my_paste_clipboard)
        self.connect('focus-in-event', self.on_focus_in_event)
        self.connect('focus-out-event', self.on_focus_out_event)
        self.connect("icon-press", self.on_icon_press)
        self.set_property("secondary_icon_stock", "gtk-clear")
        self.set_property("secondary_icon_activatable", True)
        self.set_property("secondary_icon_sensitive", True)
        self.connect("show", self.on_show)


    def on_icon_press(self, widget):
        pass

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

    def my_key_press_event(self, widget, event):
        pass


    def my_focus_out_event(self, widget, event):
        pass


    def my_paste_clipboard(self, widget):
        self.emit_stop_by_name('paste_clipboard')


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


#gobject.type_register(CustomEntryField)
