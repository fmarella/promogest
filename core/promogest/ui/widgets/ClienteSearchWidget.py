# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>

import gtk
import gobject

from CustomComboBoxSearch import CustomComboBoxSearch

from promogest import Environment
from promogest.ui.utils import *

class ClienteSearchWidget(CustomComboBoxSearch):
    """ Classe base per la ricerca clienti """

    def __init__(self):
        CustomComboBoxSearch.__init__(self)

        idHandler = self.connect('changed',
                                 self.on_combobox_cliente_search_clicked)
        self.setChangedHandler(idHandler)

        self.connect("destroy-event", self.on_widget_destroy)

        self._callName = None
        self._ricerca = None
        self._filter = True
        self._resultsCount = 0
        self.clear()


    def on_combobox_cliente_search_clicked(self, combobox):
        #richiama la ricerca dei clienti

        def refresh_combobox_cliente(anagWindow):
            self._resultsCount = self._ricerca.getResultsCount()
            resultsElement = self._ricerca.getResultsElement()
            if not(self._resultsCount > 0):
                self.set_active(0)
                return

            if self._resultsCount == 1:
                id = resultsElement.id
                res = leggiCliente(id)
                denominazione = res["ragioneSociale"]
                if denominazione == '':
                    denominazione = res["nome"] + ' ' + res["cognome"]
                combobox.refresh(id, denominazione, res)
            else:
                self.idlist = []
                for ids in resultsElement:
                    self.idlist.append(ids.id)
                combobox.refresh(self.idlist, ('< %d clienti selezionati... >' % self._resultsCount), None, rowType='old_search')
            if self._callName is not None:
                self._callName()

        if combobox.on_selection_changed():
            if self._ricerca is None:
                from promogest.ui.RicercaComplessaClienti import RicercaComplessaClienti
                self._ricerca = RicercaComplessaClienti()
                if not self._filter:
                    self._ricerca.setTreeViewSelectionType(gtk.SELECTION_SINGLE)
            else:
                self._ricerca.refresh()
            anagWindow = self._ricerca.getTopLevel()
            returnWindow = combobox.get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.connect("hide",
                               refresh_combobox_cliente)
            self._ricerca.show_all()

        elif self._callName is not None:
            self._callName()


    def setId(self, value):
        self.insertComboboxSearchCliente(self, value)


    def getId(self):
        if self.isEmpty():
            self.clear()
        elif (self._resultsCount > 1) and (self._ricerca is not None):
            self._ricerca.refresh()
            return self.idlist
        return self._id


    def getData(self):
        return self._container


    def insertComboboxSearchCliente(self, combobox, idCliente, clear=False, filter=True):
        res = leggiCliente(idCliente)
        denominazione = res["ragioneSociale"]
        if denominazione == '':
            denominazione = res["nome"] + ' ' + res["cognome"]
        combobox.refresh(idCliente, denominazione, res, clear, filter)


    def clear(self):
        self.set_active(0)


    def setOnChangedCall(self, callName=None):
        self._callName = callName


    def setSingleValue(self):
        self._filter = False


    def setMultipleValues(self):
        self._filter = True


    def on_widget_destroy(self, widget, event):
        if self._ricerca is not None:
            anagWindow = self._ricerca.getTopLevel()
            anagWindow.destroy()
            del self._ricerca
            self._ricerca = None
