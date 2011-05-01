# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
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
from AnagraficaSemplice import Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest.dao.Pagamento import Pagamento
from utils import prepareFilterString, obligatoryField


class AnagraficaPagamenti(Anagrafica):
    """ Anagrafica pagamenti """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica pagamenti',
                            '_Pagamenti',
                            AnagraficaPagamentiFilter(self),
                            AnagraficaPagamentiDetail(self))

    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self.anagrafica_treeview

        renderer = gtk.CellRendererText()
        renderer.set_property('editable', False)
        renderer.connect('edited', self.on_column_edited, treeview, False)
        renderer.set_data('column', 0)
        renderer.set_data('max_length', 200)
        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)

        treeview.append_column(column)

        self.lsmodel = gtk.ListStore(str)
        self.lsmodel.append(["cassa"])
        self.lsmodel.append(["banca"])

        cellcombo1= gtk.CellRendererCombo()
        cellcombo1.set_property("editable", True)
        cellcombo1.set_property("visible", True)
        cellcombo1.set_property("text-column", 0)
        cellcombo1.set_property("editable", True)
        cellcombo1.set_property("has-entry", False)
        cellcombo1.set_property("model", self.lsmodel)
        cellcombo1.connect('edited', self.on_column_listinoRiga_edited, treeview, True)

        column = gtk.TreeViewColumn('tipo', cellcombo1, text=2)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(60)

        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str,str)
        treeview.set_model(self._treeViewModel)

        self.refresh()

    def on_column_listinoRiga_edited(self, cell, path, value, treeview, editNext=True):
        model = treeview.get_model()
        model[path][2] = value

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.filter.denominazione_filter_entry.get_text())
        self.numRecords = Pagamento().count(denominazione=denominazione)

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Pagamento().select(denominazione=denominazione,
                                                orderBy=self.orderBy,
                                                offset=self.offset,
                                                batchSize=self.batchSize)

        self._filterClosure = filterClosure

        pags = self.runFilter()

        self._treeViewModel.clear()

        for p in pags:
            self._treeViewModel.append((p,
                                        (p.denominazione or ''),
                                        (p.tipo or '')))


class AnagraficaPagamentiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei pagamenti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_pagamenti_filter_table',
                          gladeFile='_anagrafica_pagamenti_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaPagamentiDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica dei pagamenti """

    def __init__(self, anagrafica):
        AnagraficaDetail.__init__(self,
                          anagrafica,
                          gladeFile='_anagrafica_pagamenti_elements.glade')

    def setDao(self, dao):
        if dao is None:
            self.dao = Pagamento()
            self._anagrafica._newRow((self.dao, '',''))
            self._refresh()
        else:
            self.dao = dao
        return self.dao

    def updateDao(self):
        self.dao = Pagamento().getRecord(id=self.dao.id)
        self._refresh()

    def _refresh(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if not iterator:return
        if not self.dao:return
        model.set_value(iterator, 0, self.dao)
        model.set_value(iterator, 1, self.dao.denominazione)
        model.set_value(iterator, 2, self.dao.tipo)

    def saveDao(self):
        sel = self._anagrafica.anagrafica_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        denominazione = model.get_value(iterator, 1) or ''
        tipo = model.get_value(iterator, 2) or ''
        if denominazione == '' or denominazione == None:
            obligatoryField(self._anagrafica.getTopLevel(),
                                self._anagrafica.anagrafica_treeview,
                                msg="Campo Obbligatorio:Denominazione Pagamento!")
        if model.get_value(iterator, 2)=="" or model.get_value(iterator, 2) == None :
            obligatoryField(self._anagrafica.getTopLevel(),
                            self._anagrafica.anagrafica_treeview,
                            msg="Campo Obbligatorio:Denominazione TIPO Pagamento!")
        self.dao.denominazione = denominazione
        self.dao.tipo = tipo
        self.dao.persist()

    def deleteDao(self):
        self.dao.delete()
