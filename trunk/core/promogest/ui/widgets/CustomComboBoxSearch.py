# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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
from promogest.lib.utils import *


class CustomComboBoxSearch(gtk.Entry):
    __gtype_name__ = 'CustomComboBoxSearch'

    def __init__(self):
        self._id = None
        self._container = None
        self.__rebuildList = False
        self._idChangedHandler = None
        gtk.Entry.__init__(self)
        self.set_property("can-focus", True)
        self.connect("show", self.on_show)
        #self.connect('changed',
                         #self.on_entry_key_press_event,self)
        #self.connect("icon-press", self.on_icon_press)
        #self.connect("focus-in-event", self.on_focus_in_event)
        #self.connect("focus-out-event", self.on_focus_out_event)
        self.set_property("sensitive", True)
        #self.set_icon_tooltip_text("primary","Clicca per aprire la ricerca")
        self.set_property("secondary_icon_stock", "gtk-clear")
        self.set_property("secondary-icon-activatable", True)
        self.set_property("secondary-icon-sensitive", True)
        self.set_property("primary_icon_stock", "gtk-find")
        self.set_property("primary-icon-activatable", True)
        self.set_property("primary-icon-sensitive", True)
        self.anaedit = None
        self.draw()

    def draw(self, filter=True, idType=None):
        self.__rebuildList = True
        if idType == 'str':
            model = gtk.ListStore(str, str, str, object)
        else:
            model = gtk.ListStore(str, int, str, object)
        #self.set_model(model)
        self.__model = model

        self.completion = gtk.EntryCompletion()
        self.completion.set_popup_single_match(True)
        if Environment.pg3:
            self.completion.set_match_func(self.match_func, None)
        else:
            self.completion.set_match_func(self.match_func)
        self.completion.connect('match-selected',
                         self.on_completion_match_main)
        self.completion.set_model(model)
        self.completion.set_text_column(2)
        self.set_completion(self.completion)
        model.clear()
        self.__rebuildList = False

    def on_icon_press(self, entry):
        print "GENERIC ICON PRESS"

    def on_entry_key_press_event(self, widget, event=None):
        """ """
        keyname = widget.get_text().lstrip()
        #print "KEYNAME PRINCIPALE", keyname, self._id
        if len(keyname) > 1:
            self.ricercaDao(keyname)

    def giveAnag(self, anag):
        """Faccio scendere l'anag nel caso servisse per
        richiamare qualche metodo
        """
        self.anaedit = anag

    def ricercaDao(self, keyname):
        """ Qui si rimanda per la gestione della completition
            Basta un import di una piccola funzione che fa la query
            e inserisce i risultati nella tendina per la selezione
        """
        pass

    def match_func(self, completion, key, iter, user_data=None):
        model = completion.get_model()
        #self._id = None
        #self._container = None
        if model[iter][2] and self.get_text().lower() in model[iter][2].lower():
            #self._id = model[iter][1]
            #self._container = model[iter][3]
            #print "CONTAINER+ID", self._container, self._id
            try:
                self.anaedit.on_id_articolo_customcombobox_changed()
            except:
                pass
            #print " QUANTO VIENI TRIGGATO", self.anaedit
            try:
                self.anaedit.persona_giuridica_changed()
            except:
                #print " TEST SU DOCUMENTI MODIFICA CLIENTE/LISTINO, poi togliere"
                pass
            return model[iter][2]
        #else:
            #self._id = None
            #self._container = None
            #return None

    def on_completion_match_main(self, completion=None, model=None, iter=None):
        #print "SEI L?ULTIMO STEPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP" , self.anaedit
        #return
        #self.articolo_matchato = model[iter][2]
        #self.set_position(-1)
        #model = self.completion.get_model()
        self._id = model[iter][1]
        self._container = model[iter][3]
        #print " ARTICOLO MATCHATO", self._id, model[iter][2]
        #try:
            #self.anaedit.persona_giuridica_changed()
        #except:
            #print " TEST SU DOCUMENTI MODIFICA CLIENTE/LISTINO, poi togliere"
            #pass
        #if model[iter][2] and self.get_text().lower() in model[iter][2].lower():
            #self.set_text(model[iter][2])
        self.set_position(-1)
        #return model[iter][2]

    def set_active(self, data):
        self.set_text("")
        self._id = None
        self._container = None

    def on_selection_changed(self):
        return

    def refresh(self, id=None, denominazione=None, container=None, clear=False, filter=True, idType=None, rowType='element'):
        #print "SEI TU IL PROBLEMA"
        self._id = id
        self.set_text(denominazione or "")
        return

    def clear_entry(self):
        self.set_text("")
        self._id = None
        self.grab_focus()

    def clean_entry(self):
        self.set_text("")
        self._id = None
        self.grab_focus()

    def getContainer(self):
        return self._container

    def setChangedHandler(self, idHandler):
        return self.setHandler(idHandler)

    def setHandler(self, tipo):
        if tipo == "commessa":
            self.connect("icon-press", on_commesse_icon_press)
            self.connect("changed", on_commesse_customcombobox_changed)
        elif tipo == "agente":
            self.connect("icon-press", on_agente_icon_press)
            self.connect("changed", on_agente_customcombobox_changed)
        elif tipo == "vettore":
            self.connect("icon-press", on_vettore_icon_press)
            self.connect("changed", on_vettore_customcombobox_changed)

        self.set_property("secondary_icon_stock", "gtk-clear")
        self.set_property("secondary-icon-activatable", True)
        self.set_property("secondary-icon-sensitive", True)
        self.set_property("primary_icon_stock", "gtk-find")
        self.set_property("primary-icon-activatable", True)
        self.set_property("primary-icon-sensitive", True)

        return
        self._idChangedHandler = idHandler

        if idHandler == "cliente":
            def on_icon_press(entry, position, event):
                """
                scopettina agganciata ad un segnale generico
                """
                if position.value_nick == "primary":

                    def refresh_entry(anagWindow):
                        if not anag.dao:
                            self.set_active(0)
                            return

                        id = anag.dao.id
                        res = leggiCliente(id)
                        denominazione = res["ragioneSociale"]
                        if denominazione == '':
                            denominazione = res["nome"] + ' ' + res["cognome"]
                        self.set_text(denominazione)
                        self._id = id
                    from promogest.ui.anagClienti.AnagraficaClientiFilter import RicercaClienti
                    anag = RicercaClienti()
                    anagWindow = anag.getTopLevel()
                    anagWindow.show_all()
                    anagWindow.connect("hide",
                                       refresh_entry)
                    anag.show_all()
                else:                            # secondary
                    self.clear_entry()

            self.connect("icon-press", on_icon_press)
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
        return
        model = self.get_model()
        rowIndex = self.get_active()
        return ((rowIndex == -1) or (model[rowIndex][0] == 'empty'))

gobject.type_register(CustomComboBoxSearch)
