# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Enrico Pintus <enrico@promotux.it>
#         Andrea Argiolas <andrea@promotux.it>
#         Francesco Meloni <francesco@promotux.it>

import gtk
import gobject
from RicercaComplessa import RicercaComplessa
from sqlalchemy import and_, or_, not_
from RicercaComplessa import analyze_treeview_key_press_event
from RicercaComplessa import parseModel, onColumnEdited, columnSelectAll
from RicercaComplessa import optimizeString, insertTreeViewRow, deleteTreeViewRow, clearWhereString

from promogest import Environment
import promogest.dao.Cliente
from promogest.dao.Cliente import Cliente
import promogest.dao.CategoriaCliente
from promogest.dao.CategoriaCliente import CategoriaCliente
import promogest.dao.Pagamento
from promogest.dao.Pagamento import Pagamento
import promogest.dao.Magazzino
from promogest.dao.Magazzino import Magazzino
import promogest.dao.Listino
from promogest.dao.Listino import Listino
import Login
from promogest.ui.GladeWidget import GladeWidget

from utils import prepareFilterString, showAnagraficaRichiamata
from utilsCombobox import fillComboboxCategorieClienti, findIdFromCombobox



class RicercaComplessaClienti(RicercaComplessa):
    """ Ricerca avanzata clienti """

    def __init__(self, ragioneSociale = None, insegna = None,
                 cognomeNome = None, codice = None,
                 localita = None, indirizzo = None,
                 codiceFiscale = None, partitaIva = None,
                 idCategoria = None, idPagamento = None,
                 idMagazzino = None, idListino = None):

        self._ragioneSociale = ragioneSociale
        self._insegna = insegna
        self._cognomeNome = cognomeNome
        self._codice = codice
        self._localita = localita
        self._indirizzo = indirizzo
        self._codiceFiscale = codiceFiscale
        self._partitaIva = partitaIva
        self._idCategoria = idCategoria
        self._idPagamento = idPagamento
        self._idMagazzino = idMagazzino
        self._idListino = idListino

        self._ricerca = RicercaClientiFilter(parentObject=self,
                                             ragioneSociale = ragioneSociale,
                                             insegna = insegna,
                                             cognomeNome = cognomeNome,
                                             codice = codice,
                                             localita = localita,
                                             indirizzo = indirizzo,
                                             codiceFiscale = codiceFiscale,
                                             partitaIva = partitaIva,
                                             idCategoria = idCategoria,
                                             idPagamento = idPagamento,
                                             idMagazzino = idMagazzino,
                                             idListino = idListino)

        RicercaComplessa.__init__(self, 'Promogest - Ricerca clienti',
                                  self._ricerca,
                                    )

        self.ricerca_hpaned = gtk.HPaned()
        self.ricerca_viewport.add(self.ricerca_hpaned)

        # set filter part on the left
        filterElement = self.filter.filter_frame
        filterElement.unparent()
        self.ricerca_hpaned.pack1(filterElement, resize=False, shrink=False)

        # set treeview on the right
        resultElement = self.filter.filter_list_vbox
        resultElement.unparent()
        self.results_vbox = gtk.VBox()
        self.results_vbox.pack_start(resultElement)
        self.ricerca_hpaned.pack2(self.results_vbox, resize=True, shrink=False)

        self.ricerca_hpaned.set_position(360)

        # no detail part below treeview
        self.detail = None
        self.detailTopLevel = None

        # single selection for simple search, no selection for advanced search
        self._fixedSelectionTreeViewType = False

        self.filter.filter_clear_button.connect('clicked', self.on_filter_clear_button_clicked)
        self.filter.filter_search_button.connect('clicked', self.on_filter_search_button_clicked)

        accelGroup = gtk.AccelGroup()
        self.getTopLevel().add_accel_group(accelGroup)
        self.filter.filter_clear_button.add_accelerator('clicked', accelGroup, gtk.keysyms.Escape, 0, gtk.ACCEL_VISIBLE)
        self.filter.filter_search_button.add_accelerator('clicked', accelGroup, gtk.keysyms.F3, 0, gtk.ACCEL_VISIBLE)

        self.draw()

        self.setInitialSearch()


    def draw(self):
        """ Disegna la treeview relativa al risultato del filtraggio """
        treeview = self.filter.resultsElement
        model = gtk.ListStore(object, str, str, str, str, str)
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Codice', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, (None,'codice'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ragione sociale', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy, (None,'ragione_sociale'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cognome e nome', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy,(None, 'cognome'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita\'', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self.filter._changeOrderBy,(None, 'sede_legale_localita'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Partita IVA/Codice fiscale', renderer, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)
        treeview.set_model(model)

    def setInitialSearch(self):
        """ Imposta il tipo di ricerca iniziale """
        # puo' essere ridefinito dalle classi derivate
        self._ricerca.setRicercaSemplice()


    def clear(self):
        """ Re-inizializza i filtri """
        self._ricerca.clear()


    def refresh(self):
        """ Esegue il filtraggio in base ai filtri impostati e aggiorna la treeview """
        self._ricerca.refresh()


    def on_filter_clear_button_clicked(self, button):
        """ Gestisce la pressione del bottone pulisci """
        pass


    def on_filter_search_button_clicked(self, button):
        """ Gestisce la pressione del bottone trova """
        pass


    def insert(self, toggleButton, returnWindow):
        """Richiamo anagrafica di competenza"""

        from AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti()
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, self.refresh)

        anag.on_record_new_activate(anag.record_new_button)


    def on_filter_treeview_cursor_changed(self, treeview):
        """ Rileva la riga attualmente selezionata """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        if iterator is None:
            return

        self.dao = model.get_value(iterator, 0)
        self.refreshDetail()


    def refreshDetail(self):
        """ Aggiornamento della parte di dettaglio """
        # puo' essere ridefinito dalle classi derivate che
        # prevedono un parte di dettaglio
        pass


    def on_filter_treeview_row_activated(self, treeview, path, column):
        """ La finestra viene nascosta perche' una riga e' stata selezionata """
        if self.getTopLevel() in Environment.windowGroup:
            Environment.windowGroup.remove(self.getTopLevel())
        self.getTopLevel().hide()


    def _changeTreeViewSelectionType(self):
        """ Imposta il tipo di selezione di default che si puo' fare sulla treeview """
        if self._fixedSelectionTreeViewType:
            return
        selection = self.filter.resultsElement.get_selection()
        if self._ricerca._tipoRicerca == 'semplice':
            # solo se la ricerca e' semplice si puo' selezionare una riga
            selection.set_mode(gtk.SELECTION_SINGLE)
        else:
            selection.set_mode(gtk.SELECTION_NONE)

    def on_filter_entry_changed(self, text):
        stringa = text.get_text()
        def bobo():
            self.refresh()
        gobject.idle_add(bobo)

    def setTreeViewSelectionType(self, mode=None):
        self._fixedSelectionTreeViewType = True
        if mode is not None:
            if mode in (gtk.SELECTION_SINGLE, gtk.SELECTION_MULTIPLE, gtk.SELECTION_NONE):
                selection = self.filter.resultsElement.get_selection()
                selection.set_mode(mode)


    def getResultsElement(self):
        """ Restituisce il risultato della ricerca se composto da un solo elemento """
        if self._ricerca._tipoRicerca == 'semplice':
            return self.dao
        else:
            selection = self.filter.resultsElement.get_selection()
            selectionMode = selection.get_mode()
            if selectionMode == gtk.SELECTION_SINGLE:
                return self.dao
            elif self._ricerca.resultsCount == 1:
                treeview = self.filter.resultsElement
                model = treeview.get_model()
                self.dao = model[0][0]
                return self.dao
            else:
                return self._ricerca.getClientResult()


    def getResultsCount(self):
        """ Restituisce il numero di clienti selezionati """
        if self._ricerca._tipoRicerca == 'semplice':
            if self.dao is not None:
                return 1
            else:
                return 0
        else:
            selection = self.filter.resultsElement.get_selection()
            selectionMode = selection.get_mode()
            if (selectionMode == gtk.SELECTION_SINGLE):
                if self.dao is not None:
                    return 1
                else:
                    return 0
            else:
                return self._ricerca.resultsCount


    def setSummaryTextBefore(self, value):
        self._ricerca.textBefore = value
        self._ricerca.setRiepilogoCliente()


    def setSummaryTextAfter(self, value):
        self._ricerca.textAfter = value
        self._ricerca.setRiepilogoCliente()



class RicercaClientiFilter(GladeWidget):
    """ Classe che gestisce la tipologia di ricerca clienti """

    def __init__(self, parentObject,
                    ragioneSociale = None,
                    insegna = None,
                    cognomeNome = None,
                    codice = None,
                    localita = None,
                    indirizzo = None,
                    codiceFiscale = None,
                    partitaIva = None,
                    idCategoria=None,
                    idPagamento = None,
                    idMagazzino = None,
                    idListino = None):

        GladeWidget.__init__(self, 'anagrafica_clienti_filter_vbox',
                            fileName='_ricerca_clienti.glade')
        self.root= self.ricerca_semplice_clienti_filter_vbox
        self._ragioneSociale = ragioneSociale
        self._insegna = insegna
        self._cognomeNome = cognomeNome
        self._codice = codice
        self._localita = localita
        self._indirizzo = indirizzo
        self._codiceFiscale = codiceFiscale
        self._partitaIva = partitaIva
        self._idCategoria = idCategoria
        self._idPagamento = idPagamento
        self._idMagazzino = idMagazzino
        self._idListino = idListino

        self._parentObject = parentObject
        self.resultsCount = 0
        self.complexFilter=None
        self.textBefore = None
        self.textAfter = None

        self.draw()

        self.ricerca_avanzata_clienti_button.connect('clicked',
                                                     self.on_ricerca_avanzata_button_clicked)
        self.ricerca_semplice_clienti_button.connect('clicked',
                                                     self.on_ricerca_semplice_button_clicked)


    def on_ricerca_avanzata_button_clicked(self, button):
        """ Seleziona la ricerca avanzata """
        self.setRicercaAvanzata()


    def on_ricerca_semplice_button_clicked(self, button):
        """ Seleziona la ricerca semplice """
        self.setRicercaSemplice()


    def setRicercaSemplice(self):
        """ Gestisce la visualizzazione della sola parte semplice della ricerca """
        self._tipoRicerca = 'semplice'
        self.ricerca_avanzata_clienti_filter_vbox.set_no_show_all(True)
        self.ricerca_avanzata_clienti_filter_vbox.hide()
        self.ricerca_semplice_clienti_filter_vbox.show()
        self.ragione_sociale_filter_entry.grab_focus()
        self._parentObject._changeTreeViewSelectionType()
        self._parentObject.refresh()

    def on_filter_entry_changed(self, text):
        stringa = text.get_text()
        def bobo():
            self.refresh()
        gobject.idle_add(bobo)


    def setRicercaAvanzata(self):
        self._tipoRicerca = 'avanzata'
        self.ricerca_semplice_clienti_filter_vbox.set_no_show_all(True)
        self.ricerca_semplice_clienti_filter_vbox.hide()
        self.ricerca_avanzata_clienti_filter_vbox.show()
        self.ragione_sociale_cliente_filter_expander.grab_focus()
        self._parentObject._changeTreeViewSelectionType()
        self._parentObject.refresh()


    def draw(self):
        """ Disegna e imposta i widgets relativi a tutta la ricerca """
        self.drawRicercaSemplice()
        self.drawRicercaComplessa()


    def drawRicercaSemplice(self):
        """ Disegna e imposta i widgets relativi alla sola parte semplice della ricerca """
        fillComboboxCategorieClienti(self.id_categoria_cliente_filter_combobox, True)

        self.ragione_sociale_filter_entry.set_text(self._ragioneSociale or '')
        self.insegna_filter_entry.set_text(self._insegna or '')
        self.cognome_nome_filter_entry.set_text(self._cognomeNome or '')
        self.codice_filter_entry.set_text(self._codice or '')
        self.localita_filter_entry.set_text(self._localita or '')
        self.codice_fiscale_filter_entry.set_text(self._codiceFiscale or '')
        self.partita_iva_filter_entry.set_text(self._partitaIva or '')
        if self._idCategoria is not None:
            findComboboxowFromId(self.id_categoria_cliente_filter_combobox, self._idFamiglia)

    def drawRicercaComplessa(self):
        """ Disegna e imposta i widgets relativi alla sola parte avanzata della ricerca """
        self.collapseAllExpanders()

        self.drawRagioneSocialeTreeView()
        self.drawInsegnaTreeView()
        self.drawCognomeNomeTreeView()
        self.drawCodiceTreeView()
        self.drawLocalitaTreeView()
        self.drawIndirizzoTreeView()
        self.drawCodiceFiscaleTreeView()
        self.drawPartitaIvaTreeView()
        self.drawCategoriaTreeView()
        self.drawPagamentoTreeView()
        self.drawMagazzinoTreeView()
        self.drawListinoTreeView()

        self._activeExpander = None
        self.setRiepilogoCliente()

    def drawRagioneSocialeTreeView(self):
        treeview = self.ragione_sociale_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._ragioneSocialeTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Ragione sociale', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertRagioneSociale(self._ragioneSociale)

    def drawInsegnaTreeView(self):
        treeview = self.insegna_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._insegnaTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Insegna', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertInsegna(self._insegna)

    def drawCognomeNomeTreeView(self):
        treeview = self.cognome_nome_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._cognomeNomeTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Cognome e nome', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertCognomeNome(self._cognomeNome)

    def drawCodiceTreeView(self):
        treeview = self.codice_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._codiceTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Codice', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertCodice(self._codice)

    def drawLocalitaTreeView(self):
        treeview = self.localita_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._localitaTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Localita\'', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertLocalita(self._localita)

    def drawIndirizzoTreeView(self):
        treeview = self.indirizzo_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._indirizzoTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Indirizzo', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertIndirizzo(self._indirizzo)

    def drawCodiceFiscaleTreeView(self):
        treeview = self.codice_fiscale_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._codiceFiscaleTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Codice fiscale', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertCodiceFiscale(self._codiceFiscale)

    def drawPartitaIvaTreeView(self):
        treeview = self.partita_iva_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, str)
        self._partitaIvaTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 1)
        renderer.set_data('column', 2)
        column = gtk.TreeViewColumn('Escludi', renderer, active=1)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', True)
        renderer.connect('edited', self.onColumnEdited, treeview)
        renderer.set_data('model_index', 2)
        renderer.set_data('column', 3)
        column = gtk.TreeViewColumn('Partita I.V.A.', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(2)

        treeview.set_model(model)
        self.insertPartitaIva(self._partitaIva)

    def drawCategoriaTreeView(self):
        treeview = self.categoria_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str)
        self._categoriaTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(3)

        cats = CategoriaCliente().select(offset=None, batchSize=None)

        for c in cats:
            included = excluded = False
            if self._idCategoria is not None:
                included = self._idCategoria == c.id

            model.append((included,
                          excluded,
                          c.id,
                          c.denominazione))

        treeview.set_model(model)

    def drawPagamentoTreeView(self):
        treeview = self.pagamento_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str)
        self._pagamentoTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(3)

        pags = Pagamento().select(offset=None, batchSize=None)

        for p in pags:
            included = excluded = False
            if self._idPagamento is not None:
                included = self._idPagamento == p.id

            model.append((included,
                          excluded,
                          p.id,
                          p.denominazione))

        treeview.set_model(model)

    def drawMagazzinoTreeView(self):
        treeview = self.magazzino_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str)
        self._magazzinoTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(3)

        mags = Magazzino().select(offset=None, batchSize=None)

        for m in mags:
            included = excluded = False
            if self._idMagazzino is not None:
                included = self._idMagazzino == p.id

            model.append((included,
                          excluded,
                          m.id,
                          m.denominazione))

        treeview.set_model(model)

    def drawListinoTreeView(self):
        treeview = self.listino_cliente_filter_treeview
        treeview.selectAllIncluded = False
        treeview.selectAllExcluded = False
        model = gtk.ListStore(bool, bool, int, str)
        self._listinoTreeViewModel = model

        for c in treeview.get_columns():
            treeview.remove_column(c)

        renderer = gtk.CellRendererToggle()
        renderer.set_property('activatable', True)
        renderer.connect('toggled', self.onColumnEdited, None, treeview)
        renderer.set_data('model_index', 0)
        renderer.set_data('column', 1)
        column = gtk.TreeViewColumn('Includi', renderer, active=0)
        column.connect("clicked", self.columnSelectAll, treeview)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(4)

        liss = Listino().select(offset=None, batchSize=None)

        for l in liss:
            included = excluded = False
            if self._idListino is not None:
                included = self._idListino == l.id

            model.append((included,
                          excluded,
                          l.id,
                          l.denominazione))

        treeview.set_model(model)

    def insertRagioneSociale(self, value=''):
        """ Inserimento nuova ragione_sociale nella treeview """
        insertTreeViewRow(self.ragione_sociale_cliente_filter_treeview, value)

    def deleteRagioneSociale(self):
        """ Eliminazione ragione sociale dalla treeview """
        deleteTreeViewRow(self.ragione_sociale_cliente_filter_treeview)
        self.setRiepilogoCliente()

    def on_nuova_ragione_sociale_cliente_filter_button_clicked(self, button=None):
        self.insertRagioneSociale()

    def on_cancella_ragione_sociale_cliente_filter_button_clicked(self, button=None):
        self.deleteRagioneSociale()
        self.setRiepilogoCliente()

    def insertInsegna(self, value=''):
        """ Inserimento nuova insegna nella treeview """
        insertTreeViewRow(self.insegna_cliente_filter_treeview, value)

    def deleteInsegna(self):
        """ Eliminazione insegna dalla treeview """
        deleteTreeViewRow(self.insegna_cliente_filter_treeview)
        self.setRiepilogoCliente()

    def on_nuova_insegna_cliente_filter_button_clicked(self, button=None):
        self.insertInsegna()

    def on_cancella_insegna_cliente_filter_button_clicked(self, button=None):
        self.deleteInsegna()
        self.setRiepilogoCliente()

    def insertCognomeNome(self, value=''):
        """ Inserimento nuovo cognome-nome nella treeview """
        insertTreeViewRow(self.cognome_nome_cliente_filter_treeview, value)

    def deleteCognomeNome(self):
        """ Eliminazione cognome-nome dalla treeview """
        deleteTreeViewRow(self.cognome_nome_cliente_filter_treeview)
        self.setRiepilogoCliente()

    def on_nuovo_cognome_nome_cliente_filter_button_clicked(self, button=None):
        self.insertCognomeNome()

    def on_cancella_cognome_nome_cliente_filter_button_clicked(self, button=None):
        self.deleteCognomeNome()
        self.setRiepilogoCliente()

    def insertCodice(self, value=''):
        """ Inserimento nuovo codice nella treeview """
        insertTreeViewRow(self.codice_cliente_filter_treeview, value)

    def deleteCodice(self):
        """ Eliminazione codice dalla treeview """
        deleteTreeViewRow(self.codice_cliente_filter_treeview)
        self.setRiepilogoCliente()

    def on_nuovo_codice_cliente_filter_button_clicked(self, button=None):
        self.insertCodice()

    def on_cancella_codice_cliente_filter_button_clicked(self, button=None):
        self.deleteCodice()
        self.setRiepilogoCliente()

    def insertLocalita(self, value=''):
        """ Inserimento nuova localita nella treeview """
        insertTreeViewRow(self.localita_cliente_filter_treeview, value)

    def deleteLocalita(self):
        """ Eliminazione localita dalla treeview """
        deleteTreeViewRow(self.localita_cliente_filter_treeview)
        self.setRiepilogoCliente()

    def on_nuova_localita_cliente_filter_button_clicked(self, button=None):
        self.insertLocalita()

    def on_cancella_localita_cliente_filter_button_clicked(self, button=None):
        self.deleteLocalita()
        self.setRiepilogoCliente()

    def insertIndirizzo(self, value=''):
        """ Inserimento nuovo indirizzo nella treeview """
        insertTreeViewRow(self.indirizzo_cliente_filter_treeview, value)

    def deleteIndirizzo(self):
        """ Eliminazione indirizzo dalla treeview """
        deleteTreeViewRow(self.indirizzo_cliente_filter_treeview)
        self.setRiepilogoCliente()

    def on_nuovo_indirizzo_cliente_filter_button_clicked(self, button=None):
        self.insertIndirizzo()

    def on_cancella_indirizzo_cliente_filter_button_clicked(self, button=None):
        self.deleteIndirizzo()
        self.setRiepilogoCliente()

    def insertCodiceFiscale(self, value=''):
        """ Inserimento nuovo codice fiscale nella treeview """
        insertTreeViewRow(self.codice_fiscale_cliente_filter_treeview, value)

    def deleteCodiceFiscale(self):
        """ Eliminazione codice fiscale dalla treeview """
        deleteTreeViewRow(self.codice_fiscale_cliente_filter_treeview)
        self.setRiepilogoCliente()

    def on_nuovo_codice_fiscale_cliente_filter_button_clicked(self, button=None):
        self.insertCodiceFiscale()

    def on_cancella_codice_fiscale_cliente_filter_button_clicked(self, button=None):
        self.deleteCodiceFiscale()
        self.setRiepilogoCliente()

    def insertPartitaIva(self, value=''):
        """ Inserimento nuova partita iva nella treeview """
        insertTreeViewRow(self.partita_iva_cliente_filter_treeview, value)

    def deletePartitaIva(self):
        """ Eliminazione partita iva dalla treeview """
        deleteTreeViewRow(self.partita_iva_cliente_filter_treeview)
        self.setRiepilogoCliente()

    def on_nuova_partita_iva_cliente_filter_button_clicked(self, button=None):
        self.insertPartitaIva()

    def on_cancella_partita_iva_cliente_filter_button_clicked(self, button=None):
        self.deletePartitaIva()
        self.setRiepilogoCliente()

    def on_ragione_sociale_cliente_filter_treeview_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertRagioneSociale,
                                                self.deleteRagioneSociale,
                                                self.setRiepilogoCliente)


    def on_insegna_cliente_filter_treeview_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertInsegna,
                                                self.deleteInsegna,
                                                self.setRiepilogoCliente)


    def on_cognome_nome_cliente_filter_treeview_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertCognomeNome,
                                                self.deleteCognomeNome,
                                                self.setRiepilogoCliente)


    def on_codice_cliente_filter_treeview_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertCodice,
                                                self.deleteCodice,
                                                self.setRiepilogoCliente)


    def on_localita_cliente_filter_treeview_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertLocalita,
                                                self.deleteLocalita,
                                                self.setRiepilogoCliente)


    def on_indirizzo_cliente_filter_treeview_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertIndirizzo,
                                                self.deleteIndirizzo,
                                                self.setRiepilogoCliente)


    def on_codice_fiscale_cliente_filter_treeview_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertCodiceFiscale,
                                                self.deleteCodiceFiscale,
                                                self.setRiepilogoCliente)


    def on_partita_iva_cliente_filter_treeview_key_press_event(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        return analyze_treeview_key_press_event(widget,
                                                keyname,
                                                self.insertPartitaIva,
                                                self.deletePartitaIva,
                                                self.setRiepilogoCliente)


    def on_ragione_sociale_cliente_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview delle ragioni sociali """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_ragione_sociale_cliente_filter_button.set_property('sensitive', (iterator is not None))


    def on_insegna_cliente_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview delle insegna """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_insegna_cliente_filter_button.set_property('sensitive', (iterator is not None))


    def on_cognome_nome_cliente_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview dei cognomi-nomi """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_cognome_nome_cliente_filter_button.set_property('sensitive', (iterator is not None))


    def on_codice_cliente_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview dei codici """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_codice_cliente_filter_button.set_property('sensitive', (iterator is not None))


    def on_localita_cliente_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview delle localita """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_localita_cliente_filter_button.set_property('sensitive', (iterator is not None))


    def on_indirizzo_cliente_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview degli indirizzi """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_indirizzo_cliente_filter_button.set_property('sensitive', (iterator is not None))


    def on_codice_fiscale_cliente_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview dei codici fiscali """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_codice_fiscale_cliente_filter_button.set_property('sensitive', (iterator is not None))


    def on_partita_iva_cliente_filter_treeview_cursor_changed(self, treeview):
        """ Gestione della selezione di una riga all'interno della treeview delle partite iva """
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()

        self.cancella_partita_iva_cliente_filter_button.set_property('sensitive', (iterator is not None))


    def onColumnEdited(self, cell, path, value, treeview, editNext=False):
        """ Gestione del salvataggio dei valori impostati nelle colonne di una treeview """
        onColumnEdited(cell, path, value, treeview, editNext, self.setRiepilogoCliente)


    def columnSelectAll(self, column, treeview):
        """
        Gestisce la selezione/deselezione alternata delle colonne
        di inclusione/esclusione valori
        """
        columnSelectAll(column, treeview, self.setRiepilogoCliente)


    def getClientResult(self):
        return self.clientResult or None

    def on_any_expander_expanded(self, expander):
        """ Permette ad un solo expander alla volta di essere espanso """
        if self._activeExpander is not None and self._activeExpander != expander:
            self._activeExpander.set_expanded(False)
        self._activeExpander = expander


    def collapseAllExpanders(self):
        """ Chiude tutti gli expander """
        self.ragione_sociale_cliente_filter_expander.set_expanded(False)
        self.insegna_cliente_filter_expander.set_expanded(False)
        self.cognome_nome_cliente_filter_expander.set_expanded(False)
        self.codice_cliente_filter_expander.set_expanded(False)
        self.localita_cliente_filter_expander.set_expanded(False)
        self.indirizzo_cliente_filter_expander.set_expanded(False)
        self.codice_fiscale_cliente_filter_expander.set_expanded(False)
        self.partita_iva_cliente_filter_expander.set_expanded(False)
        self.categoria_cliente_filter_expander.set_expanded(False)
        self.pagamento_cliente_filter_expander.set_expanded(False)
        self.magazzino_cliente_filter_expander.set_expanded(False)
        self.listino_cliente_filter_expander.set_expanded(False)


    def on_campo_filter_entry_key_press_event(self, widget, event):
        """ Conferma parametri filtro x ricerca semplice da tastiera """
        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname == 'Return' or keyname == 'KP_Enter':
            self._parentObject.refresh()


    def setRiepilogoCliente(self):
        """ In base ai filtri impostati costruisce il testo del riepilogo """
        def buildIncludedString(row, index):
            if row[0]:
                self._includedString += '     + ' + row[index] + '\n'

        def buildExcludedString(row, index):
            if row[1]:
                self._excludedString += '     - ' + row[index] + '\n'

        testo = ''

        model = self._ragioneSocialeTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Ragione Sociale:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._insegnaTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Insegna:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._cognomeNomeTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Cognome e Nome:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._codiceTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Codice:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._localitaTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Localita:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._indirizzoTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Indirizzo:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._codiceFiscaleTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Codice fiscale:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._partitaIvaTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 2)
        self._excludedString = ''
        parseModel(model, buildExcludedString, 2)
        if self._includedString != '' or self._excludedString != '':
            testo += '  Partita iva:\n'
        if self._includedString != '':
            testo += self._includedString
        if self._excludedString != '':
            testo += self._excludedString

        model = self._categoriaTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 3)
        if self._includedString != '':
            testo += '  Categoria:\n'
            testo += self._includedString

        model = self._pagamentoTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 3)
        if self._includedString != '':
            testo += '  Pagamento:\n'
            testo += self._includedString

        model = self._magazzinoTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 3)
        if self._includedString != '':
            testo += '  Magazzino:\n'
            testo += self._includedString

        model = self._listinoTreeViewModel
        self._includedString = ''
        parseModel(model, buildIncludedString, 3)
        if self._includedString != '':
            testo += '  Listino:\n'
            testo += self._includedString

        if self.textBefore is not None:
            testo = self.textBefore + testo
        if self.textAfter is not None:
            testo = testo + self.textAfter

        buffer = self.riepilogo_cliente_filter_textview.get_buffer()
        buffer.set_text(testo)
        self.riepilogo_cliente_filter_textview.set_buffer(buffer)


    def getRiepilogoCliente(self):
        """ Restituisce il testo relativo al riepilogo dei filtri impostati """
        # puo' essere richiamato da una classe derivata o proprietaria per costruire
        # dei riepiloghi globali in caso di ricerche su piu' elementi diversi
        if self._tipoRicerca == 'semplice':
            testo = ''

            value = self.ragione_sociale_filter_entry.get_text()
            if value != '':
                testo += '  Ragione sociale:\n'
                testo += '       ' + value + '\n'

            value = self.insegna_filter_entry.get_text()
            if value != '':
                testo += '  Insegna:\n'
                testo += '       ' + value + '\n'

            value = self.cognome_nome_filter_entry.get_text()
            if value != '':
                testo += '  Cognome - nome:\n'
                testo += '       ' + value + '\n'

            value = self.codice_filter_entry.get_text()
            if value != '':
                testo += '  Codice:\n'
                testo += '       ' + value + '\n'

            value = self.localita_filter_entry.get_text()
            if value != '':
                testo += '  Localita\':\n'
                testo += '       ' + value + '\n'

            value = self.codice_fiscale_filter_entry.get_text()
            if value != '':
                testo += '  Codice fiscale:\n'
                testo += '       ' + value + '\n'

            value = self.partita_iva_filter_entry.get_text()
            if value != '':
                testo += '  Partita I.V.A.:\n'
                testo += '       ' + value + '\n'

            if self.id_categoria_cliente_filter_combobox.get_active() != -1:
                value = self.id_categoria_cliente_filter_combobox.get_active_text()
                testo += '  Categoria:\n'
                testo += '       ' + value + '\n'
            print "QUESTO E' IL TESTO DEL RIEPILOGO IN BASSO .....",testo
            return testo
        else:
            buffer = self.riepilogo_cliente_filter_textview.get_buffer()
            return buffer.get_text()


    def clear(self):
        # Annullamento filtro
        if self._tipoRicerca == 'semplice':
            self.drawRicercaSemplice()
        elif self._tipoRicerca == 'avanzata':
            self.drawRicercaComplessa()
        self._parentObject.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        model = self._parentObject.filter.resultsElement.get_model()

        self._prepare()

        if self._tipoRicerca == 'semplice':
            ragioneSociale = prepareFilterString(self.ragione_sociale_filter_entry.get_text())
            insegna = prepareFilterString(self.insegna_filter_entry.get_text())
            cognomeNome = prepareFilterString(self.cognome_nome_filter_entry.get_text())
            codice = prepareFilterString(self.codice_filter_entry.get_text())
            localita = prepareFilterString(self.localita_filter_entry.get_text())
            codiceFiscale = prepareFilterString(self.codice_fiscale_filter_entry.get_text())
            partitaIva = prepareFilterString(self.partita_iva_filter_entry.get_text())
            idCategoria = findIdFromCombobox(self.id_categoria_cliente_filter_combobox)
        elif self._tipoRicerca == 'avanzata':
            # tutti i filtri vengono annullati in modo che nella stored procedure di select
            # venga fatta la join con il risultato della query di filtraggio sui clienti
            ragioneSociale = None
            insegna = None
            cognomeNome = None
            codice = None
            localita = None
            codiceFiscale = None
            partitaIva = None
            idCategoria = None

        self.filter.numRecords = Cliente().count(ragioneSociale = ragioneSociale,
                                                            insegna = insegna,
                                                            cognomeNome = cognomeNome,
                                                            codice = codice,
                                                            localita = localita,
                                                            codiceFiscale = codiceFiscale,
                                                            partitaIva = partitaIva,
                                                            idCategoria = idCategoria,
                                                            complexFilter=self.complexFilter)
        self.resultsCount = self.filter.numRecords
        self.filter._refreshPageCount()

        clis = Cliente().select(
                                            ragioneSociale = ragioneSociale,
                                            insegna = insegna,
                                            cognomeNome = cognomeNome,
                                            codice = codice,
                                            localita = localita,
                                            codiceFiscale = codiceFiscale,
                                            partitaIva = partitaIva,
                                            idCategoria = idCategoria,
                                            offset=self.filter.offset,
                                            batchSize=self.filter.batchSize,
                                            complexFilter=self.complexFilter)
        model.clear()

        for c in clis:
            if c.ragione_sociale:
                pi_cf = (c.partita_iva or '')
            else:
                pi_cf = (c.codice_fiscale or '')
            if c.sede_legale_localita:
                loc = (c.sede_legale_localita or '')
            else:
                loc = (c.sede_operativa_indirizzo or '')
            model.append((c,
                          (c.codice or ''),
                          (c.ragione_sociale or ''),
                          (c.cognome or '') + ' ' + (c.nome or ''),
                          loc,
                          pi_cf))
        self.clientResult = Cliente().select(
                                            ragioneSociale = ragioneSociale,
                                            insegna = insegna,
                                            cognomeNome = cognomeNome,
                                            codice = codice,
                                            localita = localita,
                                            codiceFiscale = codiceFiscale,
                                            partitaIva = partitaIva,
                                            idCategoria = idCategoria,
                                            offset=None,
                                            batchSize=None,
                                            complexFilter=self.complexFilter)

    def _prepare(self):
        """
        Viene costruita ed eseguita la query di filtraggio sui clienti in base
        ai filtri impostati
        """
        stringa= []
        wherestring=[]
        def getRagioniSocialiIn(row, index):
            if row[0]:
                self._ragioniSocialiIn.append(optimizeString(row[index]))

        def getRagioniSocialiOut(row, index):
            if row[1]:
                self._ragioniSocialiOut.append(optimizeString(row[index]))

        def getInsegneIn(row, index):
            if row[0]:
                self._insegneIn.append(optimizeString(row[index]))

        def getInsegneOut(row, index):
            if row[1]:
                self._insegneOut.append(optimizeString(row[index]))

        def getCognomiNomiIn(row, index):
            if row[0]:
                self._cognomiNomiIn.append(optimizeString(row[index]))

        def getCognomiNomiOut(row, index):
            if row[1]:
                self._cognomiNomiOut.append(optimizeString(row[index]))

        def getCodiciIn(row, index):
            if row[0]:
                self._codiciIn.append(optimizeString(row[index]))

        def getCodiciOut(row, index):
            if row[1]:
                self._codiciOut.append(optimizeString(row[index]))

        def getLocalitaIn(row, index):
            if row[0]:
                self._localitaIn.append(row[index])

        def getLocalitaOut(row, index):
            if row[1]:
                self._localitaOut.append(row[index])

        def getIndirizziIn(row, index):
            if row[0]:
                self._indirizziIn.append(row[index])

        def getIndirizziOut(row, index):
            if row[1]:
                self._indirizziOut.append(row[index])

        def getPartiteIvaIn(row, index):
            if row[0]:
                self._partiteIvaIn.append(row[index])

        def getPartiteIvaOut(row, index):
            if row[1]:
                self._partiteIvaOut.append(row[index])

        def getCodiciFiscaliIn(row, index):
            if row[0]:
                self._codiciFiscaliIn.append(optimizeString(row[index]))

        def getCodiciFiscaliOut(row, index):
            if row[1]:
                self._codiciFiscaliOut.append(optimizeString(row[index]))

        def getCategorieIn(row, index):
            if row[0]:
                self._idCategorieIn.append(row[index])

        def getPagamentiIn(row, index):
            if row[0]:
                self._idPagamentiIn.append(row[index])

        def getMagazziniIn(row, index):
            if row[0]:
                self._idMagazziniIn.append(row[index])

        def getListiniIn(row, index):
            if row[0]:
                self._idListiniIn.append(row[index])

        # eliminazione tabella clienti filtrati
        #Tabella volante dei clienti filtrati .....

        self.resultsCount = 0
        if self._tipoRicerca == 'avanzata':
            self._ragioniSocialiIn = []
            self._ragioniSocialiOut = []
            self._insegneIn = []
            self._insegneOut = []
            self._cognomiNomiIn = []
            self._cognomiNomiOut = []
            self._codiciIn = []
            self._codiciOut = []
            self._localitaIn = []
            self._localitaOut  = []
            self._indirizziIn = []
            self._indirizziOut = []
            self._codiciFiscaliIn = []
            self._codiciFiscaliOut = []
            self._partiteIvaIn = []
            self._partiteIvaOut = []
            self._idCategorieIn = []
            self._idPagamentiIn = []
            self._idMagazziniIn = []
            self._idListiniIn = []

            parseModel(self._ragioneSocialeTreeViewModel, getRagioniSocialiIn, 2)
            parseModel(self._ragioneSocialeTreeViewModel, getRagioniSocialiOut, 2)
            parseModel(self._insegnaTreeViewModel, getInsegneIn, 2)
            parseModel(self._insegnaTreeViewModel, getInsegneOut, 2)
            parseModel(self._cognomeNomeTreeViewModel, getCognomiNomiIn, 2)
            parseModel(self._cognomeNomeTreeViewModel, getCognomiNomiOut, 2)
            parseModel(self._codiceTreeViewModel, getCodiciIn, 2)
            parseModel(self._codiceTreeViewModel, getCodiciOut, 2)
            parseModel(self._localitaTreeViewModel, getLocalitaIn, 2)
            parseModel(self._localitaTreeViewModel, getLocalitaOut, 2)
            parseModel(self._indirizzoTreeViewModel, getIndirizziIn, 2)
            parseModel(self._indirizzoTreeViewModel, getIndirizziOut, 2)
            parseModel(self._codiceFiscaleTreeViewModel, getCodiciFiscaliIn, 2)
            parseModel(self._codiceFiscaleTreeViewModel, getCodiciFiscaliOut, 2)
            parseModel(self._partitaIvaTreeViewModel, getPartiteIvaIn, 2)
            parseModel(self._partitaIvaTreeViewModel, getPartiteIvaOut, 2)
            parseModel(self._categoriaTreeViewModel, getCategorieIn, 2)
            parseModel(self._pagamentoTreeViewModel, getPagamentiIn, 2)
            parseModel(self._magazzinoTreeViewModel, getMagazziniIn, 2)
            parseModel(self._listinoTreeViewModel, getListiniIn, 2)


            whereString = ""
            wherestring = []

            if len(self._ragioniSocialiIn) > 0:
                variabili = []
                for stri in self._ragioniSocialiIn:
                    stringa= and_(Cliente.ragione_sociale.ilike("%"+stri+"%"))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)


            if len(self._ragioniSocialiOut) > 0:
                variabili = []
                for stri in self._descrizioniOut:
                    stringa= and_(not_(Cliente.ragione_sociale.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus = and_(*variabili)
                wherestring.append(datus)

            if len(self._insegneIn) > 0:
                variabili = []
                for stri in self._insegneIn:
                    stringa= and_(Cliente.insegna.ilike("%"+stri+"%"))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)


            if len(self._insegneOut) > 0:
                variabili = []
                for stri in self._insegneOut:
                    stringa= and_(not_(Cliente.insegna.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus = and_(*variabili)
                wherestring.append(datus)


            if len(self._cognomiNomiIn) > 0:
                variabili = []
                for stri in self._cognomiNomiIn:
                    stringa= and_(or_(Cliente.cognome.ilike("%"+stri+"%"),Cliente.nome.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._cognomiNomiOut) > 0:
                variabili = []
                for stri in self._cognomiNomiOut:
                    stringa= and_(not_(or_(Cliente.cognome.ilike("%"+stri+"%"),Cliente.nome.ilike("%"+stri+"%"))))
                    variabili.append(stringa)
                datus = and_(*variabili)
                wherestring.append(datus)

            if len(self._codiciIn) > 0:
                variabili = []
                for stri in self._codiciIn:
                    stringa= and_(Cliente.codice.ilike("%"+stri+"%"))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._codiciOut) > 0:
                variabili = []
                for stri in self._codiciOut:
                    stringa= and_(not_(Cliente.codice.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus = and_(*variabili)
                wherestring.append(datus)


            if len(self._localitaIn) > 0:
                variabili = []
                for stri in self._localitaIn:
                    stringa= and_(or_(Cliente.sede_operativa_localita.ilike("%"+stri+"%"),Cliente.sede_legale_localita.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._localitaOut) > 0:
                variabili = []
                for stri in self._localitaOut:
                    stringa= and_(not_(or_(Cliente.sede_operativa_localita.ilike("%"+stri+"%"),Cliente.sede_legale_localita.ilike("%"+stri+"%"))))
                    variabili.append(stringa)
                datus = and_(*variabili)
                wherestring.append(datus)

            if len(self._indirizziIn) > 0:
                variabili = []
                for stri in self._indirizziIn:
                    stringa= and_(or_(Cliente.sede_operativa_indirizzo.ilike("%"+stri+"%"),Cliente.sede_legale_indirizzo.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._indirizziOut) > 0:
                variabili = []
                for stri in self._indirizziOut:
                    stringa= and_(not_(or_(Cliente.sede_operativa_indirizzo.ilike("%"+stri+"%"),Cliente.sede_legale_indirizzo.ilike("%"+stri+"%"))))
                    variabili.append(stringa)
                datus = and_(*variabili)
                wherestring.append(datus)

            if len(self._codiciFiscaliIn) > 0:
                variabili = []
                for stri in self._codiciFiscaliIn:
                    stringa= and_(Cliente.codice_fiscale.ilike("%"+stri+"%"))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._codiciFiscaliOut) > 0:
                variabili = []
                for stri in self._codiciFiscaliOut:
                    stringa= and_(not_(Cliente.codice_fiscale.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus = and_(*variabili)
                wherestring.append(datus)

            if len(self._partiteIvaIn) > 0:
                variabili = []
                for stri in self._partiteIvaIn:
                    stringa= and_(Cliente.partita_iva.ilike("%"+stri+"%"))
                    variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._partiteIvaOut) > 0:
                variabili = []
                for stri in self._partiteIvaOut:
                    stringa= and_(not_(Cliente.partita_iva.ilike("%"+stri+"%")))
                    variabili.append(stringa)
                datus = and_(*variabili)
                wherestring.append(datus)

            #if len(self._idCategorieIn) > 0:
                #joinString += " LEFT OUTER JOIN cliente_categoria_cliente CCC ON C.id = CCC.id_cliente"
                #joinString += " LEFT OUTER JOIN categoria_cliente CC on CC.id = CCC.id_categoria_cliente"

                #if len(self._idCategorieIn) > 0:
                    #condition = ""
                    #for e in self._idCategorieIn:
                        #if condition != "":
                            #condition += " OR "
                        #condition += "CC.id = " + str(e)
                    #if whereString != "":
                        #whereString += " AND "
                    #whereString += "(" + condition + ")"

            if len(self._idPagamentiIn) > 0:
                variabili = []
                for stri in self._idPagamentiIn:
                    quer= Environment.params["session"].query(Pagamento)\
                            .filter(Pagamento.id ==stri).all()
                    for q in quer:
                        stringa= and_(Cliente.id_pagamento == q.id)
                        variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._idMagazziniIn) > 0:
                variabili = []
                for stri in self._idMagazziniIn:
                    quer= Environment.params["session"].query(Magazzino)\
                            .filter(Magazzino.id ==stri).all()
                    for q in quer:
                        stringa= and_(Cliente.id_magazzino == q.id)
                        variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)

            if len(self._idListiniIn) > 0:
                variabili = []
                for stri in self._idListiniIn:
                    quer= Environment.params["session"].query(Listino)\
                            .filter(Listino.id ==stri).all()
                    for q in quer:
                        stringa= and_(Cliente.id_listino == q.id)
                        variabili.append(stringa)
                datus= or_(*variabili)
                wherestring.append(datus)
            self.complexFilter=and_(*wherestring)
        return self.complexFilter