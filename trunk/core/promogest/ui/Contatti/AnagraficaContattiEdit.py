# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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

__author__ = 'Francesco Meloni'

from promogest.ui.gtk_compat import *
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest import Environment
from promogest.dao.daoContatti.Contatto import Contatto
from promogest.dao.daoContatti.ContattoCliente import ContattoCliente
from promogest.dao.daoContatti.ContattoFornitore import ContattoFornitore
from promogest.dao.daoContatti.ContattoMagazzino import ContattoMagazzino
from promogest.dao.daoContatti.ContattoAzienda import ContattoAzienda
from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
from promogest.dao.daoContatti.ContattoCategoriaContatto import ContattoCategoriaContatto

from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaContattiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei contatti """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                  anagrafica,
                                'Dati contatto',
                                  root='anagrafica_contatti_detail_table',
                                  path='Contatti/_anagrafica_contatti_elements.glade',
                                   )
        self._widgetFirstFocus = self.cognome_entry
        self.dao = Contatto()
        self._tabPressed = False

    def draw(self, cplx=False):
        #Popola combobox categorie contatti
        fillComboboxCategorieContatti(self.id_categoria_contatto_customcombobox.combobox)
        self.id_categoria_contatto_customcombobox.connect('clicked',
                      on_id_categoria_contatto_customcombobox_clicked)
        #Elenco categorie
        model = self.categorie_liststore
        self.categorie_treeview.set_model(model)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Categoria', rendererText, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.categorie_treeview.append_column(column)

        rendererPixbuf = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', rendererPixbuf, pixbuf=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(20)
        self.categorie_treeview.append_column(column)

        #Elenco recapiti
        model = self.recapiti_liststore
        self.recapiti_treeview.set_model(model)

        rendererCombo = gtk.CellRendererCombo()
        rendererCombo.set_property('editable', True)
        rendererCombo.connect('edited', self.on_tipo_recapito_edited, self.recapiti_treeview.get_model())
        rendererCombo.set_property('text-column', 0)
        rendererCombo.set_property('has_entry', False)
        rendererCombo.set_property('model', fillModelTipiRecapito())
        rendererCombo.set_property('width', 200)
        rendererCombo.column = 0
        column = gtk.TreeViewColumn('Tipo', rendererCombo, text=1)
        column.set_clickable(False)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        self.recapiti_treeview.append_column(column)

        rendererText = gtk.CellRendererText()
        rendererText.set_property('editable', True)
        rendererText.connect('edited', self.on_recapito_edited, self.recapiti_treeview.get_model())
        rendererText.column = 1
        column = gtk.TreeViewColumn('Recapito', rendererText, text=2)
        column.set_clickable(False)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        self.recapiti_treeview.append_column(column)
        rendererPixbuf = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', rendererPixbuf, pixbuf=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(20)
        self.recapiti_treeview.append_column(column)

        self.recapiti_treeview.set_search_column(2)

        #idHandler = self.appartenenza_customcombobox.connect('changed',
                                                             #self.on_appartenenza_customcombobox_changed)
        #if self.dao:
            #self.appartenenza_customcombobox.setChangedHandler(self.dao.tipo_contatto)
        #self.appartenenza_customcombobox.refresh(clear=True, filter=False)

        #self.cliente_radiobutton.connect('toggled',
                                         #self.on_radiobutton_toggled)
        #self.fornitore_radiobutton.connect('toggled',
                                           #self.on_radiobutton_toggled)
        #self.magazzino_radiobutton.connect('toggled',
                                           #self.on_radiobutton_toggled)
        #self.azienda_radiobutton.connect('toggled',
                                         #self.on_radiobutton_toggled)
        #self.generico_radiobutton.connect('toggled',
                                          #self.on_radiobutton_toggled)
        self.generico_radiobutton.set_active(True)
        self.on_radiobutton_toggled()
        self.categorie_contatti_add_row_button.set_sensitive(True)
        self.categorie_contatti_delete_row_button.set_sensitive(False)
        self.categorie_contatti_undelete_row_button.set_sensitive(False)
        self.categorie_treeview.get_selection().unselect_all()

        self.recapiti_add_row_button.set_sensitive(True)
        self.recapiti_delete_row_button.set_sensitive(False)
        self.recapiti_undelete_row_button.set_sensitive(False)
        self.recapiti_treeview.get_selection().unselect_all()
        if self._anagrafica._ownerKey:
            self.pg_toggle_hbox.set_sensitive(False)


    def on_categorie_contatti_add_row_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_contatto_customcombobox.combobox)
        if id is not None:
            categoria = findStrFromCombobox(self.id_categoria_contatto_customcombobox.combobox, 2)
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    return
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_ADD,
                                           GTK_ICON_SIZE_BUTTON)
            model.append((id, categoria, anagPixbuf, 'added'))
        self.categorie_treeview.get_selection().unselect_all()


    def on_categorie_contatti_delete_row_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_contatto_customcombobox.combobox)
        if id is not None:
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_REMOVE,
                                           GTK_ICON_SIZE_BUTTON)
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    if c[2] is None:
                        c[2] = anagPixbuf
                        c[3] = 'deleted'
                    else:
                        model.remove(c.iter)
        self.categorie_treeview.get_selection().unselect_all()


    def on_categorie_contatti_undelete_row_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_contatto_customcombobox.combobox)
        if id is not None:
            model = self.categorie_treeview.get_model()
            for c in model:
                if c[0] == id:
                    if c[3] == 'deleted':
                        c[2] = None
                        c[3] = None
        self.categorie_treeview.get_selection().unselect_all()


    def on_categorie_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            idCategoriaContatto = model.get_value(iterator, 0)
            findComboboxRowFromId(self.id_categoria_contatto_customcombobox.combobox, idCategoriaContatto)
            status = model.get_value(iterator, 3)
            self.categorie_contatti_delete_row_button.set_sensitive(status != 'deleted')
            self.categorie_contatti_undelete_row_button.set_sensitive(status == 'deleted')


    def on_recapiti_treeview_keypress_event(self, treeview, event):
        if event.keyval == 65289:
            self._tabPressed = True


    def on_tipo_recapito_edited(self, cell, path, value, model):
        iterator = model.get_iter(path)
        column = cell.column

        model.set_value(iterator, column+1, value)
        if self._tabPressed:
            self._tabPressed = False
        gobject.timeout_add(1, self.recapiti_treeview.set_cursor, path, self.recapiti_treeview.get_column(column+1), True)


    def on_recapito_edited(self, cell, path, value, model):
        iterator = model.get_iter(path)
        column = cell.column
        row = model[iterator]
        new = model.get_value(iterator, 0) == 0
        anagPixbuf = None
        operation = None
        if new:
            recapito = model.get_value(iterator, 2)
            tipoRecapito = model.get_value(iterator, 1)
            if recapito == '' and tipoRecapito == '':
                model.remove(iterator)
                self.recapiti_treeview_focus_out()
                return

            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_ADD,
                                           GTK_ICON_SIZE_BUTTON)
        model.set_value(iterator, column+1, value)
        model.set_value(iterator, 3, anagPixbuf)
        model.set_value(iterator, 4, operation)
        if self._tabPressed:
            self._tabPressed = False
        self.recapiti_treeview_focus_out()


    def recapiti_treeview_focus_out(self):
        self.recapiti_treeview.get_selection().unselect_all()
        self.recapiti_delete_row_button.set_sensitive(False)
        self.recapiti_undelete_row_button.set_sensitive(False)
        self.recapiti_add_row_button.grab_focus()


    def on_recapiti_add_row_button_clicked(self, widget):
        model = self.recapiti_treeview.get_model()
        iterator = model.append((0, '', '', None, None))
        column = self.recapiti_treeview.get_column(0)
        row = model[iterator]
        self.recapiti_treeview.set_cursor(row.path, column, True)


    def on_recapiti_delete_row_button_clicked(self, widget):
        sel = self.recapiti_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            new = model.get_value(iterator, 0) == 0
            if not new:
                image = gtk.Image()
                anagPixbuf = image.render_icon(gtk.STOCK_REMOVE,
                                               GTK_ICON_SIZE_BUTTON)
                operation = 'deleted'
                model.set_value(iterator, 3, anagPixbuf)
                model.set_value(iterator, 4, operation)
            else:
                model.remove(iterator)
        self.recapiti_treeview.get_selection().unselect_all()


    def on_recapiti_undelete_row_button_clicked(self, widget):
        sel = self.recapiti_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            operation = model.get_value(iterator, 4)
            if operation == 'deleted':
                anagPixbuf = None
                operation = None
                model.set_value(iterator, 3, anagPixbuf)
                model.set_value(iterator, 4, operation)
        self.recapiti_treeview.get_selection().unselect_all()


    def on_recapiti_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator is not None:
            status = model.get_value(iterator, 4)
            self.recapiti_delete_row_button.set_sensitive(status != 'deleted')
            self.recapiti_undelete_row_button.set_sensitive(status == 'deleted')


    def on_appartenenza_customcombobox_changed(self, combobox):
        """ Funzioni generiche messe in utils"""
        if self.cliente_radiobutton.get_active():
            on_combobox_cliente_search_clicked(combobox)
        elif self.fornitore_radiobutton.get_active():
            on_combobox_fornitore_search_clicked(combobox)
        elif self.magazzino_radiobutton.get_active():
            on_combobox_magazzino_search_clicked(combobox)
        elif self.azienda_radiobutton.get_active():
            on_combobox_azienda_search_clicked(combobox)


    def setDao(self, dao):
        if dao is None:
            if self._anagrafica.filter.cliente_filter_radiobutton.get_active():
                self.cliente_radiobutton.set_active(True)
            elif self._anagrafica.filter.fornitore_filter_radiobutton.get_active():
                self.fornitore_radiobutton.set_active(True)
            elif self._anagrafica.filter.magazzino_filter_radiobutton.get_active():
                self.magazzino_radiobutton.set_active(True)
            elif self._anagrafica.filter.azienda_filter_radiobutton.get_active():
                self.azienda_radiobutton.set_active(True)
            else:
                self.generico_radiobutton.set_active(True)
            # Crea un nuovo Dao vuoto
            if self.cliente_radiobutton.get_active():
                self.dao = ContattoCliente()
                self.dao.tipo_contatto = 'cliente'
                self.dao.id_cliente = self._anagrafica._ownerKey
            elif self.fornitore_radiobutton.get_active():
                self.dao = ContattoFornitore()
                self.dao.tipo_contatto = 'fornitore'
                self.dao.id_fornitore = self._anagrafica._ownerKey
            elif self.magazzino_radiobutton.get_active():
                self.dao = ContattoMagazzino()
                self.dao.tipo_contatto = 'magazzino'
                self.dao.id_magazzino = self._anagrafica._ownerKey
            elif self.azienda_radiobutton.get_active():
                self.dao = ContattoAzienda()
                self.dao.tipo_contatto = 'azienda'
                self.dao.schema_azienda = self._anagrafica._ownerKey
            elif self.generico_radiobutton.get_active():
                self.dao = Contatto()
                self.dao.tipo_contatto = 'generico'
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            if dao.tipo_contatto == 'cliente':
                self.dao = ContattoCliente().getRecord(id=(dao.id,'cliente'))
            elif dao.tipo_contatto == 'fornitore':
                self.dao = ContattoFornitore().getRecord(id=(dao.id,'fornitore'))
            elif dao.tipo_contatto == 'magazzino':
                self.dao = ContattoMagazzino().getRecord(id=(dao.id,'magazzino'))
            elif dao.tipo_contatto == 'azienda':
                self.dao = ContattoAzienda().getRecord(id=(dao.id,'azienda'))
            elif dao.tipo_contatto == 'generico':
                self.dao = Contatto().getRecord(id=(dao.id,'generico'))
        #self.appartenenza_customcombobox.setChangedHandler(self.dao.tipo_contatto)
        self._refresh()


    def _refresh(self):
        self.on_radiobutton_toggled()
        if self.dao.tipo_contatto == 'cliente':
            self.appartenenza_customcombobox.refresh(clear=True, filter=False)
            self.cliente_radiobutton.set_active(True)
            insertComboboxSearchCliente(self.appartenenza_customcombobox,
                                        self.dao.id_cliente)
            if self._anagrafica._ownerKey:
                self.appartenenza_customcombobox.set_sensitive(False)
        elif self.dao.tipo_contatto == 'fornitore':
            self.appartenenza_customcombobox.refresh(clear=True, filter=False)
            self.fornitore_radiobutton.set_active(True)
            # self.appartenenza_customcombobox.setId(self.dao.id_fornitore)
            insertComboboxSearchFornitore(self.appartenenza_customcombobox,
                                          self.dao.id_fornitore)
            if self._anagrafica._ownerKey:
                self.appartenenza_customcombobox.set_sensitive(False)
        elif self.dao.tipo_contatto == 'magazzino':
            self.appartenenza_customcombobox.refresh(clear=True, filter=False)
            self.magazzino_radiobutton.set_active(True)
            insertComboboxSearchMagazzino(self.appartenenza_customcombobox,
                                          self.dao.id_magazzino)
        elif self.dao.tipo_contatto == 'azienda':
            self.appartenenza_customcombobox.refresh(clear=True, filter=False, idType='str')
            self.azienda_radiobutton.set_active(True)
            insertComboboxSearchAzienda(self.appartenenza_customcombobox,
                                       self.dao.schema_azienda)
        self.cognome_entry.set_text(self.dao.cognome or '')
        self.nome_entry.set_text(self.dao.nome or '')
        self.ruolo_comboboxentry.get_child().set_text(self.dao.ruolo or '')
        self.descrizione_comboboxentry.get_child().set_text(self.dao.descrizione or '')
        textBuffer = self.note_textview.get_buffer()
        if self.dao.note is not None:
            textBuffer.set_text(self.dao.note)
        else:
            textBuffer.set_text('')
        self.note_textview.set_buffer(textBuffer)
        self._refreshRecapiti()
        self._refreshCategorie()


    def _refreshRecapiti(self, widget=None, orderBy=None):
        model = self.recapiti_treeview.get_model()
        model.clear()
        if not self.dao.id:
            return
        else:
            recapiti = self.dao.recapiti
            for r in recapiti:
                model.append((r.id, r.tipo_recapito, r.recapito, None, None))


    def _refreshCategorie(self, widget=None, orderBy=None):
        model = self.categorie_treeview.get_model()
        model.clear()
        if not self.dao.id:
            return
        else:
            categorie = self.dao.categorieContatto
            for c in categorie:
                model.append((c.id_categoria_contatto, c.categoria_contatto, None, None))


    def on_radiobutton_toggled(self, widget=None):
        if self.dao.id is not None:
            if self.dao.tipo_contatto == 'cliente':
                self.cliente_radiobutton.set_active(True)
                self.cliente_radiobutton.set_sensitive(True)
                self.fornitore_radiobutton.set_sensitive(False)
                self.magazzino_radiobutton.set_sensitive(False)
                self.azienda_radiobutton.set_sensitive(False)
                self.generico_radiobutton.set_sensitive(False)
            if self.dao.tipo_contatto == 'fornitore':
                self.fornitore_radiobutton.set_active(True)
                self.fornitore_radiobutton.set_sensitive(True)
                self.cliente_radiobutton.set_sensitive(False)
                self.magazzino_radiobutton.set_sensitive(False)
                self.azienda_radiobutton.set_sensitive(False)
                self.generico_radiobutton.set_sensitive(False)
            if self.dao.tipo_contatto == 'magazzino':
                self.magazzino_radiobutton.set_active(True)
                self.magazzino_radiobutton.set_sensitive(True)
                self.cliente_radiobutton.set_sensitive(False)
                self.fornitore_radiobutton.set_sensitive(False)
                self.azienda_radiobutton.set_sensitive(False)
                self.generico_radiobutton.set_sensitive(False)
            if self.dao.tipo_contatto == 'azienda':
                self.azienda_radiobutton.set_active(True)
                self.azienda_radiobutton.set_sensitive(True)
                self.cliente_radiobutton.set_sensitive(False)
                self.fornitore_radiobutton.set_sensitive(False)
                self.magazzino_radiobutton.set_sensitive(False)
                self.generico_radiobutton.set_sensitive(False)
            if self.dao.tipo_contatto == 'generico':
                self.generico_radiobutton.set_active(True)
                self.generico_radiobutton.set_sensitive(True)
                self.cliente_radiobutton.set_sensitive(False)
                self.fornitore_radiobutton.set_sensitive(False)
                self.magazzino_radiobutton.set_sensitive(False)
                self.azienda_radiobutton.set_sensitive(False)
        else:
            self.cliente_radiobutton.set_sensitive(True)
            self.fornitore_radiobutton.set_sensitive(True)
            self.magazzino_radiobutton.set_sensitive(True)
            self.azienda_radiobutton.set_sensitive(True)
            self.generico_radiobutton.set_sensitive(True)
            if self.azienda_radiobutton.get_active():
                self.appartenenza_customcombobox.refresh(clear=True, filter=False, idType='str')
            else:
                self.appartenenza_customcombobox.refresh(clear=True, filter=False)
            self.appartenenza_customcombobox.set_active(0)

        if self.generico_radiobutton.get_active():
            self.appartenenza_customcombobox.set_active(0)
            self.appartenenza_customcombobox.set_sensitive(False)
            self.appartenenza_label.set_text('-')
        else:
            if self.dao.id is None:
                self.appartenenza_customcombobox.set_sensitive(True)
                self.appartenenza_customcombobox.grab_focus()
                self.appartenenza_customcombobox.set_property("secondary_icon_stock", "gtk-clear")
                self.appartenenza_customcombobox.set_property("secondary-icon-activatable", True)
                self.appartenenza_customcombobox.set_property("secondary-icon-sensitive", True)
                self.appartenenza_customcombobox.set_property("primary_icon_stock", "gtk-find")
                self.appartenenza_customcombobox.set_property("primary-icon-activatable", True)
                self.appartenenza_customcombobox.set_property("primary-icon-sensitive", True)
            else:
                self.appartenenza_customcombobox.set_sensitive(False)
                self.cognome_entry.grab_focus()
            if self.cliente_radiobutton.get_active():
                self.appartenenza_label.set_text('Cliente')
                self.appartenenza_customcombobox.setChangedHandler("cliente")
            elif self.fornitore_radiobutton.get_active():
                self.appartenenza_label.set_text('Fornitore')
                self.appartenenza_customcombobox.setChangedHandler("fornitore")
            elif self.magazzino_radiobutton.get_active():
                self.appartenenza_label.set_text('Magazzino')
                self.appartenenza_customcombobox.setChangedHandler("magazzino")
            elif self.azienda_radiobutton.get_active():
                self.appartenenza_label.set_text('Azienda')
                self.appartenenza_customcombobox.setChangedHandler("azienda")



    def saveDao(self, tipo=None):
        if not self.generico_radiobutton.get_active():
            if self.appartenenza_customcombobox._id is None:
                obligatoryField(self.dialogTopLevel, self.appartenenza_customcombobox)
        if self.cliente_radiobutton.get_active():
            if self.dao.id is None:
                self.dao = ContattoCliente()
            self.dao.id_cliente = self.appartenenza_customcombobox._id
            self.dao.tipo_contatto ="cliente"
        elif self.fornitore_radiobutton.get_active():
            if self.dao.id is None:
                self.dao = ContattoFornitore()
            self.dao.id_fornitore = self.appartenenza_customcombobox._id
            self.dao.tipo_contatto ="fornitore"
        elif self.magazzino_radiobutton.get_active():
            if self.dao.id is None:
                self.dao = ContattoMagazzino()
            self.dao.id_magazzino = self.appartenenza_customcombobox._id
            self.dao.tipo_contatto ="magazzino"
        elif self.azienda_radiobutton.get_active():
            if self.dao.id is None:
                self.dao = ContattoAzienda()
            self.dao.schema_azienda = self.appartenenza_customcombobox._id
            self.dao.tipo_contatto ="azienda"
        elif self.generico_radiobutton.get_active():
            if self.dao.id is None:
                self.dao = Contatto()
            self.dao.tipo_contatto ="generico"


        self.dao.cognome = self.cognome_entry.get_text()
        self.dao.nome = self.nome_entry.get_text()
        #self.dao.ruolo = self.ruolo_comboboxentry.get_child().get_text()
        #self.dao.descrizione = self.descrizione_comboboxentry.get_child().get_text()
        #tree_iter = self.ruolo_comboboxentry.get_active_iter()
        #if tree_iter != None:
            #model = self.ruolo_comboboxentry.get_model()
            #row_id, name = model[tree_iter][:1]
            #self.dao.ruolo = name
        #else:
        entry = self.ruolo_comboboxentry.get_child()
        self.dao.ruolo =  entry.get_text()

        #tree_iter = self.descrizione_comboboxentry.get_active_iter()
        #if tree_iter != None:
            #model = self.descrizione_comboboxentry.get_model()
            #row_id, name = model[tree_iter][:1]
            #self.dao.descrizione = name
        #else:
        entry = self.descrizione_comboboxentry.get_child()
        self.dao.descrizione = entry.get_text()



        textBuffer = self.note_textview.get_buffer()
        self.dao.note = textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter(),True)
        if Environment.tipo_eng =="sqlite" and not self.dao.id:
            forMaxId = Contatto().select(batchSize=None)
            if not forMaxId:
                self.dao.id = 1
            else:
                idss = []
                for l in forMaxId:
                    idss.append(l.id)
                self.dao.id = (max(idss)) +1
        #self.daoid=self.dao.id
        self.dao.persist()
        # Salvo categorie contatti
        model = self.categorie_treeview.get_model()

        cleanContattoCategoriaContatto = ContattoCategoriaContatto()\
                                                    .select(idContatto=self.dao.id,
                                                    batchSize=None)
        for contatto in cleanContattoCategoriaContatto:
            contatto.delete()
        for c in model:
            if c[3] == 'deleted':
                pass
            else:
                daoContattoCategoriaContatto = ContattoCategoriaContatto()
                daoContattoCategoriaContatto.id_contatto = self.dao.id
                daoContattoCategoriaContatto.id_categoria_contatto = c[0]
                daoContattoCategoriaContatto.persist()

        ## Salvo recapiti
        model = self.recapiti_treeview.get_model()
        recapiti = []
        cleanRecapitoContatto = RecapitoContatto().select(idContatto=self.dao.id)
        for recapito in cleanRecapitoContatto:
            recapito.delete()

        for r in model:
            if r[4] == 'deleted':
                pass
            else:
                if r[1] == '' or r[2] == '':
                    continue
                daoRecapitoContatto = RecapitoContatto()
                daoRecapitoContatto.id_contatto = self.dao.id
                daoRecapitoContatto.tipo_recapito = r[1]
                daoRecapitoContatto.recapito = r[2]
                daoRecapitoContatto.persist()


        self._refreshCategorie()
        self._refreshRecapiti()

