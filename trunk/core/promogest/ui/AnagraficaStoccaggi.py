# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 Author: Andrea Argiolas <andrea@promotux.it>
 License: GNU GPLv2
"""

import gtk
import gobject

from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.Stoccaggio
from promogest.dao.Stoccaggio import Stoccaggio

from utils import *
from utilsCombobox import *


class AnagraficaStoccaggi(Anagrafica):
    """ Anagrafica stoccaggi articoli """

    def __init__(self, idArticolo=None, idMagazzino=None, aziendaStr=None):
        self._articoloFissato = (idArticolo <> None)
        self._magazzinoFissato = (idMagazzino <> None)
        self._idArticolo=idArticolo
        self._idMagazzino=idMagazzino
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Situazione magazzino',
                            recordMenuLabel='_Stoccaggi',
                            filterElement=AnagraficaStoccaggiFilter(self),
                            htmlHandler=AnagraficaStoccaggiHtml(self),
                            reportHandler=AnagraficaStoccaggiReport(self),
                            editElement=AnagraficaStoccaggiEdit(self),
                            aziendaStr=aziendaStr)



class AnagraficaStoccaggiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica stoccaggi """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_stoccaggi_filter_table', gladeFile='_anagrafica_stoccaggi_articoli_elements.glade')
        self._widgetFirstFocus = self.id_magazzino_filter_combobox
        self.orderBy=None


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        rendererSx = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Magazzino', rendererSx, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'magazzino')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'codice_articolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Articolo', rendererSx, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'articolo')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        self._treeViewModel = gtk.ListStore(object, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)

        if self._anagrafica._articoloFissato:
            self.id_articolo_filter_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_filter_customcombobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(1)
            column.set_property('visible', False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(2)
            column.set_property('visible', False)
        if self._anagrafica._magazzinoFissato:
            findComboboxRowFromId(self.id_magazzino_filter_combobox, self._anagrafica._idMagazzino)
            self.id_magazzino_filter_combobox.set_sensitive(False)
            column = self._anagrafica.anagrafica_filter_treeview.get_column(0)
            column.set_property('visible', False)

        self.clear()


    def clear(self):
        # Annullamento filtro
        if not(self._anagrafica._magazzinoFissato):
            fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
            self.id_magazzino_filter_combobox.set_active(0)
        if not(self._anagrafica._articoloFissato):
            self.id_articolo_filter_customcombobox.set_active(0)
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        idArticolo = self.id_articolo_filter_customcombobox.getId()
        idMagazzino = findIdFromCombobox(self.id_magazzino_filter_combobox)


        def filterCountClosure():
            return Stoccaggio().count(idArticolo=idArticolo,
                                                  idMagazzino=idMagazzino)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Stoccaggio().select(orderBy=self.orderBy,
                                                   idArticolo=idArticolo,
                                                   idMagazzino=idMagazzino,
                                                   offset=offset,
                                                   batchSize=batchSize)


        self._filterClosure = filterClosure

        stos = self.runFilter()

        self._treeViewModel.clear()

        for s in stos:
            self._treeViewModel.append((s,
                                        (s.magazzino or ''),
                                        (s.codice_articolo or ''),
                                        (s.articolo or '')))



class AnagraficaStoccaggiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'stoccaggio',
                                'Informazioni sullo stoccaggio')



class AnagraficaStoccaggiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli stoccaggi',
                                  defaultFileName='stoccaggi',
                                  htmlTemplate='stoccaggi',
                                  sxwTemplate='stoccaggi')



class AnagraficaStoccaggiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei stoccaggi """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_stoccaggi_detail_table',
                                'Dati stoccaggi',
                                gladeFile='_anagrafica_stoccaggi_articoli_elements.glade')
        self._widgetFirstFocus = self.id_magazzino_customcombobox


    def draw(self):
        self.id_articolo_customcombobox.setSingleValue()

        fillComboboxMagazzini(self.id_magazzino_customcombobox.combobox)
        self.id_magazzino_customcombobox.connect('clicked',
                                                 on_id_magazzino_customcombobox_clicked)

        if self._anagrafica._articoloFissato:
            self.id_articolo_customcombobox.setId(self._anagrafica._idArticolo)
            self.id_articolo_customcombobox.set_sensitive(False)
        if self._anagrafica._magazzinoFissato:
            findComboboxRowFromId(self.id_magazzino_customcombobox.combobox, self._anagrafica._idMagazzino)
            self.id_magazzino_customcombobox.set_sensitive(False)


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Stoccaggio()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Stoccaggio().getRecord(id=dao.id)
        self._refresh()


    def _refresh(self):
        self.id_articolo_customcombobox.refresh(clear=True, filter=False)
        self.id_articolo_customcombobox.set_sensitive(True)
        if self.dao.id_articolo is None:
            if self._anagrafica._articoloFissato:
                self.dao.id_articolo = self._anagrafica._idArticolo
                self.id_articolo_customcombobox.set_sensitive(False)
        else:
            self.id_articolo_customcombobox.set_sensitive(False)
        self.id_articolo_customcombobox.setId(self.dao.id_articolo)
        self.id_magazzino_customcombobox.combobox.set_active(-1)
        self.id_magazzino_customcombobox.set_sensitive(True)
        if self.dao.id_magazzino is None:
            if self._anagrafica._magazzinoFissato:
                self.dao.id_magazzino = self._anagrafica._idMagazzino
                self.id_magazzino_customcombobox.set_sensitive(False)
        else:
            self.id_magazzino_customcombobox.set_sensitive(False)
        findComboboxRowFromId(self.id_magazzino_customcombobox.combobox, self.dao.id_magazzino)
        self.scorta_minima_entry.set_text(str(self.dao.scorta_minima or 0))
        self.livello_riordino_entry.set_text(str(self.dao.livello_riordino or 0))
        self.data_fine_scorte_entry.set_text(dateToString(self.dao.data_fine_scorte))
        self.data_prossimo_ordine_entry.set_text(dateToString(self.dao.data_prossimo_ordine))


    def saveDao(self):
        if findIdFromCombobox(self.id_magazzino_customcombobox.combobox) is None:
            obligatoryField(self.dialogTopLevel, self.id_magazzino_customcombobox.combobox)

        if self.id_articolo_customcombobox.getId() is None:
            obligatoryField(self.dialogTopLevel, self.id_articolo_customcombobox)

        self.dao.id_magazzino = findIdFromCombobox(self.id_magazzino_customcombobox.combobox)
        self.dao.id_articolo = self.id_articolo_customcombobox.getId()
        self.dao.scorta_minima = int(self.scorta_minima_entry.get_text())
        self.dao.livello_riordino = int(self.livello_riordino_entry.get_text())
        self.dao.data_fine_scorte = stringToDate(self.data_fine_scorte_entry.get_text())
        self.dao.data_prossimo_ordine = stringToDate(self.data_prossimo_ordine_entry.get_text())
        self.dao.persist()
