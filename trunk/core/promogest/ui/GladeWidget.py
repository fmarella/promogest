# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2010 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>
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

from SimpleGladeWrapper import SimpleGladeWrapper
import os
import gtk
import gobject
import xml.etree.cElementTree as ElementTree

from promogest import Environment
from promogest.ui.widgets.UnsignedDecimalEntryField import UnsignedDecimalEntryField
from promogest.ui.widgets.SignedDecimalEntryField import SignedDecimalEntryField
from promogest.ui.widgets.UnsignedMoneyEntryField import UnsignedMoneyEntryField
from promogest.ui.widgets.SignedMoneyEntryField import SignedMoneyEntryField
from promogest.ui.widgets.UnsignedIntegerEntryField import UnsignedIntegerEntryField
from promogest.ui.widgets.SignedIntegerEntryField import SignedIntegerEntryField
from promogest.ui.widgets.DateEntryField import DateEntryField
from promogest.ui.widgets.DateTimeEntryField import DateTimeEntryField
from promogest.ui.widgets.DateWidget import DateWidget
from promogest.ui.widgets.DateTimeWidget import DateTimeWidget
from promogest.ui.widgets.CustomComboBoxModify import CustomComboBoxModify
from promogest.ui.widgets.CustomComboBoxSearch import CustomComboBoxSearch
from promogest.ui.widgets.ScontiWidget import ScontiWidget
from promogest.ui.widgets.ScontoWidget import ScontoWidget


#from promogest.lib.HtmlTextView import HtmlTextView
from SimpleGladeApp import SimpleGladeApp

class GladeWidget(SimpleGladeApp):
    """ Classe base per i widget creati utilizzando Glade 2 """

    def __init__(self, rootWidget, fileName=None, callbacks_proxy=None, isModule=False):
        if not isModule:
            glade_path = './gui/'+(fileName or '')
        else:
            glade_path = fileName
        SimpleGladeWrapper.__init__(self, path=glade_path, root=rootWidget,
                                    domain=None,
                                    callbacks_proxy=callbacks_proxy, isModule=isModule)
        self._prepareWindowPlacement()

    def on_generic_button_clicked(self, button):
        return False

    def _prepareWindowPlacement(self):
        """ Elements for the correct view of windows """

        self._defaultWindowAttributesFile = Environment.conf.windowsrc
        self._windowName = self.__class__.__name__
        self.isWindowPlaced = False
        self.topLevelWindow = None
        try:
            xmlFile = open(self._defaultWindowAttributesFile, 'r')
            xmlFile.close()
        except:
            root = ElementTree.Element("WINDOWS")
            tree = ElementTree.ElementTree(root)
            tree.write(self._defaultWindowAttributesFile)

    def _loadWindowAttributes(self):
        """ Imports size and position of the window """

        self.isWindowPlaced = True
        self.width = None
        self.height = None
        self.left = None
        self.top = None

        file = open(self._defaultWindowAttributesFile, "r")
        try:
            doc = ElementTree.parse(file)
            file.close()
            elem = doc.getroot()
            if  elem.findall(self._windowName):
                obj = elem.find(self._windowName)
                self.width = int(obj.get('width'))
                self.height = int(obj.get('height'))
                self.left = int(obj.get('left'))
                self.top = int(obj.get('top'))
        except:
            print "FILE XMLWINDOW errato da cancellare e ricreare"
            os.remove(self._defaultWindowAttributesFile)


    def _saveWindowAttributes(self):
        """
        solo un po' di refactoring, SAX2 non è tra i parser XML  di default
        ho portato tutto ad ElementTree e semplificato l'albero xml
        """

        (self.width, self.height) = self.topLevelWindow.get_size()
        (self.left, self.top) = self.topLevelWindow.get_position()

        file = open(self._defaultWindowAttributesFile, "r")
        doc = ElementTree.parse(file)
        file.close()
        elem = doc.getroot()
        if elem.findall(self._windowName):
            obj = elem.find(self._windowName)
        else:
            obj = ElementTree.SubElement(elem,self._windowName)
        obj.set("width", str(self.width) or "")
        obj.set("height", str(self.height) or "")
        obj.set("left", str(self.left) or "")
        obj.set("top", str(self.top) or "")
        doc.write(self._defaultWindowAttributesFile)


    def placeWindow(self, window):
        """ Positioning and sizing the window """
        if window is not None:
            self.topLevelWindow = window
            self._loadWindowAttributes()
            if self.width is not None and self.height is not None:
                self.topLevelWindow.resize(self.width, self.height)
            if self.left is not None and self.top is not None:
                self.topLevelWindow.move(self.left, self.top)

    def on_number_insert_text(self,editable, new_text, new_text_length, position):
        #print new_text, new_text_length, new_text.isdigit()
        pass


    def on_button_press_event(self, widget, event):
        #if event.button == 1:
            #print "left click"
        #elif event.button == 2:
            #print "middle click"
        #elif event.button == 3:
            #print "right click"

        # was it a multiple click?
        if event.type == gtk.gdk.BUTTON_PRESS:
            pass
            #print "single click"
        elif event.type == gtk.gdk._2BUTTON_PRESS:
            testo = widget.get_text()
            if testo.isupper():
                uppertext = testo.lower()
            else:
                uppertext = testo.upper()
            widget.set_text(uppertext)
            #print "double click"
        elif event.type == gtk.gdk._3BUTTON_PRESS:
            testo = widget.get_text()
            capitalizetext = testo.capitalize()
            widget.set_text(capitalizetext)
            #print "triple click. ouch, you hurt your user."


    def on_icon_press(self,entry,position,event):
        """
        scopettina agganciata ad un segnale generico
        """
        if position.value_nick == "primary":
            pass
            #print "CERCA"
        else:                            #secondary
            entry.set_text("")
            entry.grab_focus()

    def on_top_level_closed(self):
        """ Saving window's parameters """
        if self.isWindowPlaced:
            self._saveWindowAttributes()

    def destroy(self):
        """ Destroying window """
        self.on_top_level_closed()
        self.topLevelWindow.destroy()
        #Environment.pg2log.info("<<<<<<<<<<  CHIUSURA PROMOGEST >>>>>>>>>>>>>")

    def hide(self):
        """ Hiding window """
        self.on_top_level_closed()
        self.topLevelWindow.hide()
