# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
#    Author: Francesco Meloni  <francesco@promotux.it>

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
#from promogest.ui.utils import

class CustomComboBoxSearch(gtk.ComboBox):
    __gtype_name__ = 'CustomComboBoxSearch'

    def __init__(self):
        self._id = None
        self._container = None
        self.__rebuildList = False
        self._idChangedHandler = None

        gtk.ComboBox.__init__(self)
        renderer = gtk.CellRendererText()
        self.pack_start(renderer, True)
        self.add_attribute(renderer, 'text', 2)
        self.set_property("can-focus", True)
        self.connect("show", self.on_show)
        self.draw()


    def on_selection_changed(self):
        if self.__rebuildList:
            return False

        model = self.get_model()
        rowIndex = self.get_active()
        if rowIndex == -1:
            self._id = None
            self._container = None
            self.clear()
        elif model[rowIndex][0] == 'new_search' or model[rowIndex][0] =='old_search':
            return True
        elif model[rowIndex][0] == 'empty':
            self._id = None
            self._container = None
            self.clear()
        else:
            self._id = model[rowIndex][1]
            self._container = model[rowIndex][3]
        return False


    def refresh(self, id=None, denominazione=None, container=None, clear=False, filter=True, idType=None, rowType='element'):
        if self._idChangedHandler is not None:
            self.handler_block(self._idChangedHandler)
        if clear:
            self.draw(filter, idType)
        self.__rebuildList = True
        model = self.get_model()

        if rowType == 'old_search':
            for r in model:
                if r[0] == rowType:
                    model.remove(r.iter)
            id = 0
            self._id = None
            self._container = container
            model.insert(1, (rowType, id, denominazione[0:40], container))
            self.set_active(1)
        elif id is not None and container is not None:
            for r in model:
                if r[1] == id:
                    model.remove(r.iter)
            self._id = id
            self._container = container
            model.insert(1, (rowType, id, denominazione[0:20], container))
            self.set_active(1)
            if len(model) > 12:
                model.remove(model[11].iter)
        else:
            self._id = id
            self._container = container
        if self._idChangedHandler is not None:
            self.handler_unblock(self._idChangedHandler)
        self.__rebuildList = False


    def draw(self, filter=True, idType=None):
        self.__rebuildList = True
        if idType == 'str':
            model = gtk.ListStore(str, str, str, object)
        else:
            model = gtk.ListStore(str, int, str, object)
        self.set_model(model)
        model.clear()
        if filter:
            model.append(('empty', 0, '< Tutti >', None))
        else:
            model.append(('empty', 0, '', None))
        self.set_active(0)
        model.append(('new_search', 0, '< Altro... >', None))
        self.__rebuildList = False


    def getContainer(self):
        return self._container


    def setChangedHandler(self, idHandler):
        self._idChangedHandler = idHandler
        self.refresh()


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


    def clear(self):
        pass


    def isEmpty(self):
        model = self.get_model()
        rowIndex = self.get_active()
        return ((rowIndex == -1) or (model[rowIndex][0] == 'empty'))

gobject.type_register(CustomComboBoxSearch)
