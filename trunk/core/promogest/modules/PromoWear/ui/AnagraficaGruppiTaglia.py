# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>


import gtk
import gobject
from promogest.ui.AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.modules.PromoWear.dao.GruppoTaglia
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.ui.utils import *



class AnagraficaGruppiTaglia(Anagrafica):
    """ Anagrafica gruppi taglia """

    def __init__(self):
        Anagrafica.__init__(self, 'Promowear - Anagrafica gruppi taglia',
                            '_GruppiTaglia',
                            AnagraficaGruppoTagliaFilter(self),
                            AnagraficaGruppoTagliaDetail(self))


    def draw(self):
        # Colonne della Treeview per il filtro

        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, True)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Denominazione', renderer, text=1,
                                    sensitive=3)
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
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=2,
                                    sensitive=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione_breve')
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)
        treeview.set_search_column(1)
        # Model: Dao, denominazione, denominazione_breve, sensitive
        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, bool)
        treeview.set_model(self._treeViewModel)

        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())

        self.numRecords = GruppoTaglia().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return GruppoTaglia().select(denominazione=denominazione,
                                                     orderBy = self.orderBy,
                                                     offset = self.offset,
                                                     batchSize = self.batchSize)

        self._filterClosure = filterClosure

        grus = self.runFilter()

        self._treeViewModel.clear()

        for g in grus:
            # Il gruppo taglia 1 (taglia unica) e' read-only
            self._treeViewModel.append((g, g.denominazione, g.denominazione_breve, (g.id != 1)))



class AnagraficaGruppoTagliaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli imballaggi """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_gruppo_taglia_filter_table',
                                  gladeFile='promogest/modules/PromoWear/gui/_anagrafica_gruppo_taglia_elements.glade',
                                  module=True)
        self._widgetFirstFocus = self.denominazione_filter_entry


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()



class AnagraficaGruppoTagliaDetail(AnagraficaDetail):
    """
    Dettaglio dell'anagrafica degli imballaggi
    """
    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                                  anagrafica)

    def setDao(self, dao):
        if dao is None:
            self.dao = GruppoTaglia()
            self._anagrafica._newRow((self.dao, '', '', True))
            self._refresh()
        else:
            self.dao = dao

    def updateDao(self):
        if self.dao is not None:
            self.dao = GruppoTaglia().getRecord(id=self.dao.id)
            self._refresh()
        else:
            raise Exception, 'Update not possible'

    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)
        model.set_value(iterator, 2, self.dao.denominazione_breve)

    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.dao.denominazione = model.get_value(iterator, 1)
        self.dao.denominazione_breve = model.get_value(iterator, 2)
        self.dao.persist()

    def deleteDao(self):
        self.dao.delete()

