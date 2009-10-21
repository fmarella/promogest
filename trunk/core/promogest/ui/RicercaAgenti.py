# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Fabrizio Loddo

import gtk
import gobject
from Ricerca import Ricerca, RicercaFilter

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Agente
from promogest.dao.Agente import Agente

from utils import *



class RicercaAgenti(Ricerca):
    """ Ricerca agenti """

    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca Agenti',
                         RicercaAgentiFilter(self))
        #self.ricerca_html.destroy()


    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza

        def refresh():
            self.filter.refresh()
            self.filter.ragione_sociale_filter_entry.grab_focus()
        if "Agenti" in Environment.modulesList:
            from promogest.modules.Agenti.ui.AnagraficaAgenti import AnagraficaAgenti
            anag = AnagraficaAgenti()
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)

            anag.on_record_new_activate(anag.record_new_button)
        else:
            fenceDialog()



class RicercaAgentiFilter(RicercaFilter):
    """ Filtro per la ricerca degli agenti """

    def __init__(self, ricerca):
        RicercaFilter.__init__(self, ricerca,
                               'anagrafica_agenti_filter_table',
                               fileName='Agenti/gui/_anagrafica_agenti_elements.glade',
                            isModule=True)
    def on_filter_treeview_selection_changed(self, treeview):
        pass

    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._ricerca.ricerca_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Codice', renderer,text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ragione Sociale', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'ragione_sociale')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cognome - Nome', renderer,text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'cognome, nome')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita', renderer,text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'localita')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self.ragione_sociale_filter_entry.set_text('')
        self.insegna_filter_entry.set_text('')
        self.cognome_nome_filter_entry.set_text('')
        self.localita_filter_entry.set_text('')
        self.codice_fiscale_filter_entry.set_text('')
        self.partita_iva_filter_entry.set_text('')

        self.clear()

    def clear(self):
        # Annullamento filtro
        self.codice_filter_entry.set_text('')
        self.ragione_sociale_filter_entry.set_text('')
        self.insegna_filter_entry.set_text('')
        self.cognome_nome_filter_entry.set_text('')
        self.localita_filter_entry.set_text('')
        self.codice_fiscale_filter_entry.set_text('')
        self.partita_iva_filter_entry.set_text('')
        self.ragione_sociale_filter_entry.grab_focus()
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        ragioneSociale = prepareFilterString(self.ragione_sociale_filter_entry.get_text())
        insegna = prepareFilterString(self.insegna_filter_entry.get_text())
        cognomeNome = prepareFilterString(self.cognome_nome_filter_entry.get_text())
        localita = prepareFilterString(self.localita_filter_entry.get_text())
        partitaIva = prepareFilterString(self.partita_iva_filter_entry.get_text())
        codiceFiscale = prepareFilterString(self.codice_fiscale_filter_entry.get_text())

        self.numRecords = Agente().count(codice=codice,
                                                ragioneSociale=ragioneSociale,
                                                insegna=insegna,
                                                cognomeNome=cognomeNome,
                                                localita=localita,
                                                partitaIva=partitaIva,
                                                codiceFiscale=codiceFiscale)

        self._refreshPageCount()

        agts = Agente().select(orderBy=self.orderBy,
                                            codice=codice,
                                            ragioneSociale=ragioneSociale,
                                            insegna=insegna,
                                            cognomeNome=cognomeNome,
                                            localita=localita,
                                            partitaIva=partitaIva,
                                            codiceFiscale=codiceFiscale,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        model = gtk.ListStore(object, str, str, str, str)

        for v in agts:
            model.append((v,
                          (v.codice or ''),
                          (v.ragione_sociale or ''),
                          (v.cognome or '') + ' ' + (v.nome or ''),
                          (v.sede_operativa_localita or '')))

        self._ricerca.ricerca_filter_treeview.set_model(model)
