# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author: vete <info@promotux.it>

import gtk
import gobject

from promogest.ui.AnagraficaComplessa import Anagrafica, AnagraficaEdit,AnagraficaHtml, AnagraficaFilter, AnagraficaReport

from promogest import Environment
from promogest.dao.Articolo import Articolo
from promogest.modules.SchedaLavorazione.dao.AssociazioneArticoli import AssociazioneArticoli
from promogest.ui.utils import *

class AnagraficaAssociazioniArticoli(Anagrafica):
    """
    Visualizza le associazioni articoli
    """
    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica associazioni articoli',
                            recordMenuLabel='_Associazioni articoli',
                            filterElement=AnagraficaAssociazioniArticoliFilter(self),
                            htmlHandler=AnagraficaAssociazioniArticoliHtml(self),
                            reportHandler=AnagraficaAssociazioniArticoliReport(self),
                            editElement=AnagraficaAssociazioniArticoliEdit(self),
                            aziendaStr=aziendaStr)
        self.record_duplicate_menu.set_property('visible', True)
        

class AnagraficaAssociazioniArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle associazioni articoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_associazioni_articoli_filter_table', \
                                  gladeFile='SchedaLavorazione/gui/schedalavorazione_plugins.glade', \
                                  module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.articoliprincipaliList = []

    def draw(self):
        treeview = self._anagrafica.anagrafica_filter_treeview

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Codice', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Produttore', renderer, text=4, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'produttore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice a barre', renderer, text=5, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice_a_barre')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', renderer, text=6, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice_articolo_fornitore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Famiglia', renderer, text=7, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione_famiglia')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Categoria', renderer, text=8, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione_categoria')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(2)

        self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.clear()


    def _refresh_filter_comboboxes(self, widget=None):
        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.codice_filter_entry.set_text('')
        self.codice_a_barre_filter_entry.set_text('')
        self.codice_articolo_fornitore_filter_entry.set_text('')
        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_filter_combobox, filter=True)
        fillComboboxCategorieArticoli(self.id_categoria_articolo_filter_combobox, True)
        fillComboboxStatiArticoli(self.id_stato_articolo_filter_combobox, True)
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        self.id_categoria_articolo_filter_combobox.set_active(0)
        self.id_stato_articolo_filter_combobox.set_active(0)
        self.cancellato_filter_checkbutton.set_active(False)
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        produttore = prepareFilterString(self.produttore_filter_entry.get_text())
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        codiceABarre = prepareFilterString(self.codice_a_barre_filter_entry.get_text())
        codiceArticoloFornitore = prepareFilterString(self.codice_articolo_fornitore_filter_entry.get_text())
        idFamiglia = findIdFromCombobox(self.id_famiglia_articolo_filter_combobox)
        idCategoria = findIdFromCombobox(self.id_categoria_articolo_filter_combobox)
        idStato = findIdFromCombobox(self.id_stato_articolo_filter_combobox)
        if self.cancellato_filter_checkbutton.get_active():
            cancellato = None
        else:
            cancellato = False

        def filterCountClosure():
            return AssociazioneArticoli().count(denominazione=denominazione,
                                                codice=codice,
                                                codiceABarre=codiceABarre,
                                                codiceArticoloFornitore=codiceArticoloFornitore,
                                                produttore=produttore,
                                                idFamiglia=idFamiglia,
                                                idCategoria=idCategoria,
                                                idStato=idStato,
                                                cancellato=cancellato)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return AssociazioneArticoli().select(nodo=True,
                                                 orderBy=self.orderBy,
                                                 denominazione=denominazione,
                                                 codice=codice,
                                                 codiceABarre=codiceABarre,
                                                 codiceArticoloFornitore=codiceArticoloFornitore,
                                                 produttore=produttore,
                                                 idFamiglia=idFamiglia,
                                                 idCategoria=idCategoria,
                                                 idStato=idStato,
                                                 cancellato=cancellato,
                                                 offset=offset,
                                                 batchSize=batchSize)

        self._filterClosure = filterClosure

        arts = self.runFilter()

        self._treeViewModel.clear()

        for a in arts:
            col = None
            if a.cancellato:
                col = 'red'
            self._treeViewModel.append((a,
                                        col,
                                        (a.codice or ''),
                                        (a.denominazione or ''),
                                        (a.produttore or ''),
                                        (a.codice_a_barre or ''),
                                        (a.codice_articolo_fornitore or ''),
                                        (a.denominazione_famiglia or ''),
                                        (a.denominazione_categoria or '')))



class AnagraficaAssociazioniArticoliHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'associazione_articoli',
                                'Dettaglio associazione articoli')
    

class AnagraficaAssociazioniArticoliReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco Associazioni articoli',
                                  defaultFileName='associazioni_articoli',
                                  htmlTemplate='associazioni_articoli',
                                  sxwTemplate='associazioni_articoli')

class AnagraficaAssociazioniArticoliEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica degli articoli """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_associazioni_articoli_detail_vbox',
                                'Dati articolo',\
                                gladeFile='SchedaLavorazione/gui/schedalavorazione_plugins.glade', \
                                module=True)
        self._widgetFirstFocus = self.articolo_principale_button
        self.remove_article_button.set_sensitive(False)
        self._loading= False
        self.articoliAssociatiList = []

    def draw(self):
        treeview = self.articoli_associati_treeview

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Codice', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(300)
        treeview.append_column(column)
        
        treeview.set_search_column(2)
        self._assTreeViewModel = gtk.ListStore(object, str, str, str,)
        self.articoli_associati_treeview.set_model(self._assTreeViewModel)
        self.articoli_associati_treeview.set_rules_hint(True)
        self.articoli_associati_treeview.set_reorderable(True)
        
        
    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.daoPadre = Articolo()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.daoPadre = Articolo().getRecord(id=dao.id_articolo)
            associatedArts = AssociazioneArticoli().select(nodo=False,
                                                            idPadre=self.daoPadre.id,
                                                            offset=None,
                                                            batchSize=None)
            self.articoliAssociatiList=[]
            for ass in associatedArts:
                self.articoliAssociatiList.append(ass)
        self._refresh(get_order=False)

    def _refresh(self, get_order=True):
        if get_order:
            self._getOrder()
        self._loading = True
        self.descrizione_label.set_text('')
        self.codice_label.set_text('')
        self._assTreeviewModel = self.articoli_associati_treeview.get_model()
        self._assTreeViewModel.clear()

        for articolo in self.articoliAssociatiList:
            col = None
            if articolo.cancellato:
                col = 'red'
            self._assTreeViewModel.append((articolo,
                                        col,
                                        (articolo.codice or ''),
                                        (articolo.denominazione or ''),))

        if self.daoPadre.id is None:
            string='Selezionare un articolo principale'
            self.descrizione_label.set_use_markup(True)
            self.descrizione_label.set_text(string)
        else:
            self.descrizione_label.set_text(self.daoPadre.denominazione or '')
        
        if self.daoPadre.codice is not None:
            self.codice_label.set_use_markup(True)
            self.codice_label.set_text(str(self.daoPadre.codice))

    def _getOrder(self):
        model = self.articoli_associati_treeview.get_model()
        self.articoliAssociatiList = []
        for row in model:
            self.articoliAssociatiList.append(row[0])

    def on_add_article_button_clicked(self, button):
        self.ricercaArticolo()

    def saveDao(self):
        """
        salva tutte le associazioni di articoli nel database
        """
        index = 0
        for articolo in self.articoliAssociatiList:
            articolo.posizione = index
            articolo.persist(Environment.connection)
            index += 1
    
    def on_articolo_principale_button_clicked(self, button):
        self.ricercaArticolo(isNode=True)

    def ricercaArticolo(self, isNode= False):

        def on_ricerca_articolo_hide(anagWindow, anag, isNode=False):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            if isNode:
                self.mostraArticoloPadre(anag.dao.id)
            else:
                self.mostraArticoloFiglio(anag.dao)
        
        codice = None
        codiceABarre = None
        denominazione = None
        codiceArticoloFornitore = None

        from promogest.ui.RicercaComplessaArticoli import RicercaComplessaArticoli
        anag = RicercaComplessaArticoli(denominazione=denominazione,
                                        codice=codice,
                                        codiceABarre=codiceABarre,
                                        codiceArticoloFornitore=codiceArticoloFornitore)
        anag.setTreeViewSelectionType(gtk.SELECTION_SINGLE)

        anagWindow = anag.getTopLevel()
        anagWindow.connect("hide",
                           on_ricerca_articolo_hide,
                           anag, isNode)
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()


    def mostraArticoloPadre(self, id):
        self.daoPadre = Articolo().getRecord(id=id)
        for articolo in self.articoliAssociatiList:
            articolo.id_associato = id
        self._refresh()
        
    def mostraArticoloFiglio(self,dao):
        daoAssociazione= AssociazioneArticoli()
        # qui è sufficiente settare solo le proprietà dell'associazione che vengono poi visualizzate nella treeview
        # nel salvataggio dellla stessa sono necessari solo id_articolo, e id_associato
        if len(self.articoliAssociatiList) > 0:
            pos = len(self.articoliAssociatiList)
        else:
            pos = 0
        daoAssociazione.id_articolo = dao.id
        daoAssociazione.id_associato = self.daoPadre.id
        daoAssociazione.posizione = pos
        daoAssociazione.denominazione = dao.denominazione
        daoAssociazione.codice = dao.codice
        self.articoliAssociatiList.append(daoAssociazione)
        self._refresh(get_order=False)

    def on_remove_article_button_clicked(self, button):
        (model,iter) = self.articoli_associati_treeview.get_selection().get_selected()
        for dao in self.articoliAssociatiList:
            if model[iter][0] == dao:
                self.articoliAssociatiList.remove(dao)
                if dao.id is not None:
                    dao.delete(son=True)
        model.remove(iter)

    def on_articoli_associati_treeview_row_activated(self, widget):
        self.remove_article_button.set_sensitive(True)