# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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

from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.RuoliAzioni.dao.Action import Action
from promogest.modules.RuoliAzioni.dao.RoleAction import RoleAction
from promogest.ui.utilsCombobox import *
from promogest.lib.utils import *
from promogest.ui.gtk_compat import *


class ManageRuoloAzioni(GladeWidget):
    """ Frame per la spedizione email """

    def __init__(self, string=None, d=False):
        GladeWidget.__init__(self, 'roleaction',
                fileName= 'RuoliAzioni/gui/roleaction.glade',
                                isModule=True)
        self.placeWindow(self.getTopLevel())
        self.getTopLevel().set_modal(True)
        self.getTopLevel().show_all()
        self.titolo.set_markup("""
        Questa finestra permette di abbinare ad un ruolo
        precedentemente creato una delle
        azioni possibili. Seleziona un Ruolo e poi premi abbina
        seleziona le azioni cliccando sulla checkbox e premi salva.
                                    """)
        self.draw()
        self.refresh()

    def draw(self):

        # Colonne della Treeview per il filtro/modifica
        treeview = self.anagrafica_treeview_role

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        #renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 5)
        column = gtk.TreeViewColumn('Den. breve', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        #column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        #renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Denominazione', renderer, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        #column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable',True)
        renderer.connect('toggled', self.on_column_edited, None, treeview)
        #renderer.set_active(False)
        column = gtk.TreeViewColumn('Attiva/Disattiva', renderer, active=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object, str, str, bool)
        treeview.set_model(self._treeViewModel)

        treeview.set_search_column(1)

    def on_column_edited(self, cell, path, value, treeview, editNext=True):
        """ Gestisce l'immagazzinamento dei valori nelle celle """
        model = treeview.get_model()
        iterator = model.get_iter(path)
        row = model[iterator]
        row[3]= not row[3]
        model.set(iterator, 3, row[3])

    def on_save_button_clicked(self,button):
        self.saveDao()
        self.hide()

    def on_annulla_button_clicked(self, button):
        self.hide()

    def clear(self):
        self._treeViewModel.clear()

    def refresh(self):
        fillComboboxRole(self.id_role_filter_combobox, True)

    def on_abbina_button_clicked(self, button):
        self.clear()
        azioni= Action().select(batchSize=None)
        self.idRole = findIdFromCombobox(self.id_role_filter_combobox)
        for i in azioni:
            roleActions = RoleAction().select(id_role=self.idRole,id_action = i.id)
            if roleActions ==[]:
                act= False
            else:
                act=True
            self._treeViewModel.append([i, i.denominazione or '', i.denominazione_breve or '', act])

    def saveDao(self):
        model = self.anagrafica_treeview_role.get_model()
        for row in model:
            if row[3] and RoleAction().select(id_role =self.idRole,id_action=row[0].id) ==[]:
                self.dao= RoleAction()
                self.dao.id_role = self.idRole
                self.dao.id_action = row[0].id
                self.dao.persist()
            elif not row[3] and not RoleAction().select(id_role=self.idRole,id_action=row[0].id) ==[]:
                if self.idRole != 1:
                    riga= RoleAction().select(id_role=self.idRole,id_action=row[0].id)[0]
                    riga.delete()
        return
