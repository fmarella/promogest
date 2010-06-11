# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>


import gtk
import gobject
from Ricerca import Ricerca, RicercaFilter

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo

from utils import *



class RicercaArticoli(Ricerca):
    """ Ricerca articoli """

    def __init__(self, denominazione = None, codice = None, codiceABarre = None,
                  codiceArticoloFornitore = None, produttore = None,
                  idFamiglia = None, idCategoria = None, idStato = None, cancellato = False):
        self._denominazione = denominazione
        self._codice = codice
        self._codiceABarre = codiceABarre
        self._codiceArticoloFornitore = codiceArticoloFornitore
        self._produttore = produttore
        self._idFamiglia = idFamiglia
        self._idCategoria = idCategoria
        self._idStato = idStato
        self._cancellato = cancellato
        #self.ricerca_html.destroy()
        Ricerca.__init__(self, 'Promogest - Ricerca articoli',
                         RicercaArticoliFilter(self))


    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza

        def refresh():
            self.filter.refresh()
            self.filter.denominazione_filter_entry.grab_focus()

        from AnagraficaArticoli import AnagraficaArticoli
        anag = AnagraficaArticoli()
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)

        anag.on_record_new_activate(anag.record_new_button)



class RicercaArticoliFilter(RicercaFilter):
    """ Filtro per la ricerca degli articoli """

    def __init__(self, ricerca):
        RicercaFilter.__init__(self, ricerca,
                               'anagrafica_articoli_filter_table',
                               fileName='_anagrafica_articoli_elements.glade')


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._ricerca.ricerca_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Codice', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'codice'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'denominazione'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Produttore', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'produttore')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice a barre', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice_a_barre')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', renderer, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice_articolo_fornitore')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_filter_combobox, filter=True)
        fillComboboxCategorieArticoli(self.id_categoria_articolo_filter_combobox, True)
        fillComboboxStatiArticoli(self.id_stato_articolo_filter_combobox, True)

        self.denominazione_filter_entry.set_text('')
        self.produttore_filter_entry.set_text('')
        self.codice_filter_entry.set_text('')
        self.codice_a_barre_filter_entry.set_text('')
        self.codice_articolo_fornitore_filter_entry.set_text('')
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        self.id_categoria_articolo_filter_combobox.set_active(0)
        self.id_stato_articolo_filter_combobox.set_active(0)
        self.cancellato_filter_label.set_property('visible', False)
        self.cancellato_filter_label.set_no_show_all(True)
        self.cancellato_filter_checkbutton.set_property('visible', False)
        self.cancellato_filter_checkbutton.set_no_show_all(True)

        self.denominazione_filter_entry.set_text(self._ricerca._denominazione or '')
        self.produttore_filter_entry.set_text(self._ricerca._produttore or '')
        self.codice_filter_entry.set_text(self._ricerca._codice or '')
        self.codice_a_barre_filter_entry.set_text(self._ricerca._codiceABarre or '')
        self.codice_articolo_fornitore_filter_entry.set_text(self._ricerca._codiceArticoloFornitore or '')

        if self._ricerca._idFamiglia is not None:
            findComboboxRowFromId(self.id_famiglia_articolo_filter_combobox, self._ricerca._idFamiglia)
        if self._ricerca._idCategoria is not None:
            findComboboxRowFromId(self.id_categoria_articolo_filter_combobox, self._ricerca._idCategoria)
        if self._ricerca._idStato is not None:
            findComboboxRowFromId(self.id_stato_articolo_filter_combobox, self._ricerca._idStato)
        self.denominazione_filter_entry.grab_focus()
        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.produttore_filter_entry.set_text('')
        self.codice_filter_entry.set_text('')
        self.codice_a_barre_filter_entry.set_text('')
        self.codice_articolo_fornitore_filter_entry.set_text('')
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        self.id_categoria_articolo_filter_combobox.set_active(0)
        self.id_stato_articolo_filter_combobox.set_active(0)
        self.denominazione_filter_entry.grab_focus()
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
            cancellato = False
        else:
            cancellato = True
        print " MA INSOMMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", cancellato
        self.numRecords = Articolo().count(denominazione=denominazione,
                                                       codice=codice,
                                                       codiceABarre=codiceABarre,
                                                       codiceArticoloFornitore=codiceArticoloFornitore,
                                                       produttore=produttore,
                                                       idFamiglia=idFamiglia,
                                                       idCategoria=idCategoria,
                                                       idStato=idStato,
                                                       cancellato=cancellato)

        self._refreshPageCount()

        arts = Articolo().select(orderBy=self.orderBy,
                                             denominazione=denominazione,
                                             codice=codice,
                                             codiceABarre=codiceABarre,
                                             codiceArticoloFornitore=codiceArticoloFornitore,
                                             produttore=produttore,
                                             idFamiglia=idFamiglia,
                                             idCategoria=idCategoria,
                                             idStato=idStato,
                                             cancellato=cancellato,
                                             offset=self.offset,
                                             batchSize=self.batchSize)

        model = gtk.ListStore(object, str, str, str, str, str)

        for a in arts:
            model.append((a,
                          (a.codice or ''),
                          (a.denominazione or ''),
                          (a.produttore or ''),
                          (a.codice_a_barre or ''),
                          (a.codice_articolo_fornitore or '')))

        self._ricerca.ricerca_filter_treeview.set_model(model)
