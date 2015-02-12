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
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.dao.daoContatti.Contatto import Contatto
from promogest.dao.daoContatti.ContattoCliente import ContattoCliente
from promogest.dao.daoContatti.ContattoFornitore import ContattoFornitore
from promogest.dao.daoContatti.ContattoMagazzino import ContattoMagazzino
from promogest.dao.daoContatti.ContattoAzienda import ContattoAzienda
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaContattiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei contatti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                  anagrafica,
                  root='anagrafica_contatti_filter_table',
                  path='Contatti/_anagrafica_contatti_elements.glade',
                   )
#        self._widgetFirstFocus = self.appartenenza_filter_entry

    def draw(self, cplx=False):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Cognome - Nome', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,
                                            (None, Contatto.cognome))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(300)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ruolo', renderer, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, Contatto.ruolo))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,
                                            (None, Contatto.descrizione))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Relativo a', renderer, text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        # treeview.set_search_column(1)

        # self._treeViewModel = gtk.ListStore(object, str, str, str, str)
        self._treeViewModel = self.contatti_filter_liststore
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.clear()
        if self._anagrafica._ownerType == 'cliente':
            self.cliente_filter_radiobutton.set_active(True)
            self.id_cliente_filter_customcombobox.setId(self._anagrafica._ownerKey)
        elif self._anagrafica._ownerType == 'fornitore':
            self.fornitore_filter_radiobutton.set_active(True)
            self.id_fornitore_filter_customcombobox.setId(self._anagrafica._ownerKey)
        elif self._anagrafica._ownerType == 'magazzino':
            self.magazzino_filter_radiobutton.set_active(True)
            findComboboxRowFromId(self.id_magazzino_filter_combobox, self._anagrafica._ownerKey)
        elif self._anagrafica._ownerType == 'azienda':
            self.azienda_filter_radiobutton.set_active(True)
            findComboboxRowFromId(self.schema_azienda_filter_combobox, self._anagrafica._ownerKey)
        else:
            self.generico_filter_radiobutton.set_active(True)
        if self._anagrafica._ownerKey:
            self.pg_toggle_hbox.set_sensitive(False)

        #self.cliente_filter_radiobutton.connect('toggled',
                                                #self.on_filter_radiobutton_toggled)
        #self.fornitore_filter_radiobutton.connect('toggled',
                                                  #self.on_filter_radiobutton_toggled)
        #self.magazzino_filter_radiobutton.connect('toggled',
                                                  #self.on_filter_radiobutton_toggled)
        #self.azienda_filter_radiobutton.connect('toggled',
                                                #self.on_filter_radiobutton_toggled)
        #self.generico_filter_radiobutton.connect('toggled',
                                                 #self.on_filter_radiobutton_toggled)
        self.on_filter_radiobutton_toggled()

        self.refresh()

    def clear(self):
        # Annullamento filtro
        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
        fillComboboxAziende(self.schema_azienda_filter_combobox, True)
        fillComboboxCategorieContatti(self.id_categoria_contatto_filter_combobox, True)
        fillComboboxTipiRecapito(self.tipo_recapito_filter_comboboxentry)

        self.id_cliente_filter_customcombobox.set_active(0)
        self.id_fornitore_filter_customcombobox.set_active(0)
        self.id_magazzino_filter_combobox.set_active(0)
        self.schema_azienda_filter_combobox.set_active(0)
#        self.appartenenza_filter_entry.set_text('')
        self.cognome_nome_filter_entry.set_text('')
        self.ruolo_filter_entry.set_text('')
        self.descrizione_filter_entry.set_text('')
        self.recapito_filter_entry.set_text('')
        self.tipo_recapito_filter_comboboxentry.get_child().set_text('')
        self.id_categoria_contatto_filter_combobox.set_active(0)
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView

        cognomeNome = prepareFilterString(self.cognome_nome_filter_entry.get_text())
        ruolo = prepareFilterString(self.ruolo_filter_entry.get_text())
        descrizione = prepareFilterString(self.descrizione_filter_entry.get_text())
        recapito = prepareFilterString(self.recapito_filter_entry.get_text())
        tipoRecapito = prepareFilterString(self.tipo_recapito_filter_comboboxentry.get_child().get_text())
        idCategoria = findIdFromCombobox(self.id_categoria_contatto_filter_combobox)
        if self.cliente_filter_radiobutton.get_active():
            # CONTATTO CLIENTE
            idCliente = self.id_cliente_filter_customcombobox.getId()

            def filterCountClosure():
                return ContattoCliente().count(idCliente=idCliente,
                                                cognomeNome=cognomeNome,
                                                ruolo=ruolo,
                                                descrizione=descrizione,
                                                recapito=recapito,
                                                tipoRecapito=tipoRecapito,
                                                idCategoria=idCategoria)

            self._filterCountClosure = filterCountClosure
            self.numRecords = self.countFilterResults()
            self._refreshPageCount()
            # Let's save the current search as a closure
            def filterClosure(offset, batchSize):
                return ContattoCliente().select(orderBy=self.orderBy,
                                                    idCliente=idCliente,
                                                    cognomeNome=cognomeNome,
                                                    ruolo=ruolo,
                                                    descrizione=descrizione,
                                                    recapito=recapito,
                                                    tipoRecapito=tipoRecapito,
                                                    idCategoria=idCategoria,
                                                    offset=offset,
                                                    batchSize=batchSize)

            self._filterClosure = filterClosure
            cons = self.runFilter()
            self._treeViewModel.clear()
            for c in cons:
                self._treeViewModel.append((c,
                                            (c.cognome or '') + ' ' + (c.nome or ''),
                                            (c.ruolo or ''),
                                            (c.descrizione or ''),
                                            (c.appartenenza or '')))
            #attenzione appartenenza per contatto generico

        elif self.fornitore_filter_radiobutton.get_active():
            # CONTATTO FORNITORE
            idFornitore = self.id_fornitore_filter_customcombobox.getId()

            def filterCountClosure():
                return ContattoFornitore().count(idFornitore=idFornitore,
                                                            cognomeNome=cognomeNome,
                                                            ruolo=ruolo,
                                                            descrizione=descrizione,
                                                            recapito=recapito,
                                                            tipoRecapito=tipoRecapito,
                                                            idCategoria=idCategoria)

            self._filterCountClosure = filterCountClosure
            self.numRecords = self.countFilterResults()
            self._refreshPageCount()
            # Let's save the current search as a closure
            def filterClosure(offset, batchSize):
                return ContattoFornitore().select(orderBy=self.orderBy,
                                                            idFornitore=idFornitore,
                                                            cognomeNome=cognomeNome,
                                                            ruolo=ruolo,
                                                            descrizione=descrizione,
                                                            recapito=recapito,
                                                            tipoRecapito=tipoRecapito,
                                                            idCategoria=idCategoria,
                                                            offset=offset,
                                                            batchSize=batchSize)

            self._filterClosure = filterClosure
            cons = self.runFilter()
            self._treeViewModel.clear()
            for c in cons:
                self._treeViewModel.append((c,
                                            (c.cognome or '') + ' ' + (c.nome or ''),
                                            (c.ruolo or ''),
                                            (c.descrizione or ''),
                                            (c.appartenenza or '')))

        elif self.magazzino_filter_radiobutton.get_active():
            idMagazzino = findIdFromCombobox(self.id_magazzino_filter_combobox)
            def filterCountClosure():
                return ContattoMagazzino().count(idMagazzino=idMagazzino,
                                                            cognomeNome=cognomeNome,
                                                            ruolo=ruolo,
                                                            descrizione=descrizione,
                                                            recapito=recapito,
                                                            tipoRecapito=tipoRecapito,
                                                            idCategoria=idCategoria)

            self._filterCountClosure = filterCountClosure
            self.numRecords = self.countFilterResults()
            self._refreshPageCount()

            # Let's save the current search as a closure
            def filterClosure(offset, batchSize):
                return ContattoMagazzino().select(orderBy=self.orderBy,
                                                    idMagazzino=idMagazzino,
                                                    cognomeNome=cognomeNome,
                                                    ruolo=ruolo,
                                                    descrizione=descrizione,
                                                    recapito=recapito,
                                                    tipoRecapito=tipoRecapito,
                                                    idCategoria=idCategoria,
                                                    offset=offset,
                                                    batchSize=batchSize)

            self._filterClosure = filterClosure
            cons = self.runFilter()
            self._treeViewModel.clear()
            for c in cons:
                self._treeViewModel.append((c,
                                            (c.cognome or '') + ' ' + (c.nome or ''),
                                            (c.ruolo or ''),
                                            (c.descrizione or ''),
                                            (c.appartenenza or '')))

        elif self.azienda_filter_radiobutton.get_active():
            schemaAzienda = findIdFromCombobox(self.schema_azienda_filter_combobox)

            def filterCountClosure():
                return ContattoAzienda().count(schemaAzienda=schemaAzienda,
                                                cognomeNome=cognomeNome,
                                                ruolo=ruolo,
                                                descrizione=descrizione,
                                                recapito=recapito,
                                                tipoRecapito=tipoRecapito,
                                                idCategoria=idCategoria)

            self._filterCountClosure = filterCountClosure
            self.numRecords = self.countFilterResults()
            self._refreshPageCount()
            # Let's save the current search as a closure
            def filterClosure(offset, batchSize):
                return ContattoAzienda().select(orderBy=self.orderBy,
                                                    schemaAzienda=schemaAzienda,
                                                    cognomeNome=cognomeNome,
                                                    ruolo=ruolo,
                                                    descrizione=descrizione,
                                                    recapito=recapito,
                                                    tipoRecapito=tipoRecapito,
                                                    idCategoria=idCategoria,
                                                    offset=offset,
                                                    batchSize=batchSize)

            self._filterClosure = filterClosure
            cons = self.runFilter()
            self._treeViewModel.clear()
            for c in cons:
                self._treeViewModel.append((c,
                                            (c.cognome or '') + ' ' + (c.nome or ''),
                                            (c.ruolo or ''),
                                            (c.descrizione or ''),
                                            (c.appartenenza or '')))

        else:
            #CONTATTO GENERICO
            self.generico_filter_radiobutton.set_active(True)
#            appartenenza = prepareFilterString(self.appartenenza_filter_entry.get_text())
            def filterCountClosure():
                return Contatto().count(cognomeNome=cognomeNome,
                                        ruolo=ruolo,
                                        descrizione=descrizione,
                                        recapito=recapito,
                                        tipoRecapito=tipoRecapito,
                                        idCategoria=idCategoria,
                                            )

            self._filterCountClosure = filterCountClosure
            self.numRecords = self.countFilterResults()
            self._refreshPageCount()
            # Let's save the current search as a closure
            def filterClosure(offset, batchSize):
                return Contatto().select(orderBy=self.orderBy,
                                                cognomeNome=cognomeNome,
                                                ruolo=ruolo,
                                                descrizione=descrizione,
                                                recapito=recapito,
                                                tipoRecapito=tipoRecapito,
                                                idCategoria=idCategoria,
#                                                appartenenza=appartenenza,
                                                offset=offset,
                                                batchSize=batchSize)

            self._filterClosure = filterClosure
            cons = self.runFilter()
            self._treeViewModel.clear()
            for c in cons:
                self._treeViewModel.append((c,
                                            (c.cognome or '') + ' ' + (c.nome or ''),
                                            (c.ruolo or ''),
                                            (c.descrizione or ''),
                                            (c.appartenenza or '')))


    def on_filter_radiobutton_toggled(self, widget=None):
        if self.cliente_filter_radiobutton.get_active():
            self.id_cliente_filter_customcombobox.set_sensitive(True)
            self.id_cliente_filter_customcombobox.grab_focus()
            self.id_cliente_filter_customcombobox.set_property("secondary-icon-activatable", True)
            self.id_cliente_filter_customcombobox.set_property("primary-icon-activatable", True)
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            self.id_magazzino_filter_combobox.set_active(0)
            self.id_magazzino_filter_combobox.set_sensitive(False)
            self.schema_azienda_filter_combobox.set_active(0)
            self.schema_azienda_filter_combobox.set_sensitive(False)
#            self.appartenenza_filter_entry.set_sensitive(False)
        elif self.fornitore_filter_radiobutton.get_active():
            self.id_fornitore_filter_customcombobox.set_sensitive(True)
            self.id_fornitore_filter_customcombobox.grab_focus()
            self.id_fornitore_filter_customcombobox.set_property("secondary-icon-activatable", True)
            self.id_fornitore_filter_customcombobox.set_property("primary-icon-activatable", True)
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
            self.id_magazzino_filter_combobox.set_active(0)
            self.id_magazzino_filter_combobox.set_sensitive(False)
            self.schema_azienda_filter_combobox.set_active(0)
            self.schema_azienda_filter_combobox.set_sensitive(False)
#            self.appartenenza_filter_entry.set_sensitive(False)
        elif self.magazzino_filter_radiobutton.get_active():
            self.id_magazzino_filter_combobox.set_sensitive(True)
            self.id_magazzino_filter_combobox.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            self.schema_azienda_filter_combobox.set_active(0)
            self.schema_azienda_filter_combobox.set_sensitive(False)
#            self.appartenenza_filter_entry.set_sensitive(False)
        elif self.azienda_filter_radiobutton.get_active():
            self.schema_azienda_filter_combobox.set_sensitive(True)
            self.schema_azienda_filter_combobox.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            self.id_magazzino_filter_combobox.set_active(0)
            self.id_magazzino_filter_combobox.set_sensitive(False)
#            self.appartenenza_filter_entry.set_sensitive(False)
        elif self.generico_filter_radiobutton.get_active():
#            self.appartenenza_filter_entry.set_sensitive(True)
#            self.appartenenza_filter_entry.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            self.id_magazzino_filter_combobox.set_active(0)
            self.id_magazzino_filter_combobox.set_sensitive(False)
            self.schema_azienda_filter_combobox.set_active(0)
            self.schema_azienda_filter_combobox.set_sensitive(False)
