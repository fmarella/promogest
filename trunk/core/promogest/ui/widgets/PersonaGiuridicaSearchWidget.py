# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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
from CustomComboBoxSearch import CustomComboBoxSearch
from promogest.lib.utils import leggiCliente, leggiFornitore


class PersonaGiuridicaSearchWidget(CustomComboBoxSearch):
    """ Classe base per la ricerca clienti """
    __gtype_name__ = 'PersonaGiuridicaSearchWidget'
    def __init__(self):
        CustomComboBoxSearch.__init__(self)

        self.connect("delete-event", self.on_widget_delete)
        self.connect('changed',
                           self.on_entry_key_press_event)
        #self.connect("destroy-event", self.on_widget_destroy)
        self.connect("icon-press", self.on_icon_press)
        self._callName = None
        self._ricerca = None
        self._filter = True
        self._resultsCount = 0
        self._type = 'cliente'
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
                    self.setId(id)
                    try:
                        self.anaedit.persona_giuridica_changed(self)
                    except:
                        pass

            if self._type == 'cliente':
                from promogest.ui.RicercaComplessaClienti import RicercaComplessaClienti
                self._ricerca = RicercaComplessaClienti()
            elif self._type == 'fornitore':
                from promogest.ui.RicercaComplessaFornitori import RicercaComplessaFornitori
                self._ricerca = RicercaComplessaFornitori()
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
            self.clean_entry()


    def ricercaDao(self, keyname):
        from promogest.dao.Cliente import Cliente
        from promogest.dao.Fornitore import Fornitore
        if self._type == "fornitore":
            cli = Fornitore().select(ragioneSociale=keyname, batchSize=40)
        else:
            cli = Cliente().select(ragioneSociale=keyname, batchSize=40)
        model = self.completion.get_model()
        model.clear()
        for m in cli:
            rag = m.ragione_sociale or (m.cognome + " " + m.nome)
            model.append(('empty', m.id, rag, m))


    def setId(self, value):
        self.insertComboboxSearchPersonaGiuridica(self, value)
        self._id = value


    def getId(self):
        #if self.isEmpty():
            #self.clear()
        #elif (self._resultsCount > 1) and (self._ricerca is not None):
            #self._ricerca.refresh()
            #return self.idlist
        return self._id


    def getData(self):
        self.insertComboboxSearchPersonaGiuridica(self, self._id)
        return self._container


    def insertComboboxSearchPersonaGiuridica(self, combobox, id, clear=False, filter=True):
        if self._type == 'cliente':
            res = leggiCliente(id)
        elif self._type == 'fornitore':
            res = leggiFornitore(id)
        denominazione = res["ragioneSociale"] or (res["nome"] + ' ' + res["cognome"])
        #if denominazione == '':
            #denominazione = res["nome"] + ' ' + res["cognome"]
        combobox.refresh(id, denominazione, res, clear, filter)
        #self.set_text(denominazione)
        #print "IDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", id
        #self._id = id
        #self.set_text(denominazione)
        self._container = res


    def clear(self):
        self.set_active(0)


    def setOnChangedCall(self, callName=None):
        self._callName = callName


    def setSingleValue(self):
        self._filter = False


    def setMultipleValues(self):
        self._filter = True


    def setType(self, type='cliente'):
        if self._type != type and self._ricerca is not None:
            anagWindow = self._ricerca.getTopLevel()
            anagWindow.destroy()
            del self._ricerca
            self._ricerca = None
        self._type = type


    def getType(self):
        return self._type


    def on_widget_delete(self, widget, event):
        if self._ricerca is not None:
            anagWindow = self._ricerca.getTopLevel()
            anagWindow.destroy()
            del self._ricerca
            self._ricerca = None
