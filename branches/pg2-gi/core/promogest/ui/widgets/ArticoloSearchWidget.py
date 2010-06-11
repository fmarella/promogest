# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <andrea@promotux.it>


import gtk
from promogest import Environment
from CustomComboBoxSearch import CustomComboBoxSearch
from promogest.ui.utils import leggiArticolo
from promogest.ui.utilsCombobox import fillComboboxListini,findIdFromCombobox,findComboboxRowFromId

class ArticoloSearchWidget(CustomComboBoxSearch):
    """ Classe base per la ricerca articoli """
    __gtype_name__ = 'ArticoloSearchWidget'
    def __init__(self):
        CustomComboBoxSearch.__init__(self)

        idHandler = self.connect('changed',
                                 self.on_combobox_articolo_search_clicked)
        self.setChangedHandler(idHandler)
        self._callName = None
        self._ricerca = None
        self._filter = True
        self._resultsCount = 0
        self.clear()


    def on_combobox_articolo_search_clicked(self, combobox):
        #richiama la ricerca degli articoli

        def refresh_combobox_articolo(anagWindow):
            """
                Si è resa necessaria una modifica a questa funzione per prelevare
                i risultati passati alla combo dalla ricerca complessa
                nel primo campo, si prelevano gli id  e si passano per l'elaborazione
            """
            self._resultsCount = self._ricerca.getResultsCount()
            resultsElement = self._ricerca.getResultsElement()
            if not(self._resultsCount > 0):
                self.set_active(0)
                return

            if self._resultsCount == 1:
                id = resultsElement.id
                res = leggiArticolo(id)
                combobox.refresh(id, res["denominazione"], res)
            else:
                self.idlist = []
                for ids in resultsElement:
                    self.idlist.append(ids.id)
                combobox.refresh(self.idlist, ('< %d articoli selezionati... >' % self._resultsCount), None, rowType='old_search')
            if self._callName is not None:
                self._callName()

        if combobox.on_selection_changed():
            if self._ricerca is None:
                from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
                self._ricerca = RicercaComplessaArticoli(listinoFissato=Environment.listinoFissato)
                Environment.listinoFissato = None
                if not self._filter:
                    self._ricerca.setTreeViewSelectionType(gtk.SELECTION_SINGLE)
            else:
                self._ricerca.refresh()
            anagWindow = self._ricerca.getTopLevel()
            returnWindow = combobox.get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.connect("hide",
                               refresh_combobox_articolo)
            self._ricerca.show_all()

        elif self._callName is not None:
            self._callName()


    def setId(self, value):
        self.insertComboboxSearchArticolo(self, value)


    def getId(self):
        """
            funziona modificata per passare una lista di id necessari alla ricerca
            prima veniva creata una tabella con i risultati della ricerca
            e la si usava per le ricerche successive, adesso si devono far passare i dati via codice
        """
        if self.isEmpty():
            self.clear()
        elif (self._resultsCount > 1) and (self._ricerca is not None):
            self._ricerca.refresh()
            return self.idlist
        return self._id

    def getData(self):
        return self._container


    def insertComboboxSearchArticolo(self, combobox, idArticolo, clear=False, filter=True):
        res = leggiArticolo(idArticolo)
        combobox.refresh(idArticolo, res["denominazione"], res, clear, filter)

    def clear(self):
        self.set_active(0)

    def setOnChangedCall(self, callName=None):
        self._callName = callName

    def setSingleValue(self):
        self._filter = False

    def setMultipleValues(self):
        self._filter = True
