# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>
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

from SimpleGladeWrapper import SimpleGladeWrapper

import gtk
import gobject
import gtkhtml2
import xml.etree.cElementTree as ElementTree

from promogest import Environment
from widgets.UnsignedDecimalEntryField import UnsignedDecimalEntryField
from widgets.SignedDecimalEntryField import SignedDecimalEntryField
from widgets.UnsignedIntegerEntryField import UnsignedIntegerEntryField
from widgets.SignedIntegerEntryField import SignedIntegerEntryField
from widgets.DateEntryField import DateEntryField
from widgets.DateTimeEntryField import DateTimeEntryField
from widgets.DateWidget import DateWidget
from widgets.DateTimeWidget import DateTimeWidget
from widgets.CustomComboBoxModify import CustomComboBoxModify
from widgets.CustomComboBoxSearch import CustomComboBoxSearch
from widgets.ScontiWidget import ScontiWidget
from widgets.ScontoWidget import ScontoWidget



from promogest.lib.HtmlTextView import HtmlTextView
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

    # Custom widget building methods (used by Glade)
    def createUnsignedDecimalEntryField(self, str1, str2, int1, int2):
        """ Return an EntryField for no sign decimal numbers input """
        return UnsignedDecimalEntryField(str1, str2, int1, int2)


    def createUnsignedIntegerEntryField(self, str1, str2, int1, int2):
        """ Return an EntryField for no sign integer numbers input """
        return UnsignedIntegerEntryField(str1, str2, int1, int2)


    def createSignedDecimalEntryField(self, str1, str2, int1, int2):
        """ Return an EntryField for signed decimal numbers input """
        return SignedDecimalEntryField(str1, str2, int1, int2)


    def createSignedIntegerEntryField(self, str1, str2, int1, int2):
        """ Return an EntryField for signed integer numbers input """
        return SignedIntegerEntryField(str1, str2, int1, int2)


    def createUnsignedMoneyEntryField(self, str1, str2, int1, int2):
        """ Return an EntryField for no sign money values input """
        return UnsignedDecimalEntryField(str1, str2, int1, Environment.conf.decimals)


    def createSignedMoneyEntryField(self, str1, str2, int1, int2):
        """ Return an EntryField for signed money values input """
        return SignedDecimalEntryField(str1, str2, int1, Environment.conf.decimals)


    def createDateEntryField(self, str1, str2, int1, int2):
        """ Return an EntryField for date input """
        return DateEntryField(str1, str2, int1, int2)


    def createDateTimeEntryField(self, str1, str2, int1, int2):
        """ Return an EntryField for date-time input """
        return DateTimeEntryField(str1, str2, int1, int2)


    def createCustomComboBoxModify(self, str1, str2, int1, int2):
        """ Return a lookup ComboBox with changes possibility """
        return CustomComboBoxModify()


    def createCustomComboBoxSearch(self, str1, str2, int1, int2):
        """ Return a ComboBox with search & history possibility """
        return CustomComboBoxSearch()


    def createScontiWidget(self, str1, str2, int1, int2):
        """ Return a ScontiWidget widget """
        return ScontiWidget(str1, str2)


    def createScontoWidget(self, str1, str2, int1, int2):
        """ Return an EntryField for discount input with selection of the discount type"""
        return ScontoWidget(str1, str2, int1, int2)


    def createGtkHtml2Widget(self, str1, str2, int1, int2):
        """ Return a GtkHtml2 widget """
        return gtkhtml2.View()

    def createHtmlWidget(self, str1, str2, int1, int2):
        """ Return a HtmlTextView widget """
        return HtmlTextView()

    def createDateWidget(self, str1, str2, int1, int2):
        """ Return a DateWidget widget """
        return DateWidget(str1, str2, int1, int2)


    def createDateTimeWidget(self, str1, str2, int1, int2):
        """ Return a DateTimeWidget widget """
        return DateTimeWidget(str1, str2, int1, int2)


    def createArticoloSearchWidget(self, str1, str2, int1, int2):
        """ Return an ArticoloSearchWidget widget """
        from widgets.ArticoloSearchWidget import ArticoloSearchWidget

        return ArticoloSearchWidget()


    def createClienteSearchWidget(self, str1, str2, int1, int2):
        """ Return an ClienteSearchWidget widget """
        from widgets.ClienteSearchWidget import ClienteSearchWidget
        widget = ClienteSearchWidget()
        #print widget.__class__
        return widget


    def createFornitoreSearchWidget(self, str1, str2, int1, int2):
        """ Return an FornitoreSearchWidget widget """
        from widgets.FornitoreSearchWidget import FornitoreSearchWidget
        return FornitoreSearchWidget()


    def createPersonaGiuridicaSearchWidget(self, str1, str2, int1, int2):
        """ Return an PersonaGiuridicaSearchWidget widget """
        from widgets.PersonaGiuridicaSearchWidget import PersonaGiuridicaSearchWidget
        return PersonaGiuridicaSearchWidget()

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

        file = open(self._defaultWindowAttributesFile, "rw")
        doc = ElementTree.parse(file)
        file.close()
        elem = doc.getroot()
        if  elem.findall(self._windowName):
            obj = elem.find(self._windowName)
            self.width = int(obj.get('width'))
            self.height = int(obj.get('height'))
            self.left = int(obj.get('left'))
            self.top = int(obj.get('top'))
        else:
            #print "Dimensioni %s impostati sui valori di default" % self._windowName
            pass

    def _saveWindowAttributes(self):
        """
        solo un po' di refactoring, SAX2 non è tra i parser XML  di default
        ho portato tutto ad ElementTree e semplificato l'albero xml
        """

        (self.width, self.height) = self.topLevelWindow.get_size()
        (self.left, self.top) = self.topLevelWindow.get_position()

        file = open(self._defaultWindowAttributesFile, "rw")
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
        #print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
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


    def on_top_level_closed(self):
        """ Saving window's parameters """

        if self.isWindowPlaced:
            self._saveWindowAttributes()


    def destroy(self):
        """ Destroying window """

        self.on_top_level_closed()
        self.topLevelWindow.destroy()


    def hide(self):
        """ Hiding window """

        self.on_top_level_closed()
        self.topLevelWindow.hide()
