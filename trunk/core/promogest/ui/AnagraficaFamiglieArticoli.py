# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010,2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
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
from AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.dao.FamigliaArticolo import FamigliaArticolo
from promogest.dao.Articolo import Articolo
from utils import *
from utilsCombobox import *


class AnagraficaFamiglieArticoli(Anagrafica):
    """ Anagrafica famiglie degli articoli """

    def __init__(self):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica famiglie articoli',
                            recordMenuLabel='_Famiglie',
                            filterElement=AnagraficaFamiglieArticoliFilter(self),
                            htmlHandler=AnagraficaFamiglieArticoliHtml(self),
                            reportHandler=AnagraficaFamiglieArticoliReport(self),
                            editElement=AnagraficaFamiglieArticoliEdit(self))
        self.hideNavigator()
        self.records_file_export.set_sensitive(True)
        self.duplica_button.set_sensitive(False)

    def on_record_delete_activate(self, widget):
        dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   'Confermi l\'eliminazione ?')
        response = dialog.run()
        dialog.destroy()
        if response !=  gtk.RESPONSE_YES:
            return

        dao = self.filter.getSelectedDao()
        if not dao:
            return
        usata = Articolo().select(idFamiglia=dao.id, batchSize=None)
        if usata:
            msg = """NON è possibile cancellare questa FAMIGLIA ARTICOLO
perchè abbinata ad uno o più articoli

ATTENZIONE ATTENZIONE!!

E' però possibile "passare" tutti gli articoli della famiglia che
si vuole cancellare ad un'altra ancora presente.
Inserite il codice ( Esattamente come è scritto) della famiglia di destinazione
qui sotto e premete SI
L'operazione è irreversibile, retroattiva e potrebbe impiegare qualche minuto.
"""
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL
                                   | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   msg)
            __entry_codi = gtk.Entry()
            dialog.vbox.pack_start(__entry_codi)
            __entry_codi.show()
            response = dialog.run()

            if response !=  gtk.RESPONSE_YES:
                dialog.destroy()
                return
            else:
#                print "WBUMMMMM", __entry_codi.get_text()
                famm = FamigliaArticolo().select(codice = __entry_codi.get_text())
                if famm:
                    idfam = famm[0].id
                    isfather = FamigliaArticolo().select(idPadre =idfam)
                    if isfather:
                        messageInfo(msg = "Cancellare prima i figli,\n questa è una famiglia padre non vuota ")
                        dialog.destroy()
                        return
                else:
                    messageInfo(msg = "NON è stato possibile trovare la famiglia\n di passaggio, non faccio niente")
                    dialog.destroy()
                    return
                for u in usata:
                    u.id_famiglia_articolo = idfam
                    u.persist()
                dialog.destroy()
                dao.delete()
                self.htmlHandler.setDao(None)
        else:
            dao.delete()
            self.htmlHandler.setDao(None)
        self.filter.refresh()
        self.setFocus()


class AnagraficaFamiglieArticoliFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle famiglie articoli """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_famiglie_articoli_filter_table',
                                  gladeFile='_anagrafica_famiglie_articoli_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.orderBy = 'denominazione'


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Codice', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione breve', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(False)
        treeview.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Descrizione', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(True)
        column.set_expand(True)
        treeview.append_column(column)

        renderer = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', renderer, pixbuf=4)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(False)
        column.set_resizable(False)
        column.set_expand(False)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.TreeStore(object, str, str, str, gtk.gdk.Pixbuf)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.codice_filter_entry.set_text('')
        self.denominazione_filter_entry.set_text('')
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        def filterCountClosure():
            return FamigliaArticolo().count()

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return  FamigliaArticolo().select(offset=None,batchSize=None)

        self._filterClosure = filterClosure

        fams = self.runFilter()

        self._treeViewModel.clear()

        padri= FamigliaArticolo().fathers()

        def recurse(padre,f):
            """ funzione di recursione per ogni figlio di ogni padre """
            for s in f.children:
                figlio1 = self._treeViewModel.append(padre, (s,
                                                    (s.codice or ''),
                                                    (s.denominazione_breve or ''),
                                                    (s.denominazione or ''),
                                                    None))
                recurse(figlio1,s)

        for f in fams:
            if f.id == f.id_padre:
                f.id_padre= None
                f.persist()
            if not f.parent:
                padre = self._treeViewModel.append(None, (f,
                                                        (f.codice or ''),
                                                        (f.denominazione_breve or ''),
                                                        (f.denominazione or ''),
                                                        None))
                if f.children:
                    recurse(padre,f)

        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)
        self._anagrafica.anagrafica_filter_treeview.collapse_all()

        denominazione = emptyStringToNone(self.denominazione_filter_entry.get_text())
        codice = emptyStringToNone(self.codice_filter_entry.get_text())
        if not (denominazione is None) or not (codice is None):
            self._treeViewModel.foreach(self.selectFilter, (denominazione, codice))


    def selectFilter(self, model, path, iter, (denominazione, codice)):
        #Seleziona elementi che concordano con il filtro
        c = model.get_value(iter, 0)
        found = False
        if denominazione is not None:
            found = (denominazione.upper() in c.denominazione.upper())
        if codice is not None:
            found = found or (codice.upper() in c.codice.upper())
        if found:
            image = gtk.Image()
            anagPixbuf = image.render_icon(gtk.STOCK_GO_BACK,
                                           gtk.ICON_SIZE_BUTTON)
            model.set_value(iter, 4, anagPixbuf)
            self._anagrafica.anagrafica_filter_treeview.expand_to_path(path)
        else:
            model.set_value(iter, 4, None)



class AnagraficaFamiglieArticoliHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'famiglia_articolo',
                                'Informazioni sulla famiglia articoli')



class AnagraficaFamiglieArticoliReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle famiglie articoli',
                                  defaultFileName='famiglie_articoli',
                                  htmlTemplate='famiglie_articoli',
                                  sxwTemplate='famiglie_articoli')



class AnagraficaFamiglieArticoliEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle famiglie articoli """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_famiglie_articoli_detail_table',
                                'Dati famiglia articolo',
                                gladeFile='_anagrafica_famiglie_articoli_elements.glade')
        self._widgetFirstFocus = self.codice_entry

    def draw(self,cplx=False):
        #Popola combobox famiglie articoli
        fillComboboxFamiglieArticoli(self.id_padre_combobox)

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = FamigliaArticolo()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = FamigliaArticolo().getRecord(id = dao.id)
        self._refresh()
        return self.dao

    def _refresh(self):
        self.codice_entry.set_text(self.dao.codice or '')
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.denominazione_breve_entry.set_text(self.dao.denominazione_breve or '')
        fillComboboxFamiglieArticoli(self.id_padre_combobox, ignore=[self.dao.id])
        findComboboxRowFromId(self.id_padre_combobox, self.dao.id_padre)

    def saveDao(self, tipo=None):
        if (self.codice_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.codice_entry,
            msg="Codice Famiglia Articolo.\n\n Campo Obbligatorio!")
            self.dao.codice = omogeneousCode(section="Famiglie", string=self.dao.codice )

        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry,
            msg="Denominazione Famiglia Articolo.\n\n Campo Obbligatorio!")

        if (self.denominazione_breve_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_breve_entry,
            msg="Denominazione Breve Famiglia Articolo.\n\n Campo Obbligatorio!")

        self.dao.codice = self.codice_entry.get_text()
        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.denominazione_breve =self.denominazione_breve_entry.get_text()
        self.dao.id_padre = findIdFromCombobox(self.id_padre_combobox)
        if self.dao.id and self.dao.id == self.dao.id_padre:
            messageInfo(msg="NON SI PUÒ ASSEGNARE QUESTO COME PADRE\n È UGUALE AL FIGLIO ")
            return
        else:
            self.dao.persist()
