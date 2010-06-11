# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>
# License: GNU GPLv2

import gtk
import gobject

from AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
#from AnagraficaComplessa import AnagraficaEdit
from promogest import Environment
from promogest.dao.Banca import Banca
from promogest.lib.ControlloIBAN import *
from GladeWidget import GladeWidget
from utils import *
from utilsCombobox import *

class AnagraficaBanche(Anagrafica):
    """ Anagrafica banche """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica banche',
                            '_Banche',
                            AnagraficaBancheFilter(self),
                            AnagraficaBancheDetail(self))


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 1)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Agenzia', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'agenzia'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 2)
        renderer.set_data('max_length', 30)
        column = gtk.TreeViewColumn('IBAN', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'iban'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str, str, str)
        treeview.set_model(self._treeViewModel)

        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())
        agenzia = prepareFilterString(self.filter.agenzia_filter_entry.get_text())
        iban = prepareFilterString(self.filter.iban_filter_entry.get_text())
        self.numRecords = Banca().count( denominazione=denominazione,
                                                    agenzia=agenzia,
                                                    iban=iban)
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Banca().select(denominazione=denominazione,
                                            agenzia=agenzia,
                                            iban=iban,
                                            orderBy=self.orderBy,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        self._filterClosure = filterClosure

        bans = self.runFilter()

        self._treeViewModel.clear()

        for b in bans:
            iban = IBAN(b.iban)

            self._treeViewModel.append((b,
                                        (b.denominazione or ''),
                                        (b.agenzia or ''),
                                        (b.iban or '')))

class AnagraficaBancheFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle banche """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_banche_filter_table',
                                  gladeFile='_anagrafica_banche_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.agenzia_filter_entry.set_text('')
        self.iban_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()

class AnagraficaBancheDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle banche """

    def __init__(self, anagrafica):
#        GladeWidget.__init__(self,
#                                  'anagrafica_banche_edit_vbox',
#                                 fileName='_anagrafica_banche_edit.glade')
#        self.show_all()
        pass


    def setDao(self, dao):
        if dao is None:
            if Environment.engine.name =="sqlite" and Banca().count() >= 1:
                fenceDialog()
                return
            else:
                self.dao = Banca()
#                self._anagrafica._newRow((self.dao, '', '', '', '', '', '', ''))
#                self._refresh()
        else:
            self.dao = dao

    def updateDao(self):
        self.dao = Banca().getRecord(id= self.dao.id)
#        self._refresh()

#    def _refresh(self):
#        sel = self._anagrafica.anagrafica_treeview.get_selection()
#        (model, iterator) = sel.get_selected()
#        if self.dao.iban is not None:
#            iban = IBAN(self.dao.iban)
#            model.set_value(iterator, 4, iban.abi or '')
#            model.set_value(iterator, 5, iban.cab or '')
#            model.set_value(iterator, 6, iban.cin or '')
#            model.set_value(iterator, 7, iban.account or '')

#        model.set_value(iterator, 0, self.dao)
#        model.set_value(iterator, 1, self.dao.denominazione)
#        model.set_value(iterator, 2, self.dao.agenzia)
#        model.set_value(iterator, 3, self.dao.iban)

#    def saveDao(self):
#        sel = self._anagrafica.anagrafica_treeview.get_selection()
#        (model, iterator) = sel.get_selected()
#        denominazione = model.get_value(iterator, 1) or ''
#        agenzia = model.get_value(iterator, 2) or ''
#        iban = model.get_value(iterator, 3) or ''
#        if (denominazione == ''):
#            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
#            return
#        elif (iban == ''):
#            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
#            return
#        self.dao.denominazione = denominazione
#        self.dao.agenzia = agenzia
#        iban = IBAN(iban)
#        if iban.iban == -1:
#            model.set_value(iterator, 3, '')
#            return
#        self.dao.iban = iban.iban
#        self.dao.persist()

#    def deleteDao(self):
#        self.dao.delete()
