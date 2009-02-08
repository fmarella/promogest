# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Andrea Argiolas <andrea@promotux.it>
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

import gtk
import gobject

from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.AliquotaIva
from promogest.dao.AliquotaIva import AliquotaIva

from utils import *
from utilsCombobox import *


class AnagraficaAliquoteIva(Anagrafica):
    """ Anagrafica aliquote IVA """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica aliquote IVA',
                            recordMenuLabel='_Aliquote IVA',
                            filterElement=AnagraficaAliquoteIvaFilter(self),
                            htmlHandler=AnagraficaAliquoteIvaHtml(self),
                            reportHandler=AnagraficaAliquoteIvaReport(self),
                            editElement=AnagraficaAliquoteIvaEdit(self),
                            aziendaStr=aziendaStr)


class AnagraficaAliquoteIvaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle aliquote IVA """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_aliquote_iva_filter_table',
                                  gladeFile='_anagrafica_aliquote_iva_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Descrizione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione breve', renderer,text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None, 'denominazione_breve'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('%', renderer,text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None, 'percentuale'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        aliquota_iva = AliquotaIva()
        def filterCountClosure():
            return aliquota_iva.count(denominazione=denominazione)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return aliquota_iva.select(denominazione=denominazione,
                                        orderBy=self.orderBy,
                                        offset=offset,
                                        batchSize=batchSize)

        self._filterClosure = filterClosure

        ivas = self.runFilter()

        self._treeViewModel.clear()

        for i in ivas:
            self._treeViewModel.append((i,
                                        (i.denominazione or ''),
                                        (i.denominazione_breve or ''),
                                        (('%5.2f') % (i.percentuale or 0))))



class AnagraficaAliquoteIvaHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'aliquota_iva',
                                'Dettaglio aliquota IVA')



class AnagraficaAliquoteIvaReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle aliquote I.V.A.',
                                  defaultFileName='aliquote_iva',
                                  htmlTemplate='aliquote_iva',
                                  sxwTemplate='aliquote_iva')



class AnagraficaAliquoteIvaEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle aliquote IVA """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_aliquote_iva_detail_table',
                                'Dati aliquota I.V.A.',
                                gladeFile='_anagrafica_aliquote_iva_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry


    def draw(self):
        #Popola combobox tipi aliquote iva
        fillComboboxTipiAliquoteIva(self.id_tipo_combobox)


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = AliquotaIva()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = AliquotaIva().getRecord(id=dao.id)
        self._refresh()


    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.denominazione_breve_entry.set_text(self.dao.denominazione_breve or '')
        percentuale = self.dao.percentuale or 0
        self.percentuale_entry.set_text(('%-5.2f') % percentuale)
        percentuale_detrazione = self.dao.percentuale_detrazione or 0
        self.percentuale_detrazione_entry.set_text(('%-5.2f') % percentuale_detrazione)
        self.descrizione_detrazione_entry.set_text(self.dao.descrizione_detrazione or '')
        findComboboxRowFromId(self.id_tipo_combobox, self.dao.id_tipo)


    def saveDao(self):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        if (self.denominazione_breve_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_breve_entry)

        if (self.percentuale_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.percentuale_entry)

        if (findIdFromCombobox(self.id_tipo_combobox) is None):
            obligatoryField(self.dialogTopLevel, self.id_tipo_combobox)

        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.denominazione_breve = self.denominazione_breve_entry.get_text()
        self.dao.percentuale = float(self.percentuale_entry.get_text())
        self.dao.percentuale_detrazione = float(self.percentuale_detrazione_entry.get_text())
        self.dao.descrizione_detrazione = self.descrizione_detrazione_entry.get_text()
        self.dao.id_tipo = findIdFromCombobox(self.id_tipo_combobox)
        self.dao.persist()
