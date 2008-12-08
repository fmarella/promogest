# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Enrico Pintus <enrico@promotux.it>

import gtk
from CustomComboBoxSearch import CustomComboBoxSearch
from promogest.ui.utils import leggiFornitore

class FornitoreSearchWidget(CustomComboBoxSearch):
    """ Classe base per la ricerca fornitori """

    def __init__(self):
        CustomComboBoxSearch.__init__(self)

        idHandler = self.connect('changed',
                                 self.on_combobox_fornitore_search_clicked)
        self.setChangedHandler(idHandler)

        self.connect("destroy-event", self.on_widget_destroy)

        self._callName = None
        self._ricerca = None
        self._filter = True
        self._resultsCount = 0
        self.clear()

    def on_combobox_fornitore_search_clicked(self, combobox, callName=None):
        #richiama la ricerca dei fornitori

        def refresh_combobox_fornitore(anagWindow):
            self._resultsCount = self._ricerca.getResultsCount()
            resultsElement = self._ricerca.getResultsElement()
            if not(self._resultsCount > 0):
                self.set_active(0)
                return

            if self._resultsCount == 1:
                id = resultsElement.id
                res = leggiFornitore(id)
                denominazione = res["ragioneSociale"]
                if denominazione == '':
                    denominazione = res["nome"] + ' ' + res["cognome"]
                combobox.refresh(id, denominazione, res)
            else:
                self.idlist = []
                for ids in resultsElement:
                    self.idlist.append(ids.id)
                combobox.refresh(self.idlist, ('< %d fornitori selezionati... >' % self._resultsCount), None, rowType='old_search')
            if self._callName is not None:
                self._callName()

        if combobox.on_selection_changed():
            if self._ricerca is None:
                from promogest.ui.RicercaComplessaFornitori import RicercaComplessaFornitori
                self._ricerca = RicercaComplessaFornitori()
                if not self._filter:
                    self._ricerca.setTreeViewSelectionType(gtk.SELECTION_SINGLE)
            else:
                self._ricerca.refresh()
            anagWindow = self._ricerca.getTopLevel()
            returnWindow = combobox.get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.connect("hide",
                               refresh_combobox_fornitore)
            self._ricerca.show_all()

        elif self._callName is not None:
            self._callName()

    def setId(self, value):
        self.insertComboboxSearchFornitore(self, value)

    def getId(self):
        if self.isEmpty():
            self.clear()
        elif (self._resultsCount > 1) and (self._ricerca is not None):
            self._ricerca.refresh()
            return self.idlist
        return self._id

    def getData(self):
        return self._container

    def insertComboboxSearchFornitore(self, combobox, idFornitore, clear=False, filter=True):
        res = leggiFornitore(idFornitore)
        denominazione = res["ragioneSociale"]
        if denominazione == '':
            denominazione = res["nome"] + ' ' + res["cognome"]
        combobox.refresh(idFornitore, denominazione, res, clear, filter)

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
