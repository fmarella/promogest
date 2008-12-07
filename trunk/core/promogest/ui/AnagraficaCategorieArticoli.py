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

from AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.CategoriaArticolo
from promogest.dao.CategoriaArticolo import CategoriaArticolo

from utils import *



class AnagraficaCategorieArticoli(Anagrafica):
    """ Anagrafica categorie degli articoli """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica categorie articoli',
                            '_Categorie',
                            AnagraficaCategorieArticoliFilter(self),
                            AnagraficaCategorieArticoliDetail(self))


    def draw(self):
        # Colonne della Treeview per il filtro/modifica
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Descrizione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 1)
        renderer.set_data('max_length', 10)
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione_breve')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str)
        treeview.set_model(self._treeViewModel)

        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())
        self.numRecords = CategoriaArticolo().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return CategoriaArticolo().select(denominazione=denominazione,
                                            orderBy=self.orderBy,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        self._filterClosure = filterClosure

        cats = self.runFilter()

        self._treeViewModel.clear()

        for c in cats:
            self._treeViewModel.append((c,
                                        (c.denominazione or ''),
                                        (c.denominazione_breve or '')))



class AnagraficaCategorieArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle categorie articoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_categorie_articoli_filter_table',
                                  gladeFile='_anagrafica_categorie_articoli_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()



class AnagraficaCategorieArticoliDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle categorie articoli """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica,
                                  gladeFile='_anagrafica_categorie_articoli_elements.glade')


    def setDao(self, dao):
        if dao is None:
            self.dao = CategoriaArticolo()
            self._anagrafica._newRow((self.dao, '', ''))
            self._refresh()
        else:
            self.dao = dao


    def updateDao(self):
        self.dao = CategoriaArticolo().getRecord(id=self.dao.id)
        self._refresh()


    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)
        model.set_value(iterator, 2, self.dao.denominazione_breve)


    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        denominazione = model.get_value(iterator, 1) or ''
        denominazioneBreve = model.get_value(iterator, 2) or ''
        if (denominazione == ''):
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        if (denominazioneBreve == ''):
            obligatoryField(self._anagrafica.getTopLevel(), self._anagrafica.anagrafica_treeview)
        self.dao.denominazione = denominazione
        self.dao.denominazione_breve = denominazioneBreve
        self.dao.persist()


    def deleteDao(self):
        self.dao.delete()
