# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010,2011 by Promotux
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

import gtk
import gobject
from promogest.ui.Ricerca import Ricerca, RicercaFilter
from promogest.dao.Promemoria import Promemoria
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class RicercaPromemoria(Ricerca):
    """ Ricerca clienti """
    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca Promemoria',
                         RicercaPromemoriaFilter(self))

    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza

        def refresh():
            self.filter.refresh()
#            self.filter.ragione_sociale_filter_entry.grab_focus()

        from promogest.ui.AnagraficaPromemoria import AnagraficaPromemoria
        anag = AnagraficaPromemoria()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)
        anag.on_record_new_activate(anag.record_new_button)


class RicercaPromemoriaFilter(RicercaFilter):
    """ Filtro per la ricerca dei clienti """
    def __init__(self, ricerca):
        RicercaFilter.__init__(self, ricerca,
                             'anagrafica_promemoria_filter_table',
                               fileName='_anagrafica_promemoria_elements.glade')
#        self.ricerca_alignment.destroy()
        self._widgetFirstFocus = self.da_data_inserimento_entry.entry
        self.orderBy = 'data_scadenza'

    def on_filter_treeview_selection_changed(self, treeview):
        pass

    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._ricerca.ricerca_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Data inserimento', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,(None, 'data_inserimento'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data scadenza', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'data_scadenza'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Oggetto', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,(None, 'oggetto'))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Incaricato', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'incaricato'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Autore', renderer, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy,(None ,'autore'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Completato', renderer, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy,(None, 'completato'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Scaduto', renderer, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy,(None, 'scaduto'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('In scadenza', renderer, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, (None,'in_scadenza'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Riferimento', renderer, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
#        column.connect("clicked", self._changeOrderBy, 'riferimento')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)
        treeview.set_search_column(1)
        self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str)
        self._ricerca.ricerca_filter_treeview.set_model(self._treeViewModel)

        self.clear()

    def clear(self):
        """ Annullamento filtro """
        self.da_data_inserimento_entry.set_text('')
        self.a_data_inserimento_entry.set_text('')
        self.da_data_scadenza_entry.set_text('')
        self.a_data_scadenza_entry.set_text('')
        self.oggetto_filter_entry.set_text('')
        fillComboboxIncaricatiPromemoria(self.incaricato_combobox_filter_entry)
        self.incaricato_combobox_filter_entry.set_active(-1)
        self.incaricato_combobox_filter_entry.child.set_text('')
        fillComboboxAutoriPromemoria(self.autore_combobox_filter_entry)
        self.autore_combobox_filter_entry.set_active(-1)
        self.autore_combobox_filter_entry.child.set_text('')
        self.descrizione_filter_entry.set_text('')
        self.annotazione_filter_entry.set_text('')
        self.riferimento_filter_entry.set_text('')
        self.completati_checkbox.set_active(False)
        self.scaduti_checkbox.set_active(False)
        self.in_scadenza_checkbox.set_active(True)
        self.refresh()

    def on_filter_entry_changed(self, text):
        stringa = text.get_text()
        def bobo():
            self.refresh()
        gobject.idle_add(bobo)

    def on_filter_radiobutton_toggled(self, widget=None):
        if self.cliente_filter_radiobutton.get_active():
            self.id_cliente_filter_customcombobox.set_sensitive(True)
            self.id_cliente_filter_customcombobox.grab_focus()
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
        elif self.fornitore_filter_radiobutton.get_active():
            self.id_fornitore_filter_customcombobox.set_sensitive(True)
            self.id_fornitore_filter_customcombobox.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)


    def refresh(self):
        """
        Aggiornamento TreeView
        """
        da_data_inserimento = stringToDateTime(emptyStringToNone(self.da_data_inserimento_entry.get_text()))
        a_data_inserimento = stringToDateTime(emptyStringToNone(self.a_data_inserimento_entry.get_text()))
        da_data_scadenza = stringToDateTime(emptyStringToNone(self.da_data_scadenza_entry.get_text()))
        a_data_scadenza = stringToDateTime(emptyStringToNone(self.a_data_scadenza_entry.get_text()))
        oggetto = prepareFilterString(self.oggetto_entry.get_text())
        incaricato = prepareFilterString(self.incaricato_combobox_filter_entry.get_active_text())
        autore = prepareFilterString(self.autore_combobox_filter_entry.get_active_text())
        descrizione = prepareFilterString(self.descrizione_filter_entry.get_text())
        annotazione = prepareFilterString(self.annotazione_filter_entry.get_text())
        riferimento = prepareFilterString(self.riferimento_filter_entry.get_text())
        completati = self.completati_checkbox.get_active()
        scaduti = self.scaduti_checkbox.get_active()
        in_scadenza = self.in_scadenza_checkbox.get_active()
        def filterCountClosure():
            return Promemoria().count( da_data_inserimento = da_data_inserimento,
                                a_data_inserimento = a_data_inserimento,
                                da_data_scadenza = da_data_scadenza,
                                a_data_scadenza = a_data_scadenza,
                                oggetto = oggetto,
                                incaricato = incaricato,
                                autore = autore,
                                descrizione = descrizione,
                                annotazione = annotazione,
                                riferimento = riferimento,
                                in_scadenza = in_scadenza,
                                scaduto = scaduti,
                                completato = completati)

        self._filterCountClosure = filterCountClosure

#        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Promemoria().select(orderBy=self.orderBy,
                                da_data_inserimento = da_data_inserimento,
                                a_data_inserimento = a_data_inserimento,
                                da_data_scadenza = da_data_scadenza,
                                a_data_scadenza = a_data_scadenza,
                                oggetto = oggetto,
                                incaricato = incaricato,
                                autore = autore,
                                descrizione = descrizione,
                                annotazione = annotazione,
                                riferimento = riferimento,
                                in_scadenza = in_scadenza,
                                scaduto = scaduti,
                                completato = completati,
                                offset = offset,
                                batchSize = batchSize)

        self._filterClosure = filterClosure
        memos = self.runFilter()

        self._treeViewModel.clear()

        for m in memos:
            if m.completato:
                compl = 'Si'
            else:
                compl = 'No'
            if m.scaduto:
                scad = 'Si'
            else:
                scad = 'No'
            if m.in_scadenza:
                in_scad = 'Si'
            else:
                in_scad = 'No'

            self._treeViewModel.append((m,
                                        dateTimeToString(m.data_inserimento),
                                        dateTimeToString(m.data_scadenza),
                                        (m.oggetto or ''),
                                        (m.incaricato or ''),
                                        (m.autore or ''),
                                        compl,
                                        scad,
                                        in_scad,
                                        (m.riferimento or '')))
