# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Andrea Argiolas <andrea@promotux.it>
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

import gtk
import gobject

from promogest.ui.AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
#from promogest.dao.Dao import Dao
from promogest.dao.Contatto import Contatto
from promogest.dao.ContattoCliente import ContattoCliente
from promogest.dao.ContattoFornitore import ContattoFornitore
from promogest.dao.ContattoMagazzino import ContattoMagazzino
from promogest.dao.ContattoAzienda import ContattoAzienda
from promogest.dao.RecapitoContatto import RecapitoContatto
from promogest.dao.ContattoCategoriaContatto import ContattoCategoriaContatto

from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *



class AnagraficaContatti(Anagrafica):
    """ Anagrafica contatti """

    def __init__(self, ownerKey=None, ownerType=None, aziendaStr=None):
        self._ownerKey = None
        self._ownerType = None
        if (((ownerType == 'cliente') or (ownerType == 'fornitore') or
             (ownerType == 'magazzino') or (ownerType == 'azienda')) and (ownerKey is not None)):
            self._ownerKey = ownerKey
            self._ownerType = ownerType

        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica contatti',
                            recordMenuLabel='_Contatti',
                            filterElement=AnagraficaContattiFilter(self),
                            htmlHandler=AnagraficaContattiHtml(self),
                            reportHandler=AnagraficaContattiReport(self),
                            editElement=AnagraficaContattiEdit(self),
                            aziendaStr=aziendaStr)



class AnagraficaContattiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei contatti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_contatti_filter_table',
                                  gladeFile='Contatti/gui/_anagrafica_contatti_elements.glade',
                                   module=True )
        self._widgetFirstFocus = self.appartenenza_filter_entry


    def draw(self, cplx=False):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Cognome - Nome', renderer,text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, Contatto.cognome))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(300)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ruolo', renderer,text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, Contatto.ruolo))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer,text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, Contatto.descrizione))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Relativo a', renderer,text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str, str, str, str)
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
        self.appartenenza_filter_entry.set_text('')
        self.cognome_nome_filter_entry.set_text('')
        self.ruolo_filter_entry.set_text('')
        self.descrizione_filter_entry.set_text('')
        self.recapito_filter_entry.set_text('')
        self.tipo_recapito_filter_comboboxentry.child.set_text('')
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
                return ContattoCliente().select(  orderBy=self.orderBy,
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
            appartenenza = prepareFilterString(self.appartenenza_filter_entry.get_text())

            def filterCountClosure():
                return Contatto().count(cognomeNome=cognomeNome,
                                        ruolo=ruolo,
                                        descrizione=descrizione,
                                        recapito=recapito,
                                        tipoRecapito=tipoRecapito,
                                        idCategoria=idCategoria,
                                        appartenenza=appartenenza)

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
                                                appartenenza=appartenenza,
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



class AnagraficaContattiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'contatto',
                                'Informazioni sul contatto')



class AnagraficaContattiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei contatti',
                                  defaultFileName='contatti',
                                  htmlTemplate='contatti',
                                  sxwTemplate='contatti')



class AnagraficaContattiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei contatti """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                  anagrafica,
                                  'anagrafica_contatti_detail_table',
                                  'Dati contatto',
                                  gladeFile='Contatti/gui/_anagrafica_contatti_elements.glade',
                                    module=True)
        self._widgetFirstFocus = self.cognome_entry
        self.dao = Contatto()
        self._tabPressed = False


    def draw(self, cplx=False):
        #Popola combobox categorie contatti
        fillComboboxCategorieContatti(self.id_categoria_contatto_customcombobox.combobox)
        self.id_categoria_contatto_customcombobox.connect('clicked',
                                                          on_id_categoria_contatto_customcombobox_clicked)

        #Elenco categorie
        model = gtk.ListStore(int, str, gtk.gdk.Pixbuf, str)
        self.categorie_treeview.set_model(model)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Categoria', rendererText, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        self.categorie_treeview.append_column(column)

        rendererPixbuf = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', rendererPixbuf, pixbuf=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(20)
        self.categorie_treeview.append_column(column)

        #Elenco recapiti
        model = gtk.ListStore(int, str, str, gtk.gdk.Pixbuf, str)
        self.recapiti_treeview.set_model(model)

        rendererCombo = gtk.CellRendererCombo()
        rendererCombo.set_property('editable', True)
        rendererCombo.connect('edited', self.on_tipo_recapito_edited, self.recapiti_treeview.get_model())
        rendererCombo.set_property('text-column', 0)
        rendererCombo.set_property('has_entry', False)
        rendererCombo.set_property('model', fillModelTipiRecapito())
        rendererCombo.set_property('width', 200)
        rendererCombo.set_data('column', 0)
        column = gtk.TreeViewColumn('Tipo', rendererCombo, text=1)
        column.set_clickable(False)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        self.recapiti_treeview.append_column(column)

        rendererText = gtk.CellRendererText()
        rendererText.set_property('editable', True)
        rendererText.connect('edited', self.on_recapito_edited, self.recapiti_treeview.get_model())
        rendererText.set_data('column', 1)
        column = gtk.TreeViewColumn('Recapito', rendererText, text=2)
        column.set_clickable(False)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(True)
        self.recapiti_treeview.append_column(column)

        rendererPixbuf = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', rendererPixbuf, pixbuf=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        column.set_min_width(20)
        self.recapiti_treeview.append_column(column)

        self.recapiti_treeview.set_search_column(2)

        idHandler = self.appartenenza_customcombobox.connect('changed',
                                                             self.on_appartenenza_customcombobox_changed)
        self.appartenenza_customcombobox.setChangedHandler(idHandler)
        self.appartenenza_customcombobox.refresh(clear=True, filter=False)

        self.cliente_radiobutton.connect('toggled',
                                         self.on_radiobutton_toggled)
        self.fornitore_radiobutton.connect('toggled',
                                           self.on_radiobutton_toggled)
        self.magazzino_radiobutton.connect('toggled',
                                           self.on_radiobutton_toggled)
        self.azienda_radiobutton.connect('toggled',
                                         self.on_radiobutton_toggled)
        self.generico_radiobutton.connect('toggled',
                                          self.on_radiobutton_toggled)
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
                                           gtk.ICON_SIZE_BUTTON)
            model.append((id, categoria, anagPixbuf, 'added'))
        self.categorie_treeview.get_selection().unselect_all()


    def on_categorie_contatti_delete_row_button_clicked(self, widget):
        id = findIdFromCombobox(self.id_categoria_contatto_customcombobox.combobox)
        if id is not None:
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_REMOVE,
                                           gtk.ICON_SIZE_BUTTON)
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
        column = cell.get_data('column')
        model.set_value(iterator, column+1, value)
        if self._tabPressed:
            self._tabPressed = False
        gobject.timeout_add(1, self.recapiti_treeview.set_cursor, path, self.recapiti_treeview.get_column(column+1), True)


    def on_recapito_edited(self, cell, path, value, model):
        iterator = model.get_iter(path)
        column = cell.get_data('column')
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
                                           gtk.ICON_SIZE_BUTTON)
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
                                               gtk.ICON_SIZE_BUTTON)
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
        self._refresh()


    def _refresh(self):
        self.on_radiobutton_toggled()

        if self.dao.tipo_contatto == 'cliente':
            self.appartenenza_customcombobox.refresh(clear=True, filter=False)
            self.cliente_radiobutton.set_active(True)
            insertComboboxSearchCliente(self.appartenenza_customcombobox,
                                        self.dao.id_cliente)
        elif self.dao.tipo_contatto == 'fornitore':
            self.appartenenza_customcombobox.refresh(clear=True, filter=False)
            self.fornitore_radiobutton.set_active(True)
            insertComboboxSearchFornitore(self.appartenenza_customcombobox,
                                          self.dao.id_fornitore)
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
        self.ruolo_comboboxentry.child.set_text(self.dao.ruolo or '')
        self.descrizione_comboboxentry.child.set_text(self.dao.descrizione or '')
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
            else:
                self.appartenenza_customcombobox.set_sensitive(False)
                self.cognome_entry.grab_focus()
            if self.cliente_radiobutton.get_active():
                self.appartenenza_label.set_text('Cliente')
            elif self.fornitore_radiobutton.get_active():
                self.appartenenza_label.set_text('Fornitore')
            elif self.magazzino_radiobutton.get_active():
                self.appartenenza_label.set_text('Magazzino')
            elif self.azienda_radiobutton.get_active():
                self.appartenenza_label.set_text('Azienda')


    def saveDao(self):
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
        self.dao.ruolo = self.ruolo_comboboxentry.child.get_text()
        self.dao.descrizione = self.descrizione_comboboxentry.child.get_text()
        textBuffer = self.note_textview.get_buffer()
        self.dao.note = textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter())
        self.daoid=self.dao.id
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
