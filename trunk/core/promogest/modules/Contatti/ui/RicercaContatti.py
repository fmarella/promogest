# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alessandro Scano <alessandro@promotux.it>

import gtk
import gobject
from promogest.ui.Ricerca import Ricerca, RicercaFilter, RicercaHtml

from promogest import Environment
from promogest.dao.Contatto import Contatto
from promogest.dao.ContattoCliente import ContattoCliente
from promogest.dao.ContattoFornitore import ContattoFornitore
from promogest.dao.ContattoAzienda import ContattoAzienda
from promogest.dao.ContattoMagazzino import ContattoMagazzino

from promogest.ui.utils import *



class RicercaContatti(Ricerca):
    """ Ricerca contatti """

    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca contatti',
                         RicercaContattiFilter(self), RicercaContattiHtml(self))


    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza

        def refresh():
            self.filter.refresh()
            self.filter.cognome_nome_filter_entry.grab_focus()
        if posso("CN"):
            from promogest.modules.Contatti.ui.AnagraficaContatti import AnagraficaContatti
            anag = AnagraficaContatti()
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)

            anag.on_record_new_activate(anag.record_new_button)
        else:
            print "MESSAGGIO DI PAT"


class RicercaContattiFilter(RicercaFilter):
    """ Filtro per la ricerca dei contatti """

    def __init__(self, ricerca):
        RicercaFilter.__init__(self, ricerca,
                               'anagrafica_contatti_filter_table',
                               fileName='Contatti/gui/_anagrafica_contatti_elements.glade',
                                isModule=True)
        self._ownerType = 'generico'
        self._widgetFirstFocus = self.cognome_nome_filter_entry


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._ricerca.ricerca_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Cognome - Nome', renderer,text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'cognome')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ruolo', renderer,text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'ruolo')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer,text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'descrizione')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Relativo a', renderer,text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str, str)
        self._ricerca.ricerca_filter_treeview.set_model(self._treeViewModel)

        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
        fillComboboxAziende(self.schema_azienda_filter_combobox, True)

        if self._ownerType == 'cliente':
            self.cliente_filter_radiobutton.set_active(True)
            self.id_cliente_filter_customcombobox.setId(self._ricerca._ownerKey)
        elif self._ownerType == 'fornitore':
            self.fornitore_filter_radiobutton.set_active(True)
            self.id_fornitore_filter_customcombobox.setId(self._ricerca._ownerKey)
        elif self._ownerType == 'magazzino':
            self.magazzino_filter_radiobutton.set_active(True)
            findComboboxRowFromId(self.id_magazzino_filter_combobox, self._ricerca._ownerKey)
        elif self._ownerType == 'azienda':
            self.azienda_filter_radiobutton.set_active(True)
            findComboboxRowFromId(self.schema_azienda_filter_combobox, self._ricerca._ownerKey)
        else:
            self.generico_filter_radiobutton.set_active(True)

        self.cliente_filter_radiobutton.connect('toggled',
                                                self.on_filter_radiobutton_toggled)
        self.fornitore_filter_radiobutton.connect('toggled',
                                                  self.on_filter_radiobutton_toggled)
        self.magazzino_filter_radiobutton.connect('toggled',
                                                  self.on_filter_radiobutton_toggled)
        self.azienda_filter_radiobutton.connect('toggled',
                                                self.on_filter_radiobutton_toggled)
        self.generico_filter_radiobutton.connect('toggled',
                                                 self.on_filter_radiobutton_toggled)
        self.on_filter_radiobutton_toggled()

        fillComboboxCategorieContatti(self.id_categoria_contatto_filter_combobox, True)
        fillComboboxTipiRecapito(self.tipo_recapito_filter_comboboxentry)

        self.clear()


    def clear(self):
        # Annullamento filtro
        self.id_cliente_filter_customcombobox.set_active(0)
        self.id_fornitore_filter_customcombobox.set_active(0)
        self.id_magazzino_filter_combobox.set_active(0)
        self.schema_azienda_filter_combobox.set_active(0)
        self.appartenenza_filter_entry.set_text('')
        self.cognome_nome_filter_entry.set_text('')
        self.ruolo_filter_entry.set_text('')
        self.descrizione_filter_entry.set_text('')
        self.recapito_filter_entry.set_text('')
        self.tipo_recapito_filter_comboboxentry.child.set_text('')
        fillComboboxCategorieContatti(self.id_categoria_contatto_filter_combobox, True)
        self.id_categoria_contatto_filter_combobox.set_active(0)
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView

        cognomeNome = prepareFilterString(self.cognome_nome_filter_entry.get_text())
        ruolo = prepareFilterString(self.ruolo_filter_entry.get_text())
        descrizione = prepareFilterString(self.descrizione_filter_entry.get_text())
        recapito = prepareFilterString(self.recapito_filter_entry.get_text())
        tipoRecapito = prepareFilterString(self.tipo_recapito_filter_comboboxentry.child.get_text())
        idCategoria = findIdFromCombobox(self.id_categoria_contatto_filter_combobox)

        if self.cliente_filter_radiobutton.get_active():
            idCliente = self.id_cliente_filter_customcombobox.getId()
            self.numRecords = ContattoCliente().count(idCliente=idCliente,
                                           cognomeNome=cognomeNome,
                                           ruolo=ruolo,
                                           descrizione=descrizione,
                                           recapito=recapito,
                                           tipoRecapito=tipoRecapito,
                                           idCategoria=idCategoria)

            self._refreshPageCount()

            cons = ContattoCliente().select(orderBy=self.orderBy,
                                 idCliente=idCliente,
                                 cognomeNome=cognomeNome,
                                 ruolo=ruolo,
                                 descrizione=descrizione,
                                 recapito=recapito,
                                 tipoRecapito=tipoRecapito,
                                 idCategoria=idCategoria,
                                 offset=self.offset,
                                 batchSize=self.batchSize)

        elif self.fornitore_filter_radiobutton.get_active():
            idFornitore = self.id_fornitore_filter_customcombobox.getId()
            self.numRecords = ContattoFornitore().count(idFornitore=idFornitore,
                                           cognomeNome=cognomeNome,
                                           ruolo=ruolo,
                                           descrizione=descrizione,
                                           recapito=recapito,
                                           tipoRecapito=tipoRecapito,
                                           idCategoria=idCategoria)

            self._refreshPageCount()

            cons = ContattoFornitore().select(orderBy=self.orderBy,
                                 idFornitore=idFornitore,
                                 cognomeNome=cognomeNome,
                                 ruolo=ruolo,
                                 descrizione=descrizione,
                                 recapito=recapito,
                                 tipoRecapito=tipoRecapito,
                                 idCategoria=idCategoria,
                                 offset=self.offset,
                                 batchSize=self.batchSize)

        elif self.magazzino_filter_radiobutton.get_active():
            idMagazzino = findIdFromCombobox(self.id_magazzino_filter_combobox)
            self.numRecords = ContattoMagazzino().count(idMagazzino=idMagazzino,
                                           cognomeNome=cognomeNome,
                                           ruolo=ruolo,
                                           descrizione=descrizione,
                                           recapito=recapito,
                                           tipoRecapito=tipoRecapito,
                                           idCategoria=idCategoria)

            self._refreshPageCount()

            cons = ContattoMagazzino().select(orderBy=self.orderBy,
                                 idMagazzino=idMagazzino,
                                 cognomeNome=cognomeNome,
                                 ruolo=ruolo,
                                 descrizione=descrizione,
                                 recapito=recapito,
                                 tipoRecapito=tipoRecapito,
                                 idCategoria=idCategoria,
                                 offset=self.offset,
                                 batchSize=self.batchSize)

        elif self.azienda_filter_radiobutton.get_active():
            schemaAzienda = findIdFromCombobox(self.schema_azienda_filter_combobox)
            self.numRecords = ContattoAzienda().count(schemaAzienda=schemaAzienda,
                                           cognomeNome=cognomeNome,
                                           ruolo=ruolo,
                                           descrizione=descrizione,
                                           recapito=recapito,
                                           tipoRecapito=tipoRecapito,
                                           idCategoria=idCategoria)

            self._refreshPageCount()

            cons = ContattoAzienda().select(orderBy=self.orderBy,
                                 schemaAzienda=schemaAzienda,
                                 cognomeNome=cognomeNome,
                                 ruolo=ruolo,
                                 descrizione=descrizione,
                                 recapito=recapito,
                                 tipoRecapito=tipoRecapito,
                                 idCategoria=idCategoria,
                                 offset=self.offset,
                                 batchSize=self.batchSize)

        else:
            appartenenza = prepareFilterString(self.appartenenza_filter_entry.get_text())
            self.numRecords = Contatto().count(cognomeNome=cognomeNome,
                                           ruolo=ruolo,
                                           descrizione=descrizione,
                                           recapito=recapito,
                                           tipoRecapito=tipoRecapito,
                                           idCategoria=idCategoria,
                                           appartenenza=appartenenza)

            self._refreshPageCount()

            cons = Contatto().select(orderBy=self.orderBy,
                                 cognomeNome=cognomeNome,
                                 ruolo=ruolo,
                                 descrizione=descrizione,
                                 recapito=recapito,
                                 tipoRecapito=tipoRecapito,
                                 idCategoria=idCategoria,
                                 appartenenza=appartenenza,
                                 offset=self.offset,
                                 batchSize=self.batchSize)


        model = gtk.ListStore(object, str, str, str, str)

        for c in cons:
            model.append((c,
                          (c.cognome or '') + ' ' + (c.nome or ''),
                          (c.ruolo or ''),
                          (c.descrizione or ''),
                          (c.appartenenza or '')))

        self._ricerca.ricerca_filter_treeview.set_model(model)


    def on_filter_radiobutton_toggled(self, widget=None):
        if self.cliente_filter_radiobutton.get_active():
            self.id_cliente_filter_customcombobox.set_sensitive(True)
            self.id_cliente_filter_customcombobox.grab_focus()
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            self.id_magazzino_filter_combobox.set_active(0)
            self.id_magazzino_filter_combobox.set_sensitive(False)
            self.schema_azienda_filter_combobox.set_active(0)
            self.schema_azienda_filter_combobox.set_sensitive(False)
            self.appartenenza_filter_entry.set_sensitive(False)
        elif self.fornitore_filter_radiobutton.get_active():
            self.id_fornitore_filter_customcombobox.set_sensitive(True)
            self.id_fornitore_filter_customcombobox.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
            self.id_magazzino_filter_combobox.set_active(0)
            self.id_magazzino_filter_combobox.set_sensitive(False)
            self.schema_azienda_filter_combobox.set_active(0)
            self.schema_azienda_filter_combobox.set_sensitive(False)
            self.appartenenza_filter_entry.set_sensitive(False)
        elif self.magazzino_filter_radiobutton.get_active():
            self.id_magazzino_filter_combobox.set_sensitive(True)
            self.id_magazzino_filter_combobox.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            self.schema_azienda_filter_combobox.set_active(0)
            self.schema_azienda_filter_combobox.set_sensitive(False)
            self.appartenenza_filter_entry.set_sensitive(False)
        elif self.azienda_filter_radiobutton.get_active():
            self.schema_azienda_filter_combobox.set_sensitive(True)
            self.schema_azienda_filter_combobox.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            self.id_magazzino_filter_combobox.set_active(0)
            self.id_magazzino_filter_combobox.set_sensitive(False)
            self.appartenenza_filter_entry.set_sensitive(False)
        elif self.generico_filter_radiobutton.get_active():
            self.appartenenza_filter_entry.set_sensitive(True)
            self.appartenenza_filter_entry.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
            self.id_magazzino_filter_combobox.set_active(0)
            self.id_magazzino_filter_combobox.set_sensitive(False)
            self.schema_azienda_filter_combobox.set_active(0)
            self.schema_azienda_filter_combobox.set_sensitive(False)
class RicercaContattiHtml(RicercaHtml):
    def __init__(self, ricerca):
        RicercaHtml.__init__(self, ricerca, 'contatto',
                                'Informazioni sul contatto')
