
# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
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

import gtk
import gobject

from AnagraficaComplessa import Anagrafica, AnagraficaEdit,AnagraficaHtml, AnagraficaFilter, AnagraficaReport

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo
import promogest.dao.DistintaBase
from promogest.dao.DistintaBase import DistintaBase

from utils import *

class AnagraficaDistintaBase(Anagrafica):
    """
    Visualizza le distinte base
    """
    def __init__(self, aziendaStr):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica distinte base',
                            recordMenuLabel='_Distinta Base',
                            filterElement=AnagraficaDistintaBaseFilter(self),
                            htmlHandler=AnagraficaDistintaBaseHtml(self),
                            reportHandler=AnagraficaDistintaBaseReport(self),
                            editElement=AnagraficaDistintaBaseEdit(self),
                            companyName=aziendaStr)
        self.record_duplicate_menu.set_property('visible', True)
        

class AnagraficaDistintaBaseFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle distinte base """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_distinta_base_filter_table', gladeFile='distinta_base_plugins.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.articoliprincipaliList = []

    def draw(self):
        treeview = self._anagrafica.anagrafica_filter_treeview

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Codice', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Descrizione', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Produttore', renderer, text=4, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'produttore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice a barre', renderer, text=5, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice_a_barre')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo fornitore', renderer, text=6, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice_articolo_fornitore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Famiglia', renderer, text=7, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione_famiglia')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Categoria', renderer, text=8, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione_categoria')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(2)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str, str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.clear()


    def _refresh_filter_comboboxes(self, widget=None):
        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.codice_filter_entry.set_text('')
        self.codice_a_barre_filter_entry.set_text('')
        self.codice_articolo_fornitore_filter_entry.set_text('')
        fillComboboxFamiglieArticoli(self.id_famiglia_articolo_filter_combobox, filter=True)
        fillComboboxCategorieArticoli(self.id_categoria_articolo_filter_combobox, True)
        fillComboboxStatiArticoli(self.id_stato_articolo_filter_combobox, True)
        self.id_famiglia_articolo_filter_combobox.set_active(0)
        self.id_categoria_articolo_filter_combobox.set_active(0)
        self.id_stato_articolo_filter_combobox.set_active(0)
        self.cancellato_filter_checkbutton.set_active(False)
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        produttore = prepareFilterString(self.produttore_filter_entry.get_text())
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        codiceABarre = prepareFilterString(self.codice_a_barre_filter_entry.get_text())
        codiceArticoloFornitore = prepareFilterString(self.codice_articolo_fornitore_filter_entry.get_text())
        idFamiglia = findIdFromCombobox(self.id_famiglia_articolo_filter_combobox)
        idCategoria = findIdFromCombobox(self.id_categoria_articolo_filter_combobox)
        idStato = findIdFromCombobox(self.id_stato_articolo_filter_combobox)
        if self.cancellato_filter_checkbutton.get_active():
            cancellato = None
        else:
            cancellato = False

        def filterCountClosure():
            return promogest.dao.DistintaBase.count(Environment.connection,
                                                denominazione=denominazione,
                                                codice=codice,
                                                codiceABarre=codiceABarre,
                                                codiceArticoloFornitore=codiceArticoloFornitore,
                                                produttore=produttore,
                                                idFamiglia=idFamiglia,
                                                idCategoria=idCategoria,
                                                idStato=idStato,
                                                cancellato=cancellato)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults() or 0

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return promogest.dao.DistintaBase.select(Environment.connection,
                                                nodo=True,
                                                 orderBy=self.orderBy,
                                                 denominazione=denominazione,
                                                 codice=codice,
                                                 codiceABarre=codiceABarre,
                                                 codiceArticoloFornitore=codiceArticoloFornitore,
                                                 produttore=produttore,
                                                 idFamiglia=idFamiglia,
                                                 idCategoria=idCategoria,
                                                 idStato=idStato,
                                                 cancellato=cancellato,
                                                 offset=offset,
                                                 batchSize=batchSize)

        self._filterClosure = filterClosure

        arts = self.runFilter()

        self._treeViewModel.clear()

        for a in arts:
            col = None
            if a.cancellato:
                col = 'red'
            self._treeViewModel.append((a,
                                        col,
                                        (a.codice or ''),
                                        (a.denominazione or ''),
                                        (a.produttore or ''),
                                        (a.codice_a_barre or ''),
                                        (a.codice_articolo_fornitore or ''),
                                        (a.denominazione_famiglia or ''),
                                        (a.denominazione_categoria or '')))



class AnagraficaDistintaBaseHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'distinta_base',
                                'Dettaglio distinta base')
    

class AnagraficaDistintaBaseReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco distinte base',
                                  defaultFileName='distinta_base',
                                  htmlTemplate='distinta_base',
                                  sxwTemplate='distinta_base')

class AnagraficaDistintaBaseEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle distinte base """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_distinta_base_detail_vbox',
                                'Dati articolo', gladeFile='distinta_base_plugins.glade')
        self._widgetFirstFocus = self.articolo_principale_button
        self.remove_article_button.set_sensitive(False)
        self._loading= False
        self.articoliAssociatiList = []

    def draw(self):
        treeview = self.articoli_associati_treeview

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Codice', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(300)
        treeview.append_column(column)
        
        treeview.set_search_column(2)
        self._assTreeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str,)
        self.articoli_associati_treeview.set_model(self._assTreeViewModel)
        
        
    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.daoPadre = Articolo(Environment.connection)
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.daoPadre = Articolo(Environment.connection, dao.id_articolo)
            associatedArts = promogest.dao.DistintaBase.select(Environment.connection,
                                                                                                        nodo=False,
                                                                                                        idPadre=self.daoPadre.id,
                                                                                                        offset=None,
                                                                                                        batchSize=None,
                                                                                                        immediate=True)
            self.articoliAssociatiList=[]
            for ass in associatedArts:
                self.articoliAssociatiList.append(ass)
        self._refresh()

    def _refresh(self):
        self._loading = True
        self.descrizione_label.set_text('')
        self.codice_label.set_text('')
        self._assTreeviewModel = self.articoli_associati_treeview.get_model()
        self._assTreeViewModel.clear()

        for articolo in self.articoliAssociatiList:
            col = None
            if articolo.cancellato:
                col = 'red'
            self._assTreeViewModel.append((articolo,
                                        col,
                                        (articolo.codice or ''),
                                        (articolo.denominazione or ''),))

        if self.daoPadre.id is None:
            string='Selezionare un articolo principale'
            self.descrizione_label.set_use_markup(True)
            self.descrizione_label.set_text(string)
        else:
            self.descrizione_label.set_text(self.daoPadre.denominazione or '')
        
        if self.daoPadre.codice is not None:
            self.codice_label.set_use_markup(True)
            self.codice_label.set_text(str(self.daoPadre.codice))

    def on_add_article_button_clicked(self, button):
        self.ricercaArticolo()

    def saveDao(self):
        """
        salva tutte le distinte base nel database
        """
        for articolo in self.articoliAssociatiList:
            articolo.persist(Environment.connection)
    
    def on_articolo_principale_button_clicked(self, button):
        self.ricercaArticolo(isNode=True)

    def ricercaArticolo(self, isNode= False):

        def on_ricerca_articolo_hide(anagWindow, anag, isNode=False):
            if anag.dao is None:
                anagWindow.destroy()
                return

            anagWindow.destroy()
            if isNode:
                self.mostraArticoloPadre(anag.dao.id)
            else:
                self.mostraArticoloFiglio(anag.dao)
        
        codice = None
        codiceABarre = None
        denominazione = None
        codiceArticoloFornitore = None

        from RicercaComplessaArticoli import RicercaComplessaArticoli
        anag = RicercaComplessaArticoli(denominazione=denominazione,
                                        codice=codice,
                                        codiceABarre=codiceABarre,
                                        codiceArticoloFornitore=codiceArticoloFornitore)
        anag.setTreeViewSelectionType(gtk.SELECTION_SINGLE)

        anagWindow = anag.getTopLevel()
        anagWindow.connect("hide",
                           on_ricerca_articolo_hide,
                           anag, isNode)
        anagWindow.set_transient_for(self.dialogTopLevel)
        anagWindow.show_all()


    def mostraArticoloPadre(self, id):
        self.daoPadre = Articolo(Environment.connection, id)
        for articolo in self.articoliAssociatiList:
            articolo.id_associato = id
        self._refresh()
        
    def mostraArticoloFiglio(self,dao):
        daoAssociazione= DistintaBase(Environment.connection)
        # qui è sufficiente settare solo le proprietà dell'associazione che vengono poi visualizzate nella treeview
        # nel salvataggio dellla stessa sono necessari solo id_articolo, e id_associato
        daoAssociazione.id_articolo = dao.id
        daoAssociazione.id_associato = self.daoPadre.id
        daoAssociazione.denominazione = dao.denominazione
        daoAssociazione.codice = dao.codice
        self.articoliAssociatiList.append(daoAssociazione)
        self._refresh()

    def on_remove_article_button_clicked(self, button):
        (model,iter) = self.articoli_associati_treeview.get_selection().get_selected()
        for dao in self.articoliAssociatiList:
            if model[iter][0] == dao:
                self.articoliAssociatiList.remove(dao)
                if dao.id is not None:
                    dao.delete(Environment.connection, son=True)
        model.remove(iter)

    def on_articoli_associati_treeview_row_activated(self, widget):
        self.remove_article_button.set_sensitive(True)
