# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Enrico Pintus <enrico@promotux.it>
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

import gtk
from CustomComboBoxSearch import CustomComboBoxSearch
from promogest.ui.utils import leggiCliente, leggiFornitore

class PersonaGiuridicaSearchWidget(CustomComboBoxSearch):
    """ Classe base per la ricerca clienti """

    def __init__(self):
        CustomComboBoxSearch.__init__(self)
        idHandler = self.connect('changed',
                                 self.on_combobox_persona_giuridica_search_clicked)
        self.setChangedHandler(idHandler)

        self.connect("delete-event", self.on_widget_delete)

        self._callName = None
        self._ricerca = None
        self._filter = True
        self._resultsCount = 0
        self._type = 'cliente'
        self.clear()


    def on_combobox_persona_giuridica_search_clicked(self, combobox):
        #richiama la ricerca clienti/fornitori

        def refresh_combobox_persona_giuridica(anagWindow):
            self._resultsCount = self._ricerca.getResultsCount()
            resultsElement = self._ricerca.getResultsElement()
            if not(self._resultsCount > 0):
                self.set_active(0)
                return

            if self._resultsCount == 1:
                id = resultsElement.id
                if self._type == 'cliente':
                    res = leggiCliente(id)
                elif self._type == 'fornitore':
                    res = leggiFornitore(id)
                denominazione = res["ragioneSociale"]
                if denominazione == '':
                    denominazione = res["nome"] + ' ' + res["cognome"]
                combobox.refresh(id, denominazione, res)
            else:
                self.idlist = []
                for ids in resultsElement:
                    self.idlist.append(ids.id)
                if self._type == 'cliente':
                    combobox.refresh(self.idlist, ('< %d clienti selezionati... >' % self._resultsCount), None, rowType='old_search')
                elif self._type == 'fornitore':
                    combobox.refresh(self.idlist, ('< %d fornitori selezionati... >' % self._resultsCount), None, rowType='old_search')
            if self._callName is not None:
                self._callName()

        if combobox.on_selection_changed():
            #if self._ricerca is None:
            if self._type == 'cliente':
                from promogest.ui.RicercaComplessaClienti import RicercaComplessaClienti
                self._ricerca = RicercaComplessaClienti()
            elif self._type == 'fornitore':
                from promogest.ui.RicercaComplessaFornitori import RicercaComplessaFornitori
                self._ricerca = RicercaComplessaFornitori()
            if not self._filter:
                self._ricerca.setTreeViewSelectionType(gtk.SELECTION_SINGLE)
            #else:
                #self._ricerca.refresh()
            anagWindow = self._ricerca.getTopLevel()
            returnWindow = combobox.get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anagWindow.connect("hide",
                               refresh_combobox_persona_giuridica)
            self._ricerca.show_all()

        elif self._callName is not None:
            self._callName()


    def setId(self, value):
        self.insertComboboxSearchPersonaGiuridica(self, value)


    def getId(self):
        if self.isEmpty():
            self.clear()
        elif (self._resultsCount > 1) and (self._ricerca is not None):
            self._ricerca.refresh()
            return self.idlist
        return self._id


    def getData(self):
        return self._container


    def insertComboboxSearchPersonaGiuridica(self, combobox, id, clear=False, filter=True):
        if self._type == 'cliente':
            res = leggiCliente(id)
        elif self._type == 'fornitore':
            res = leggiFornitore(id)
        denominazione = res["ragioneSociale"]
        if denominazione == '':
            denominazione = res["nome"] + ' ' + res["cognome"]
        combobox.refresh(id, denominazione, res, clear, filter)


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
