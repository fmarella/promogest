# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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

from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.Promemoria import Promemoria
from datetime import datetime, timedelta
from utils import *
from utilsCombobox import *
from promogest.lib.HtmlHandler import createHtmlObj, renderTemplate, renderHTML

class AnagraficaPromemoria(Anagrafica):
    """ Anagrafica promemoria """

    def __init__(self, aziendaStr=None, selectedData=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica promemoria',
                            recordMenuLabel='_Promemoria',
                            filterElement=AnagraficaPromemoriaFilter(self),
                            htmlHandler=AnagraficaPromemoriaHtml(self),
                            reportHandler=AnagraficaPromemoriaReport(self),
                            editElement=AnagraficaPromemoriaEdit(self, selectedData=selectedData),
                            aziendaStr=aziendaStr)


class AnagraficaPromemoriaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei clienti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_promemoria_filter_table',
                                  gladeFile='_anagrafica_promemoria_elements.glade')
        self._widgetFirstFocus = self.da_data_inserimento_entry.entry
        self.orderBy = 'data_scadenza'

    def draw(self,cplx=False):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Data inserimento', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'data_inserimento')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data scadenza', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'data_scadenza')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Oggetto', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'oggetto')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Incaricato', renderer, text=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'incaricato')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Autore', renderer, text=5)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'autore')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Completato', renderer, text=6)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'completato')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Scaduto', renderer, text=7)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'scaduto')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('In scadenza', renderer, text=8)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'in_scadenza')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Riferimento', renderer, text=9)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.connect("clicked", self._changeOrderBy, 'riferimento')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str, str, str, str, str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.clear()

    def clear(self):
        # Annullamento filtro
        self.da_data_inserimento_entry.set_text('')
        self.a_data_inserimento_entry.set_text('')
        self.da_data_scadenza_entry.set_text('')
        self.a_data_scadenza_entry.set_text('')
        self.oggetto_filter_entry.set_text('')
        fillComboboxIncaricatiPromemoria(self.incaricato_combobox_filter_entry)
        self.incaricato_combobox_filter_entry.set_active(-1)
        self.incaricato_combobox_filter_entry.child.set_text('')
        fillComboboxAutoriPromemoria(self.autore_combobox_filter_entry)
        self.autore_combobox_filter_entry.set_active(-1)
        self.autore_combobox_filter_entry.child.set_text('')
        self.descrizione_filter_entry.set_text('')
        self.annotazione_filter_entry.set_text('')
        self.riferimento_filter_entry.set_text('')
        self.completati_checkbox.set_active(False)
        self.scaduti_checkbox.set_active(False)
        self.in_scadenza_checkbox.set_active(True)

        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        da_data_inserimento = stringToDateTime(emptyStringToNone(self.da_data_inserimento_entry.get_text()))
        a_data_inserimento = stringToDateTime(emptyStringToNone(self.a_data_inserimento_entry.get_text()))
        da_data_scadenza = stringToDateTime(emptyStringToNone(self.da_data_scadenza_entry.get_text()))
        a_data_scadenza = stringToDateTime(emptyStringToNone(self.a_data_scadenza_entry.get_text()))
        oggetto = prepareFilterString(self.oggetto_entry.get_text())
        incaricato = prepareFilterString(self.incaricato_combobox_filter_entry.get_active_text())
        autore = prepareFilterString(self.autore_combobox_filter_entry.get_active_text())
        descrizione = prepareFilterString(self.descrizione_filter_entry.get_text())
        annotazione = prepareFilterString(self.annotazione_filter_entry.get_text())
        riferimento = prepareFilterString(self.riferimento_filter_entry.get_text())
        completati = self.completati_checkbox.get_active()
        scaduti = self.scaduti_checkbox.get_active()
        in_scadenza = self.in_scadenza_checkbox.get_active()
        def filterCountClosure():
            return Promemoria().count( da_data_inserimento = da_data_inserimento,
                                a_data_inserimento = a_data_inserimento,
                                da_data_scadenza = da_data_scadenza,
                                a_data_scadenza = a_data_scadenza,
                                oggetto = oggetto,
                                incaricato = incaricato,
                                autore = autore,
                                descrizione = descrizione,
                                annotazione = annotazione,
                                riferimento = riferimento,
                                in_scadenza = in_scadenza,
                                scaduto = scaduti,
                                completato = completati)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Promemoria().select(orderBy=self.orderBy,
                                da_data_inserimento = da_data_inserimento,
                                a_data_inserimento = a_data_inserimento,
                                da_data_scadenza = da_data_scadenza,
                                a_data_scadenza = a_data_scadenza,
                                oggetto = oggetto,
                                incaricato = incaricato,
                                autore = autore,
                                descrizione = descrizione,
                                annotazione = annotazione,
                                riferimento = riferimento,
                                in_scadenza = in_scadenza,
                                scaduto = scaduti,
                                completato = completati,
                                offset = offset,
                                batchSize = batchSize)

        self._filterClosure = filterClosure
        memos = self.runFilter()

        self._treeViewModel.clear()

        for m in memos:
            if m.completato:
                compl = 'Si'
            else:
                compl = 'No'
            if m.scaduto:
                scad = 'Si'
            else:
                scad = 'No'
            if m.in_scadenza:
                in_scad = 'Si'
            else:
                in_scad = 'No'

            self._treeViewModel.append((m,
                                        dateTimeToString(m.data_inserimento),
                                        dateTimeToString(m.data_scadenza),
                                        (m.oggetto or ''),
                                        (m.incaricato or ''),
                                        (m.autore or ''),
                                        compl,
                                        scad,
                                        in_scad,
                                        (m.riferimento or '')))


class AnagraficaPromemoriaHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'promemoria',
                                'Informazioni sul promemoria')


class AnagraficaPromemoriaReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei promemoria',
                                  defaultFileName='promemoria',
                                  htmlTemplate='promemorias',
                                  sxwTemplate='promemoria')


class AnagraficaPromemoriaEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei clienti """

    def __init__(self, anagrafica, selectedData=None):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_promemoria_detail_table',
                                'Dati promemoria',
                                gladeFile='_anagrafica_promemoria_elements.glade')
        self._widgetFirstFocus = self.data_scadenza_entry
        self.selectedData = selectedData

    def draw(self,cplx=False):
        textBuffer = gtk.TextBuffer()
        self.descrizione_textview.set_buffer(textBuffer)
#        self.annotazioneHTML = createHtmlObj(self)
#        self.annotazione_scrolled.add(self.annotazioneHTML)
        textBuffer = gtk.TextBuffer()
        self.annotazione_textview.set_buffer(textBuffer)
        fillComboboxIncaricatiPromemoria(self.incaricato_combobox_entry)
        fillComboboxAutoriPromemoria(self.autore_combobox_entry)

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Promemoria()
            self._is_changing = False
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = Promemoria().getRecord(id= dao.id)
            self._is_changing = True
        self._refresh()

    def setPreavvisoSpinLimit(self, diffe):
        adj = self.giorni_preavviso_entry.get_adjustment()
        adj.set_upper(diffe)

    def on_data_scadenza_entry_focus_out_event(self, entry, event):
        differenze = 0
        data_scadenza = stringToDateTime(self.data_scadenza_entry.get_text())
        data_inserimento = stringToDateTime(self.data_inserimento_entry.get_text())
        if data_scadenza:
            differenze = int((data_scadenza - data_inserimento).days)
            self.setPreavvisoSpinLimit(differenze)

    def _refresh(self):
        self.data_scadenza_entry.set_text(dateTimeToString(self.dao.data_scadenza) or '')
        self.oggetto_entry.set_text(self.dao.oggetto or '')
        self.incaricato_combobox_entry.child.set_text(self.dao.incaricato or '')
        self.autore_combobox_entry.child.set_text(self.dao.autore or '')
        self.descrizione_textview.get_buffer().set_text(self.dao.descrizione or '')
#        static = self.dao.annotazione or "test"
#        pageData = {"file": "promemoria_annotazioni.html",
#                    "static":static,
#                    }
#        self.hhttmmll = renderTemplate(pageData)
#        renderHTML(self.annotazioneHTML,self.hhttmmll)
        self.annotazione_textview.get_buffer().set_text(self.dao.annotazione or '')
        self.riferimento_combobox_entry.child.set_text(self.dao.riferimento or '')
        self.giorni_preavviso_entry.set_text(str(self.dao.giorni_preavviso or ''))
        self.in_scadenza_checkbutton.set_active(self.dao.in_scadenza or False)
#        self.setPreavvisoSpinLimit()
        if self._is_changing:
            self.scaduto_checkbutton.set_property('visible',True)
            self.completato_checkbutton.set_property('visible',True)
            self.scaduto_checkbutton.set_active(self.dao.scaduto)
            self.completato_checkbutton.set_active(self.dao.completato)
            self.data_inserimento_entry.set_text(dateTimeToString(self.dao.data_inserimento))
        else:
            self.scaduto_checkbutton.set_property('visible',False)
            self.completato_checkbutton.set_property('visible',False)
            if self.selectedData:
                self.data_inserimento_entry.set_text(self.selectedData)
            else:
                self.data_inserimento_entry.set_text(dateTimeToString(datetime.datetime.now()) or '')

        fillComboboxIncaricatiPromemoria(self.incaricato_combobox_entry)
        fillComboboxAutoriPromemoria(self.autore_combobox_entry)

    def saveDao(self):
        if self.data_scadenza_entry.get_text() == '':
            msg = 'Data scadenza. \nCampo obbligatorio'
            obligatoryField(self.dialogTopLevel, self.data_scadenza_entry, msg)

        if self.oggetto_entry.get_text() == '':
            msg = 'Oggetto. \nCampo obbligatorio'
            obligatoryField(self.dialogTopLevel, self.oggetto_entry, msg)
        self.dao.data_inserimento = stringToDateTime(self.data_inserimento_entry.get_text())
        self.dao.data_scadenza = stringToDateTime(self.data_scadenza_entry.get_text())
        self.dao.oggetto = self.oggetto_entry.get_text()
        self.dao.incaricato = self.incaricato_combobox_entry.get_active_text()
        self.dao.autore = self.autore_combobox_entry.get_active_text()
        textBuffer = self.descrizione_textview.get_buffer()
        self.dao.descrizione = textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter())
        textBuffer = self.annotazione_textview.get_buffer()
        self.dao.annotazione = textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter())
        self.dao.riferimento = self.riferimento_combobox_entry.get_active_text()
        if self.giorni_preavviso_entry.get_text() == '':
            self.giorni_preavviso_entry.set_text('0')
            self.in_scadenza_checkbutton.set_active(True)
        self.dao.giorni_preavviso = self.giorni_preavviso_entry.get_text()
        self.dao.in_scadenza = self.in_scadenza_checkbutton.get_active()
        self.dao.scaduto = self.scaduto_checkbutton.get_active()
        self.dao.completato = self.completato_checkbutton.get_active()

        self.dao.persist()

    def on_riferimento_combobox_entry_changed(self, combobox):
        stringContatti = 'Contatti..'
        stringClienti = 'Clienti..'
        stringFornitori = 'Fornitori..'


        def refresh_combobox(anagWindow, tipo):
            if anag.dao is None:
                id = None
            else:
                id = anag.dao.id
            if tipo == 'fornitore':
                res = leggiFornitore(id)
            elif tipo == 'cliente':
                res = leggiCliente(id)
            elif tipo == 'contatto':
                res = leggiContatto(id)

            if res.has_key("ragioneSociale") and res["ragioneSociale"] != '':
                self.riferimento_combobox_entry.child.set_text(res["ragioneSociale"])
            else:
                self.riferimento_combobox_entry.child.set_text(res["cognome"] + ' ' + res["nome"])
            anag.on_ricerca_window_close(self)

        if combobox.child.get_text() == stringClienti:
            from RicercaComplessaClienti import RicercaComplessaClienti
            anag = RicercaComplessaClienti()
            anag.setTreeViewSelectionType(gtk.SELECTION_SINGLE)
            anagWindow = anag.getTopLevel()
            anagWindow.connect("hide", refresh_combobox, 'cliente')
            returnWindow = combobox.get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anag.show_all()
        elif combobox.child.get_text() == stringFornitori:
            from RicercaComplessaFornitori import RicercaComplessaFornitori
            anag = RicercaComplessaFornitori()
            anag.setTreeViewSelectionType(gtk.SELECTION_SINGLE)
            anagWindow = anag.getTopLevel()
            anagWindow.connect("hide", refresh_combobox, 'fornitore')
            returnWindow = combobox.get_toplevel()
            anagWindow.set_transient_for(returnWindow)
            anag.show_all()
        elif combobox.child.get_text() == stringContatti:
            if ("Contatti" in Environment.modulesList) or \
                    ("pan" in Environment.modulesList) or \
                        ("basic" in Environment.modulesList):
                from promogest.modules.Contatti.ui.RicercaContatti import RicercaContatti
                anag = RicercaContatti()
                anagWindow = anag.getTopLevel()
                anagWindow.connect("hide", refresh_combobox, 'contatto')
                returnWindow = combobox.get_toplevel()
                anagWindow.set_transient_for(returnWindow)
                anag.show_all()
            else:
                fenceDialog()
