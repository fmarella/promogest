# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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
from promogest import Environment

from CustomComboBoxSearch import CustomComboBoxSearch
from promogest.lib.utils import leggiArticolo
from promogest.ui.utilsCombobox import fillComboboxListini,findIdFromCombobox,findComboboxRowFromId
#from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli

class ArticoloSearchWidget(CustomComboBoxSearch):
    """ Classe base per la ricerca articoli """
    __gtype_name__ = 'ArticoloSearchWidget'
    def __init__(self):
        CustomComboBoxSearch.__init__(self)

        self.connect('changed',
                           self.on_entry_key_press_event)
        #self.setChangedHandler(idHandler)

        #self.connect("destroy-event", self.on_widget_destroy)
        self.connect("icon-press", self.on_icon_press)
        self._callName = None
        self._ricerca = None
        self._filter = True
        self._resultsCount = 0
        self.clear()


    def on_icon_press(self,entry,position,event):
        """
        scopettina agganciata ad un segnale generico
        """
        if position.value_nick == "primary":

            def refresh_entry(anagWindow):
                self._resultsCount = self._ricerca.getResultsCount()
                resultsElement = self._ricerca.getResultsElement()
                if not(self._resultsCount > 0):
                    self.set_active(0)
                    return

                if self._resultsCount == 1:
                    id = resultsElement.id
                    res = leggiArticolo(id)
                    denominazione = res["denominazione"]
                    self.set_text(denominazione)
                    self._id = id
                    self._container = res["daoArticolo"]
                    try:
                        self.anaedit.on_id_articolo_customcombobox_changed()
                    except:
                        pass

            from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
            self._ricerca = RicercaComplessaArticoli()
            if not self._filter:
                self._ricerca.setTreeViewSelectionType(GTK_SELECTIONMODE_SINGLE)
            else:
                self._ricerca.refresh()
            anagWindow = self._ricerca.getTopLevel()
            returnWindow = self.get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.connect("hide",
                               refresh_entry)
            self._ricerca.show_all()
        else:                            #secondary
            self.set_text("")
            self._id = None
            self.grab_focus()

    def ricercaDao(self, keyname):
        from promogest.dao.Articolo import Articolo
        #print keyname
        cli = Articolo().select(denominazione=keyname, cancellato=True, batchSize=40)
        model = self.completion.get_model()
        model.clear()
        for m in cli:
            model.append(('empty', m.id, m.denominazione, m))

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
        self._container = res

    def clear(self):
        self.set_active(0)

    def setOnChangedCall(self, callName=None):
        self._callName = callName

    def setSingleValue(self):
        self._filter = False

    def setMultipleValues(self):
        self._filter = True

gobject.type_register(ArticoloSearchWidget)