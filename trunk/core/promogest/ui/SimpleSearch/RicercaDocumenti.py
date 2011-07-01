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

from promogest.ui.gtk_compat import *
from promogest.ui.Ricerca import Ricerca, RicercaFilter
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class RicercaDocumenti(Ricerca):
    """ Ricerca clienti """
    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca documenti',
                         RicercaDocumentiFilter(self))

    def insert(self, toggleButton, returnWindow):
        # Richiamo anagrafica di competenza

        def refresh():
            self.filter.refresh()
#            self.filter.ragione_sociale_filter_entry.grab_focus()

        from promogest.ui.AnagraficaDocumenti import AnagraficaDocumenti
        anag = AnagraficaDocumenti()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)
        anag.on_record_new_activate(anag.record_new_button)


class RicercaDocumentiFilter(RicercaFilter):
    """ Filtro per la ricerca dei clienti """
    def __init__(self, ricerca):
        RicercaFilter.__init__(self, ricerca,
                             'anagrafica_documenti_filter_table',
                               fileName='_ricerca_semplice_documenti.glade')
#        self.ricerca_alignment.destroy()

    def on_filter_treeview_selection_changed(self, treeview):
        pass

    def draw(self):
        # Colonne della Treeview per il filtro
        #treeview = self._ricerca.ricerca_filter_treeview
        # impostazione permanente della selezione multipla dei record in treeview
        #treeselection = treeview.get_selection()

        #rendererSx = gtk.CellRendererText()
        #rendererDx = gtk.CellRendererText()
        #rendererDx.set_property('xalign', 1)

        #column = gtk.TreeViewColumn('Data', rendererSx, text=1, background=10)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, (None, 'data_documento'))
        #column.set_resizable(True)
        #column.set_expand(False)
        #column.set_min_width(100)
        #treeview.append_column(column)

        #column = gtk.TreeViewColumn('Numero', rendererSx, text=2, background=10)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, (TestataDocumento,TestataDocumento.numero))
        #column.set_resizable(True)
        #column.set_expand(False)
        #column.set_min_width(100)
        #treeview.append_column(column)

        #column = gtk.TreeViewColumn('Tipo documento', rendererSx, text=3, background=10)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, (None, 'operazione'))
        #column.set_resizable(True)
        #column.set_expand(False)
        #column.set_min_width(150)
        #treeview.append_column(column)

        #column = gtk.TreeViewColumn('Cliente / Fornitore', rendererSx, text=4, background=10)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
        #column.set_resizable(True)
        #column.set_expand(False)
        #column.set_min_width(250)
        #treeview.append_column(column)

        #column = gtk.TreeViewColumn('Rif. doc. fornitore', rendererSx, text=5, background=10)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(True)
        #column.connect("clicked", self._changeOrderBy, (None, 'protocollo'))
        #column.set_resizable(True)
        #column.set_expand(False)
        #column.set_min_width(100)
        #treeview.append_column(column)

        #column = gtk.TreeViewColumn('Imponibile', rendererDx, text=6, background=10)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
        #column.set_resizable(True)
        #column.set_expand(False)
        #column.set_min_width(100)
        #treeview.append_column(column)

        #column = gtk.TreeViewColumn('Imposta', rendererDx, text=7, background=10)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
        #column.set_resizable(True)
        #column.set_expand(False)
        #column.set_min_width(100)
        #treeview.append_column(column)

        #column = gtk.TreeViewColumn('Totale', rendererDx, text=8, background=10)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
        #column.set_resizable(True)
        #column.set_expand(False)
        #column.set_min_width(100)
        #treeview.append_column(column)

        #column = gtk.TreeViewColumn('Note interne', rendererSx, text=9, background=10)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        #column.set_clickable(False)
        #column.set_resizable(True)
        #column.set_expand(True)
        #column.set_min_width(200)
        #treeview.append_column(column)
        #if posso("PA"):
            #column = gtk.TreeViewColumn('Saldato', rendererSx, text=11, background=10)
            #column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            #column.set_clickable(False)
            #column.set_resizable(True)
            #column.set_expand(True)
            #column.set_min_width(200)
            #treeview.append_column(column)
        #else:
            ##self.stato_documento_filter_combobox.destroy()
            #self.statoDocumento_label.destroy()

        #self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str,str)
        #self._ricerca.ricerca_filter_treeview.set_model(self._treeViewModel)

        fillComboboxOperazioni(self.id_operazione_filter_combobox, 'documento',True)
        self.id_operazione_filter_combobox.set_active(0)
        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)

        self.id_operazione_filter_combobox.set_wrap_width(setconf("Numbers", "combo_column"))
        self.id_magazzino_filter_combobox.set_wrap_width(setconf("Numbers", "combo_column"))

        self.cliente_filter_radiobutton.connect('toggled',
                                                self.on_filter_radiobutton_toggled)
        self.fornitore_filter_radiobutton.connect('toggled',
                                                  self.on_filter_radiobutton_toggled)
        self.cliente_filter_radiobutton.set_active(True)
        self.on_filter_radiobutton_toggled()
        idHandler = self.id_agente_filter_customcombobox.connect('changed',
                                                                 on_combobox_agente_search_clicked)
        self.id_agente_filter_customcombobox.setChangedHandler(idHandler)
        self.clear()

    def clear(self):
        """
        Annullamento filtro
         """
        self.da_data_filter_entry.set_text('01/01/' + Environment.workingYear)
        self.a_data_filter_entry.set_text('')
        self.da_numero_filter_entry.set_text('')
        self.a_numero_filter_entry.set_text('')
        self.protocollo_entry.set_text('')
        self.id_operazione_filter_combobox.set_active(0)
#        if not self._anagrafica._magazzinoFissato:
        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
        self.id_magazzino_filter_combobox.set_active(0)
#        else:
#            findComboboxRowFromId(self.id_magazzino_filter_combobox,
#                                  self._anagrafica._idMagazzino)
        self.id_cliente_filter_customcombobox.set_active(0)
        self.id_fornitore_filter_customcombobox.set_active(0)
        self.id_agente_filter_customcombobox.set_active(0)
        #if posso("PA"):
            #self.stato_documento_filter_combobox.set_active(-1)
        if posso("GN"):
            self.a_data_inizio_noleggio_filter_entry.set_text('')
            self.da_data_inizio_noleggio_filter_entry.set_text('')
            self.a_data_fine_noleggio_filter_entry.set_text('')
            self.da_data_fine_noleggio_filter_entry.set_text('')
        self.id_articolo_filter_customcombobox.set_active(0)
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
        daData = stringToDate(self.da_data_filter_entry.get_text())
        aData = stringToDate(self.a_data_filter_entry.get_text())
        daNumero = prepareFilterString(self.da_numero_filter_entry.get_text())
        aNumero = prepareFilterString(self.a_numero_filter_entry.get_text())
        protocollo = prepareFilterString(self.protocollo_entry.get_text())
        idOperazione = prepareFilterString(findIdFromCombobox(self.id_operazione_filter_combobox))
        idMagazzino = findIdFromCombobox(self.id_magazzino_filter_combobox)
        idCliente = self.id_cliente_filter_customcombobox.getId()
        idFornitore = self.id_fornitore_filter_customcombobox.getId()
        idAgente = self.id_agente_filter_customcombobox._id
        if self.tutto_radio.get_active():
            statoDocumento = None
        elif self.saldato_radio.get_active():
            statoDocumento = bool(True)
        else:
            statoDocumento = bool(False)
        idArticolo = self.id_articolo_filter_customcombobox.getId()
        #genero il dizionario dei filtri
        self.filterDict = {"daNumero":daNumero ,
                            "aNumero":aNumero,
                            "daData":daData,
                            "aData":aData,
                            "daParte":None,
                            "aParte":None,
                            "protocollo":protocollo,
                            "idOperazione":idOperazione,
                            "idMagazzino":idMagazzino,
                            "idCliente":idCliente,
                            "idFornitore":idFornitore,
                            "idAgente":idAgente,
                            "statoDocumento":statoDocumento,
                            "idArticolo":idArticolo}
        if posso("GN"):
            daDataInizioNoleggio = stringToDate(self.da_data_inizio_noleggio_filter_entry.get_text())
            aDataInizioNoleggio = stringToDate(self.a_data_inizio_noleggio_filter_entry.get_text())
            daDataFineNoleggio = stringToDate(self.da_data_fine_noleggio_filter_entry.get_text())
            aDataFineNoleggio = stringToDate(self.a_data_fine_noleggio_filter_entry.get_text())
            self.filterDict.update(daDataInizioNoleggio = daDataInizioNoleggio,
                                    aDataInizioNoleggio = aDataInizioNoleggio,
                                    daDataFineNoleggio = daDataFineNoleggio,
                                    aDataFineNoleggio = aDataFineNoleggio)

        def filterCountClosure():
            return TestataDocumento().count(filterDict = self.filterDict)

        self._filterCountClosure = filterCountClosure
#        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return TestataDocumento().select(orderBy=self.orderBy,
                                                offset=offset,
                                                batchSize=batchSize,
                                                filterDict = self.filterDict)
        self._filterClosure = filterClosure
        #self._allResultForHtml = self.runFilter(offset=None, batchSize=None)
        tdos = self.runFilter()
#        self.xptDaoList = self.runFilter(offset=None, batchSize=None)
        print dir(self), dir(self._ricerca)
        self.filter_listore.clear()
        for t in tdos:
            totali = t.totali
            totaleImponibile = mN(t._totaleImponibileScontato,2) or 0
            totaleImposta = mN(t._totaleImpostaScontata,2) or 0
            totale = mN(t._totaleScontato,2) or 0
            col = None
            if posso("PA") and t.documento_saldato == 1:
                documento_saldato_filter = "Si"
                if t.operazione in Environment.hapag:
                    col = "#CCFFAA"
                else:
                    col = None
            elif posso("PA") and t.documento_saldato == 0:
                documento_saldato_filter = "No"
                if t.operazione in Environment.hapag:
                    col = "#FFD7D7"
                else:
                    col = None
            else:
                documento_saldato_filter = ''
            self.filter_listore.append((t,
                                    dateToString(t.data_documento),
                                    (str(t.numero) or str(0)),
                                    (t.operazione or ''),
                                    (t.intestatario or ''),
                                    (str(t.protocollo) or ''),
                                    str(totaleImponibile),
                                    str(totaleImposta),
                                    str(totale),
                                    (t.note_interne or ''),
                                    col,
                                    (documento_saldato_filter or '')
                                    ))
