# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
# Author: Dr astico <zoccolodignu@gmail.com>
# Author: Francesco Meloni <francesco@promotux.it>

from AnagraficaComplessa import AnagraficaFilter
import gtk
from utils import *
from promogest.dao.TestataDocumento import TestataDocumento
import datetime
from utilsCombobox import *
from promogest import Environment

class AnagraficaDocumentiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nei documenti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_documenti_filter_table', 'anagrafica_documenti.glade')
        self._widgetFirstFocus = self.da_data_filter_entry
        self.orderBy = 'id'
        self.xptDaoList = None

    def draw(self):
        """
        Disegna colonne della Treeview per il filtro
        """

        treeview = self._anagrafica.anagrafica_filter_treeview
        # impostazione permanente della selezione multipla dei record in treeview
        treeselection = treeview.get_selection()
        treeselection.set_mode(gtk.SELECTION_MULTIPLE)

        rendererSx = gtk.CellRendererText()
        rendererDx = gtk.CellRendererText()
        rendererDx.set_property('xalign', 1)

        column = gtk.TreeViewColumn('Data', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'data_documento')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Numero', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'numero')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Tipo documento', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'operazione')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(150)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Cliente / Fornitore', rendererSx, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(250)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Rif. doc. fornitore', rendererSx, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'protocollo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Imponibile', rendererDx, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Imposta', rendererDx, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Totale', rendererDx, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Note interne', rendererSx, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)
        if Environment.conf.hasPagamenti == True:
            column = gtk.TreeViewColumn('Saldato', rendererSx, text=10)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
            column.set_clickable(False)
            column.set_resizable(True)
            column.set_expand(True)
            column.set_min_width(200)
            treeview.append_column(column)
        else:
            self.stato_documento_filter_combobox.destroy()
            self.statoDocumento_label.destroy()

        self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        fillComboboxOperazioni(self.id_operazione_filter_combobox, 'documento',True)
        self.id_operazione_filter_combobox.set_active(0)
        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)

        self.id_operazione_filter_combobox.set_wrap_width(Environment.conf.combo_columns)
        self.id_magazzino_filter_combobox.set_wrap_width(Environment.conf.combo_columns)
        #if self._anagrafica._magazzinoFissato:
            #findComboboxRowFromId(self.id_magazzino_filter_combobox,
                                  #self._anagrafica._idMagazzino)
        #else:
            #self.id_magazzino_filter_combobox.set_active(0)
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
        if not self._anagrafica._magazzinoFissato:
            fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
            self.id_magazzino_filter_combobox.set_active(0)
        else:
            findComboboxRowFromId(self.id_magazzino_filter_combobox,
                                  self._anagrafica._idMagazzino)
        self.id_cliente_filter_customcombobox.set_active(0)
        self.id_fornitore_filter_customcombobox.set_active(0)
        self.id_agente_filter_customcombobox.set_active(0)
        if Environment.conf.hasPagamenti == True:
            self.stato_documento_filter_combobox.set_active(-1)
        self.id_articolo_filter_customcombobox.set_active(0)
        self.refresh()


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
        statoDocumento = self.stato_documento_filter_combobox.get_active() or None
        if statoDocumento == -1:
            statoDocumento = None
        idArticolo = self.id_articolo_filter_customcombobox.getId()

        def filterCountClosure():
            return TestataDocumento().count(daNumero=daNumero,
                                            aNumero=aNumero,
                                            daParte=None,
                                            aParte=None,
                                            daData=daData,
                                            aData=aData,
                                            protocollo=protocollo,
                                            idOperazione=idOperazione,
                                            idMagazzino=idMagazzino,
                                            idCliente=idCliente,
                                            idFornitore=idFornitore,
                                            idAgente=idAgente,
                                            statoDocumento=statoDocumento,
                                            idArticolo = idArticolo)

        self._filterCountClosure = filterCountClosure
        self.numRecords = self.countFilterResults()
        self._refreshPageCount()


        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return TestataDocumento().select(orderBy=self.orderBy,
                                                daNumero=daNumero,
                                                aNumero=aNumero,
                                                daParte=None,
                                                aParte=None,
                                                daData=daData,
                                                aData=aData,
                                                protocollo=protocollo,
                                                idOperazione=idOperazione,
                                                idMagazzino=idMagazzino,
                                                idCliente=idCliente,
                                                idFornitore=idFornitore,
                                                idAgente=idAgente,
                                                statoDocumento=statoDocumento,
                                                idArticolo=idArticolo,
                                                offset=offset,
                                                batchSize=batchSize)

        self._filterClosure = filterClosure
        tdos = self.runFilter()
        self.xptDaoList = self.runFilter(offset=None, batchSize=None)
        self._treeViewModel.clear()

        for t in tdos:
            if Environment.totaliDict.has_key(t):
                totali = Environment.totaliDict[t]
            else:
                Environment.totaliDict[t] = t.totali
                totali = t.totali
            totaleImponibile = mN(t._totaleImponibileScontato,2) or 0
            totaleImposta = mN(t._totaleImpostaScontata,2) or 0
            totale = mN(t._totaleScontato,2) or 0

            if Environment.conf.hasPagamenti == True and t.documento_saldato == 1:
                documento_saldato_filter = "Si"
            elif Environment.conf.hasPagamenti == True and t.documento_saldato == 0:
                documento_saldato_filter = "No"
            else:
                documento_saldato_filter = ''

            self._treeViewModel.append((t,
                                    dateToString(t.data_documento),
                                    (t.numero or 0),
                                    (t.operazione or ''),
                                    (t.intestatario or ''),
                                    (t.protocollo or ''),
                                    totaleImponibile,
                                    totaleImposta,
                                    totale,
                                    (t.note_interne or ''),
                                    (documento_saldato_filter or '')
                                    ))

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

