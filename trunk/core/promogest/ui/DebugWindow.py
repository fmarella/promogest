# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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
from promogest.lib.utils import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget


class DebugWindow(GladeWidget):

    def __init__(self, parent):
        '''
        Constructor
        '''
        GladeWidget.__init__(self, root='debug_window',
            path='_debug_window.glade')
        self.__parent = parent
        self.placeWindow(self.getTopLevel())
        self.draw()

    def draw(self):
        msg = "DAO={0} FILTER={1} ALL={2}".format(Environment.debugDao,
            Environment.debugFilter, Environment.params['engine'].echo)
        textview_set_text(self.textview1, msg)

    def on_entry1_key_press_event(self, widget, event):
        buf = textview_get_text(self.textview1)
        if event.type == gtk.gdk.KEY_PRESS:
            if gdk_keyval_name(event.keyval) == 'Return':
                cmd = self.entry1.get_text()
                self.entry1.set_text('')
                if cmd == 'god':
                    Environment.params['engine'].echo = not Environment.params['engine'].echo
                    buf += "\nALL={0}".format(Environment.params['engine'].echo)
                elif cmd == 'dao':
                    Environment.debugDao = not Environment.debugDao
                    buf += "\nDAO={0}".format(Environment.debugDao)
                elif cmd == 'filter':
                    Environment.debugFilter = not Environment.debugFilter
                    buf += "\nFILTER={0}".format(Environment.debugFilter)
                textview_set_text(self.textview1, buf)
            elif gdk_keyval_name(event.keyval) == 'Escape':
                self.debug_window.hide()