# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author:  Andrea Argiolas   <andrea@promotux.it>
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

from promogest.ui.Ricerca import Ricerca, RicercaFilter
from promogest.dao.Cliente import Cliente
from promogest.ui.utils import showAnagraficaRichiamata, fillComboboxCategorieClienti,\
                    prepareFilterString, findIdFromCombobox
from promogest.ui.gtk_compat import *

class RicercaClienti(Ricerca):
    """ Ricerca clienti """
    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca clienti',
                         RicercaClientiFilter(self))
        #self.ricerca_html.destroy()

    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza

        def refresh():
            self.filter.refresh()
            self.filter.ragione_sociale_filter_entry.grab_focus()

        from promogest.ui.AnagraficaClienti import AnagraficaClienti
        anag = AnagraficaClienti()
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)

        anag.on_record_new_activate(anag.record_new_button)


class RicercaClientiFilter(RicercaFilter):
    """ Filtro per la ricerca dei clienti """
    def __init__(self, ricerca):
        RicercaFilter.__init__(self, ricerca,
                             "anagrafica_clienti_filter_vbox",
                               fileName='_ricerca_clienti.glade')
        self.ricerca_avanzata_clienti_filter_vbox.destroy()
        self.ricerca_alignment.destroy()

    def on_filter_treeview_selection_changed(self, treeview):
        pass

    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._ricerca.ricerca_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Codice', renderer,text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ragione Sociale', renderer, text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'ragione_sociale')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cognome - Nome', renderer,text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'cognome, nome')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita', renderer,text=4)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'localita')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        fillComboboxCategorieClienti(self.id_categoria_cliente_filter_combobox, True)

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
        self.id_categoria_cliente_filter_combobox.set_active(0)
        self.ragione_sociale_filter_entry.grab_focus()
        self.refresh()

    def on_filter_entry_changed(self, text):
        stringa = text.get_text()
        def bobo():
            self.refresh()
        gobject.idle_add(bobo)

    def refresh(self):
        # Aggiornamento TreeView
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        ragioneSociale = prepareFilterString(self.ragione_sociale_filter_entry.get_text())
        insegna = prepareFilterString(self.insegna_filter_entry.get_text())
        cognomeNome = prepareFilterString(self.cognome_nome_filter_entry.get_text())
        localita = prepareFilterString(self.localita_filter_entry.get_text())
        partitaIva = prepareFilterString(self.partita_iva_filter_entry.get_text())
        codiceFiscale = prepareFilterString(self.codice_fiscale_filter_entry.get_text())
        idCategoria = findIdFromCombobox(self.id_categoria_cliente_filter_combobox)

        self.numRecords = Cliente().count(codice=codice,
                                                    ragioneSociale=ragioneSociale,
                                                    insegna=insegna,
                                                    cognomeNome=cognomeNome,
                                                    localita=localita,
                                                    partitaIva=partitaIva,
                                                    codiceFiscale=codiceFiscale,
                                                    idCategoria=idCategoria)

        self._refreshPageCount()

        clis = Cliente().select(orderBy=self.orderBy,
                                            codice=codice,
                                            ragioneSociale=ragioneSociale,
                                            insegna=insegna,
                                            cognomeNome=cognomeNome,
                                            localita=localita,
                                            partitaIva=partitaIva,
                                            codiceFiscale=codiceFiscale,
                                            idCategoria=idCategoria,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        model = gtk.ListStore(object, str, str, str, str)

        for c in clis:
            model.append((c,
                          (c.codice or ''),
                          (c.ragione_sociale or ''),
                          (c.cognome or '') + ' ' + (c.nome or ''),
                          (c.sede_operativa_localita or '')))

        self._ricerca.ricerca_filter_treeview.set_model(model)
