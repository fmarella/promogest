# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>


import gtk
from Ricerca import Ricerca, RicercaFilter
from promogest.dao.Vettore import Vettore
from utils import *

class RicercaVettori(Ricerca):
    """ Ricerca vettori """

    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca Vettori',
                         RicercaVettoriFilter(self))

    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza

        def refresh():
            self.filter.refresh()
            self.filter.ragione_sociale_filter_entry.grab_focus()

        from AnagraficaVettori import AnagraficaVettori
        anag = AnagraficaVettori()
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)

        anag.on_record_new_activate(anag.record_new_button)



class RicercaVettoriFilter(RicercaFilter):
    """ Filtro per la ricerca dei vettori """

    def __init__(self, ricerca):
        RicercaFilter.__init__(self, ricerca,
                               'anagrafica_vettori_filter_table',
                               fileName='_anagrafica_vettori_elements.glade')


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._ricerca.ricerca_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Codice', renderer,text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'codice'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ragione Sociale', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'ragione_sociale'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cognome - Nome', renderer,text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'cognome, nome'))
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita', renderer,text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'sede_operativa_localita'))
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

        self.numRecords = Vettore().count(codice=codice,
                                                    ragioneSociale=ragioneSociale,
                                                    insegna=insegna,
                                                    cognomeNome=cognomeNome,
                                                    localita=localita,
                                                    partitaIva=partitaIva,
                                                    codiceFiscale=codiceFiscale)

        self._refreshPageCount()

        vets = Vettore().select(orderBy=self.orderBy,
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

        for v in vets:
            model.append((v,
                          (v.codice or ''),
                          (v.ragione_sociale or ''),
                          (v.cognome or '') + ' ' + (v.nome or ''),
                          (v.sede_operativa_localita or '')))

        self._ricerca.ricerca_filter_treeview.set_model(model)
