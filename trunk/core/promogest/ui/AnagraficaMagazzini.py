# -*- coding: utf-8 -*-

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
import promogest.dao.Magazzino
from promogest.dao.Magazzino import Magazzino

from utils import *
from utilsCombobox import *


class AnagraficaMagazzini(Anagrafica):
    """ Anagrafica magazzini """

    def __init__(self, denominazione=None, aziendaStr=None):
        self._denominazione = denominazione
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica magazzini',
                            recordMenuLabel='_Magazzini',
                            filterElement=AnagraficaMagazziniFilter(self),
                            htmlHandler=AnagraficaMagazziniHtml(self),
                            reportHandler=AnagraficaMagazziniReport(self),
                            editElement=AnagraficaMagazziniEdit(self),
                            aziendaStr=aziendaStr)


class AnagraficaMagazziniFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei magazzini """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_magazzini_filter_table',
                                  gladeFile='_anagrafica_magazzini_elements.glade')
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
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        if self._anagrafica._denominazione is not None:
            self.denominazione_filter_entry.set_text(self._anagrafica._denominazione)

        self.refresh()

        if self._anagrafica._denominazione is not None:
            self._anagrafica.anagrafica_filter_treeview.grab_focus()

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())

        def filterCountClosure():
            return Magazzino().count(denominazione=denominazione)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Magazzino().select(  denominazione=denominazione,
                                orderBy=self.orderBy,
                                offset=offset,
                                batchSize=batchSize)


        self._filterClosure = filterClosure

        mags = self.runFilter()

        self._treeViewModel.clear()
        if Environment.tipo_eng =="sqlite":
            if len(mags) >1:
                liss = mags[0]
        for m in mags:
            self._treeViewModel.append((m,
                                        (m.denominazione or '')))



class AnagraficaMagazziniHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'magazzino',
                                'Informazioni sul magazzino')



class AnagraficaMagazziniReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei magazzini',
                                  defaultFileName='magazzini',
                                  htmlTemplate='magazzini',
                                  sxwTemplate='magazzini')



class AnagraficaMagazziniEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei magazzini """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                  anagrafica,
                                  'anagrafica_magazzini_detail_table',
                                  'Dati magazzino',
                                  gladeFile='_anagrafica_magazzini_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry


    def draw(self):
        pass


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            if Environment.tipo_eng =="sqlite" and Magazzino().count() >=1:
                self.destroy()
                msg="STAI USANDO UNA VERSIONE BASE DI PROMOGEST2\n CHE GESTISCE UN SOLO MAGAZZINO"
                dialog = gtk.MessageDialog(None,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
                dialog.run()
                dialog.destroy()
            else:
                self.dao = Magazzino()
                self._refresh()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Magazzino().getRecord(id=dao.id)
            self._refresh()

    def _refresh(self):
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.indirizzo_entry.set_text(self.dao.indirizzo or '')
        self.localita_entry.set_text(self.dao.localita or '')
        self.cap_entry.set_text(self.dao.cap or '')
        self.provincia_entry.set_text(self.dao.provincia or '')

    def saveDao(self):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.indirizzo = self.indirizzo_entry.get_text()
        self.dao.localita = self.localita_entry.get_text()
        self.dao.cap = self.cap_entry.get_text()
        self.dao.provincia = self.provincia_entry.get_text()
        if Environment.tipo_eng =="sqlite" and Magazzino().count() >=1:
            return
        self.dao.persist()


    def on_contatti_togglebutton_clicked(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return

        if self.dao.id is None:
            msg = 'Prima di poter inserire i contatti occorre salvare il magazzino.\n Salvare ?'
            dialog = gtk.MessageDialog(self.dialogTopLevel, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.on_anagrafica_complessa_detail_dialog_response(self.dialogTopLevel, gtk.RESPONSE_APPLY)
            else:
                toggleButton.set_active(False)
                return

        from AnagraficaContatti import AnagraficaContatti
        anag = AnagraficaContatti(self.dao.id, 'magazzino')
        anagWindow = anag.getTopLevel()

        showAnagraficaRichiamata(self.dialogTopLevel, anagWindow, toggleButton)
