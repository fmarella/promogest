# -*- coding: iso-8859-15 -*-

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
        self.connect('key_press_event', self.do_key_press_event)
        self.connect('focus_out_event', self.do_focus_out_event)
        self.connect('paste_clipboard', self.do_paste_clipboard)
        self.connect("show", self.on_show)


    def do_key_press_event(self, widget, event):
        pass


    def do_focus_out_event(self, widget, event):
        pass


    def do_paste_clipboard(self, widget):
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
