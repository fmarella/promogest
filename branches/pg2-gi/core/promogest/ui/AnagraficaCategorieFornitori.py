# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco "m3nt0r3" Meloni  <francesco@promotux.it>


import gtk
import gobject
from AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.dao.CategoriaFornitore import CategoriaFornitore
from utils import *



class AnagraficaCategorieFornitori(Anagrafica):
    """ Anagrafica categorie fornitori """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica categorie fornitori',
                            '_Categorie fornitori',
                            AnagraficaCategorieFornitoriFilter(self),
                            AnagraficaCategorieFornitoriDetail(self))


    def draw(self):
        # Colonne della Treeview per il filtro/modifica
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Descrizione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str)
        treeview.set_model(self._treeViewModel)

        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())
        self.numRecords = CategoriaFornitore().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return CategoriaFornitore().select(denominazione=denominazione,
                                                        orderBy=self.orderBy,
                                                        offset=self.offset,
                                                        batchSize=self.batchSize)

        self._filterClosure = filterClosure

        cats = self.runFilter()

        self._treeViewModel.clear()

        for c in cats:
            self._treeViewModel.append((c,
                                        (c.denominazione or '')))



class AnagraficaCategorieFornitoriFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle categorie fornitori """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_categorie_fornitori_filter_table',
                                  gladeFile='_anagrafica_categorie_fornitori_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()



class AnagraficaCategorieFornitoriDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle categorie fornitori """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                anagrafica,
                                gladeFile='_anagrafica_categorie_fornitori_elements.glade')


    def setDao(self, dao):
        if dao is None:
            self.dao = CategoriaFornitore()
            self._anagrafica._newRow((self.dao, ''))
            self._refresh()
        else:
            self.dao = dao


    def updateDao(self):
        self.dao = CategoriaFornitore().getRecord(id=self.dao.id)
        self._refresh()


    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)


    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        denominazione = model.get_value(iterator, 1) or ''
        if (denominazione == ''):
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        self.dao.denominazione = denominazione
        self.dao.persist()


    def deleteDao(self):
        self.dao.delete()