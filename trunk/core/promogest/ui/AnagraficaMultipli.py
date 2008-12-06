# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#!/usr/local/bin/python
# coding: UTF-8

import gtk
import gobject

from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Multiplo
from promogest.dao.Multiplo import Multiplo
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo

from utils import *
from utilsCombobox import fillComboboxUnitaBase, findIdFromCombobox



class AnagraficaMultipli(Anagrafica):
    """ Anagrafica multipli unita di misura """

    def __init__(self, idArticolo = None):
        self._articoloFissato = (idArticolo <> None)
        self._idArticolo = idArticolo
        if self._idArticolo is not None:
            articolo = leggiArticolo(self._idArticolo)
            self._idUnitaBase = articolo["idUnitaBase"]
        else:
            self._idUnitaBase = None
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica unita'' di misura derivate',
                            recordMenuLabel='_Multipli',
                            filterElement=AnagraficaMultipliFilter(self),
                            htmlHandler=AnagraficaMultipliHtml(self),
                            reportHandler=AnagraficaMultipliReport(self),
                            editElement=AnagraficaMultipliEdit(self))


    def on_record_edit_activate(self, widget, path=None, column=None):
        dao = self.filter.getSelectedDao()
        if self._idArticolo is not None and dao.id_unita_base is not None:
            msg = "Il multiplo e' generico !!"
            dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            response = dialog.run()
            dialog.destroy()
            return

        Anagrafica.on_record_edit_activate(self, widget, path, column)



class AnagraficaMultipliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei multipli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_multipli_filter_table',
                                  gladeFile='_anagrafica_multipli_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Descrizione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, 'denominazione_breve')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Moltiplicatore', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, 'moltiplicatore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Unita'' base', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, 'unita_base')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Articolo Associato', renderer, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, 'articolo_associato')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self._anagrafica._idArticolo
        idUnitaBase = None

        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        multiplo = Multiplo(isList=True)
        def filterCountClosure():
            return multiplo.count(denominazione=denominazione,
                                idArticolo=idArticolo,
                                idUnitaBase=idUnitaBase)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return multiplo.select(orderBy=self.orderBy,
                                denominazione=denominazione,
                                idArticolo=idArticolo,
                                idUnitaBase=idUnitaBase,
                                offset=offset,
                                batchSize=batchSize)

        self._filterClosure = filterClosure

        muls = self.runFilter()

        self._treeViewModel.clear()

        for m in muls:
            self._treeViewModel.append((m,
                                        (m.denominazione or ''),
                                        (m.denominazione_breve or ''),
                                        (('%-6.4f') % (m.moltiplicatore or 0)),
                                        (m.unita_base or ''),
                                        (m.articolo or '')))

        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)



class AnagraficaMultipliHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'multiplo',
                                'Informazioni sul multiplo')



class AnagraficaMultipliReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei multipli',
                                  defaultFileName='multipli',
                                  htmlTemplate='multipli',
                                  sxwTemplate='multipli')



class AnagraficaMultipliEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei multipli """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_multipli_detail_table',
                                'Dati multiplo',
                                gladeFile='_anagrafica_multipli_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry


    def draw(self):
        #Popola combobox unita di misura base
        fillComboboxUnitaBase(self.id_unita_base_combobox)
        if self._anagrafica._idUnitaBase is not None:
            self.id_unita_base_combobox.set_sensitive(False)


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Multiplo()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Multiplo().getRecord(id=dao.id)
        self._refresh()


    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.denominazione_breve_entry.set_text(self.dao.denominazione_breve or '')
        moltiplicatore = self.dao.moltiplicatore or 0
        self.moltiplicatore_entry.set_text('%-6.4f' % moltiplicatore)
        findComboboxRowFromId(self.id_unita_base_combobox,
                              self.dao.id_unita_base or self._anagrafica._idUnitaBase)
        if self._anagrafica._idUnitaBase is not None:
            self.id_unita_base_combobox.set_sensitive(False)


    def saveDao(self):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        if (self.denominazione_breve_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_breve_entry)

        if (self.moltiplicatore_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.moltiplicatore_entry)

        if findIdFromCombobox(self.id_unita_base_combobox) is None:
            obligatoryField(self.dialogTopLevel, self.id_unita_base_combobox)

        if self._anagrafica._idArticolo is not None:
            if self.dao.id_unita_base is not None:
                # il multiplo esiste gia' ed e' generico e tale deve restare
                return
            else:
                # e' un multiplo legato all'articolo
                self.dao.id_articolo = self._anagrafica._idArticolo
                self.dao.id_unita_base = None
        else:
            # il multiplo e' generico
            self.dao.id_articolo = None
            self.dao.id_unita_base = findIdFromCombobox(self.id_unita_base_combobox)

        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.denominazione_breve =self.denominazione_breve_entry.get_text()
        self.dao.moltiplicatore = float(self.moltiplicatore_entry.get_text())
        self.dao.persist()
