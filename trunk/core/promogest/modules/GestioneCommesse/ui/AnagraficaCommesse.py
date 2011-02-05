# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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
import gobject
from decimal import *
from promogest.ui.AnagraficaComplessa import Anagrafica, AnagraficaFilter, \
                            AnagraficaHtml, AnagraficaReport, AnagraficaEdit
from promogest.modules.GestioneCommesse.dao.StadioCommessa import StadioCommessa
from promogest.modules.GestioneCommesse.dao.TestataCommessa import TestataCommessa
from promogest.modules.GestioneCommesse.dao.RigaCommessa import RigaCommessa
from promogest.dao.Cliente import Cliente
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.lib.relativedelta import relativedelta
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaCommesse(Anagrafica):
    """ Anagrafica Comesse """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica Gestione Commesse',
                            recordMenuLabel='_Gestione commesse',
                            filterElement=AnagraficaCommesseFilter(self),
                            htmlHandler=AnagraficaCommesseHtml(self),
                            reportHandler=AnagraficaCommesseReport(self),
                            editElement=AnagraficaCommesseEdit(self),
                            aziendaStr=aziendaStr)
        self.records_print_on_screen_button.set_sensitive(False)
        self.records_print_button.set_sensitive(False)
        self.records_file_export.set_sensitive(True)


class AnagraficaCommesseFilter(AnagraficaFilter):
    """ Filtro per la ricerca nella prim nota cassa """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_commessa_filter_table',
                          gladeFile='GestioneCommesse/gui/_anagrafica_commessa_elements.glade',
                          module=True)
        self._widgetFirstFocus = self.numero_filter_entry
        self.da_data_inizio_datetimewidget.set_text('01/01/' + Environment.workingYear+" 00:00")


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Numero', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'numero'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Da Data', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None, 'data_inizio'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('A Data', renderer, text=4, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None, 'data_fine'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Saldo singola Prima nota', renderer, text=5, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Totale Riporti', renderer, text=6, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Nome/Note', renderer, text=7, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
#        column.set_clickable(True)
#        column.connect('clicked', self._changeOrderBy, (None, 'data_inizio'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)


        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str,str, str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.refresh()

    def clear(self):
        # Annullamento filtro
        self.da_data_inizio_datetimewidget.set_text('01/01/' + Environment.workingYear+" 00:00")
        self.numero_filter_entry.set_text('')
#        self.da_data_inizio_datetimewidget.set_text('')
        self.a_data_inizio_datetimewidget.set_text('')
        self.da_data_fine_datetimewidget.set_text('')
        self.a_data_fine_datetimewidget.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        numero = prepareFilterString(self.numero_filter_entry.get_text())
        da_data_inizio = stringToDateTime(emptyStringToNone(self.da_data_inizio_datetimewidget.get_text()))
        a_data_inizio = stringToDateTime(emptyStringToNone(self.a_data_inizio_datetimewidget.get_text()))
        da_data_fine = stringToDateTime(emptyStringToNone(self.da_data_fine_datetimewidget.get_text()))
        a_data_fine = stringToDateTime(emptyStringToNone(self.a_data_fine_datetimewidget.get_text()))

        def filterCountClosure():
            return TestataCommessa().count(numero=numero,
                                daDataInizio = da_data_inizio,
                                aDataInizio = a_data_inizio,
                                daDataFine = da_data_fine,
                                aDataFine = a_data_fine)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return TestataCommessa().select(numero=numero,
                                     daDataInizio = da_data_inizio,
                                    aDataInizio = a_data_inizio,
                                    daDataFine = da_data_fine,
                                    aDataFine = a_data_fine,
                                        orderBy=self.orderBy,
                                        offset=offset,
                                        batchSize=batchSize)

        self._filterClosure = filterClosure

        valis = self.runFilter()

        self._treeViewModel.clear()
        valore = 0
        for i in valis:
            col = None
            if not i.data_fine:
                col = "#CCFFAA"
            valore += mN(i.totali["totale"]) or 0
            self._treeViewModel.append((i,col,
                                        (i.numero or ''),
                                        (dateToString(i.data_inizio) or ''),
                                        (dateToString(i.data_fine) or ''),
                                        (str(mN(i.totali["totale"])) or "0"),
                                        str(valore),
                                        (i.note or "")))


class AnagraficaCommesseHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'prima_nota',
                                'Dettaglio Prima Nota Cassa')


class AnagraficaCommesseReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle Prime Note Cassa',
                                  defaultFileName='commessa',
                                  htmlTemplate='commessa',
                                  sxwTemplate='commessa')


class AnagraficaCommesseEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle commessa """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_commessa_detail_vbox',
                                'Dati della commessa cliente.',
                                gladeFile='GestioneCommesse/gui/_anagrafica_commessa_elements.glade',
                                module=True)
        self._widgetFirstFocus = self.titolo_commessa_entry
        self.anagrafica = anagrafica
        self.editRiga = None
        self.daoo = None
#        self.rotazione = setconf("rotazione_primanota","Primanota")
#        fillComboboxBanche(self.id_banca_customcombobox.combobox)
#        self.id_banca_customcombobox.connect('clicked',
#                                 on_id_banca_customcombobox_clicked)
#        self.id_banca_customcombobox.set_sensitive(False)

    def draw(self, cplx=False):
        treeview = self.riga_commessa_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Numero', renderer, text=1, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(50)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data', renderer, text=2, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Titolo', renderer, text=3, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
#        column.set_clickable(True)
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Tipo', renderer, text=4, background=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)
        self._rigaModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str,str, str, str,str, str, int)
        self.riga_commessa_treeview.set_model(self._rigaModel)
        fillComboboxStadioCommessa(self.stadio_commessa_combobox.combobox)
        self.stadio_commessa_combobox.connect('clicked',
                                            on_stadio_commessa_combobox_clicked)
        model = self.tipo_combobox.get_model()
        model.clear()
        tipi = ["","DOCUMENTO", "PROMEMORIA", "FORNITORE", "ARTICOLO",
                    "VETTORE", "MAGAZZINO",
                     "CLIENTE","AGENTE"]
        for t in tipi:
            model.append((t,))
        self.open_button.set_sensitive(False)
        self.trova_button.set_sensitive(False)
        self.new_dao_button.set_sensitive(False)
        self.stampa_dao_button.set_sensitive(False)


    def composeInfoDaoLabel(self, dao):
        if not dao:
            info = ""
        elif dao.__class__.__name__ == "TestataDocumento":
            info = "<b>%s</b>  - <b>del</b> %s <b>N°</b> %s - <b>Da/A</b> %s  - <b>TOT: €</b> %s" %(str(dao.operazione),
                                                                dateToString(dao.data_documento),
                                                                str(dao.numero),
                                                                dao.intestatario,
                                                                str(mN(dao._totaleScontato,2)))
        elif dao.__class__.__name__ == "Promemoria":
            info = "Promemoria <b>del</b> %s  <b>Descr:</b> %s" %(str(dateToString(dao.data_inserimento)),
            dao.descrizione[0:50])
        elif dao.__class__.__name__ in ["Cliente", "Fornitore", "Vettore", "Agente"]:
            info = "<b>%s</b>,  %s , %s %s" %(str(dao.__class__.__name__),
                                        dao.ragione_sociale,
                                        dao.cognome,
                                        dao.nome)
        elif dao.__class__.__name__ =="Magazzino":
            info = "Magazzino: %s , %s " %(str(dao.denominazione),str(dao.pvcode))
        self.info_dao_label.set_markup(info)


    def on_tipo_combobox_changed(self, combobox):
        """ """
        self.open_button.set_sensitive(False)
        self.trova_button.set_sensitive(False)
        self.new_dao_button.set_sensitive(False)
        self.stampa_dao_button.set_sensitive(False)
        self.tipo_dao = combobox.get_model().get_value(combobox.get_active_iter(), 0).lower()
        if self.tipo_dao:
#            self.open_button.set_sensitive(True)
            self.trova_button.set_sensitive(True)
            self.new_dao_button.set_sensitive(True)
#            self.stampa_dao_button.set_sensitive(True)
        self.composeInfoDaoLabel(None)

    def on_trova_button_clicked(self, button):
#        self.new_dao_button.set_sensitive(False)
        def returnDao(anagWindow):
            if anag.dao:
                self.dao_temp = anag.dao
                self.composeInfoDaoLabel(anag.dao)
                self.open_button.set_sensitive(True)
                self.stampa_dao_button.set_sensitive(True)
            else:
                self.dao_temp = None

        if self.tipo_dao !="":
            if self.tipo_dao =="DOCUMENTO".lower():
                from promogest.ui.SimpleSearch.RicercaDocumenti import RicercaDocumenti
                anag = RicercaDocumenti()
            elif self.tipo_dao =="PROMEMORIA".lower():
                from promogest.ui.SimpleSearch.RicercaPromemoria import RicercaPromemoria
                anag = RicercaPromemoria()
            elif self.tipo_dao =="FORNITORE".lower():
                from promogest.ui.SimpleSearch.RicercaFornitori import RicercaFornitori
                anag = RicercaFornitori()
            elif self.tipo_dao =="ARTICOLO".lower():
                from promogest.ui.SimpleSearch.RicercaArticoli import RicercaArticoli
                anag = RicercaArticoli()
            elif self.tipo_dao =="VETTORE".lower():
                from promogest.ui.SimpleSearch.RicercaVettori import RicercaVettori
                anag = RicercaVettori()
            elif self.tipo_dao =="MAGAZZINO".lower():
                from promogest.ui.SimpleSearch.RicercaMagazzini import RicercaMagazzini
                anag = RicercaMagazzini()
            elif self.tipo_dao =="CLIENTE".lower():
                from promogest.ui.SimpleSearch.RicercaClienti import RicercaClienti
                anag = RicercaClienti()
            elif self.tipo_dao =="AGENTE".lower():
                from promogest.ui.SimpleSearch.RicercaAgenti import RicercaAgenti
                anag = RicercaAgenti()
            anagWindow = anag.getTopLevel()
            anagWindow.show_all()
            anagWindow.connect("hide",returnDao)






    def setDao(self, dao):
        if dao is None:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = TestataCommessa()
        else:
            self.dao = TestataCommessa().getRecord(id=dao.id)
        self._refresh()
        return self.dao


    def _refresh(self):
        return

    def clear(self):
        self.data_ins_riga.set_text("")
        bufferNoteRiga= self.riga_testo.get_buffer()
        bufferNoteRiga.set_text("")
        self.riga_testo.set_buffer(bufferNoteRiga)
        self.info_dao_label.set_text("-")
        self.titolo_riga_commessa_entry.set_text("")
        self.tipo_combobox.set_active(0)

    def on_delete_row_button_clicked(self, button):
        print "CANCELLIAMO"


    def on_add_row_button_clicked(self, button):
        """ Aggiunge la riga """

        titolo_riga = self.titolo_riga_commessa_entry.get_text()
        if not titolo_riga:
            titolo_riga = self.info_dao_label.get_text()
        bufferNoteRiga= self.riga_testo.get_buffer()
        note_riga = bufferNoteRiga.get_text(bufferNoteRiga.get_start_iter(), bufferNoteRiga.get_end_iter()) or ""

        if self.dao_temp:
            dao_id = self.dao_temp.id
            dao_class = self.dao_temp.__class__.__name__

        if not titolo_riga:
            obligatoryField(self.dialogTopLevel, self.denominazione_entry,
            msg="Campo obbligatorio: TITOLO RIGA!")
        data_ins_riga = dateToString(self.data_ins_riga.get_text())

#        print "DDDDDDDDDDDDDDDDDD",  titolo_riga, note_riga, data_ins_riga, dao_id, dao_class

        model = self.riga_commessa_treeview.get_model()
        if self.editRiga:
            riga = self.editRiga
            riga.numero = self.editRiga.numero
        else:
            riga = RigaCommessa()
            riga.numero = len(model)+1

        riga.data_registrazione = data_ins_riga
        riga.denominazione = titolo_riga
        if dao_class =="TestataDocumento":
            dc = self.dao_temp.operazione
        else:
            dc = dao_class

        dati = (riga,str(len(model)+1),data_ins_riga,
                        titolo_riga,
                        str(dc),
                            note_riga, dao_class, int(dao_id))
        if self.editRiga:
            if riga.dao_class=="TestataDocumento":
                td = TestataDocumento().getRecord(id=riga.id_dao)
                dc = td.operazione
            else:
                dc = riga.dao_class
            self.rigaIter[0] = riga
            self.rigaIter[1] = str(riga.numero)
            self.rigaIter[2] = dateToString(riga.data_registrazione)
            self.rigaIter[3] = riga.denominazione[0:100]
            self.rigaIter[4] =  dc
            self.rigaIter[5] =  riga.note
            self.rigaIter[6] =  riga.dao_class
            self.rigaIter[7] =  int(riga.id_dao)
        else:
            model.append(dati)
        self.riga_commessa_treeview.set_model(model)
        self.editRiga = None
        self.clear()


    def on_rimuovi_button_clicked(self, button):
        """ Elimina la riga di prima nota selezionata
        """
        if self.editRiga:
            dao = RigaCommessa().getRecord(id=self.editRiga.id)
            dao.delete()
            self._editModel.remove(self._editIterator)
            self.clear()

    def on_riga_commessa_treeview_row_activated(self,treeview, path, column):
        """Selezione della riga nella treeview
        """
        sel = self.riga_commessa_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.rigaIter = model[iterator]
        self._editIterator = iterator
        self._editModel = model
        self.data_ins_riga.set_text(self.rigaIter[2])
        self.titolo_riga_commessa_entry.set_text(self.rigaIter[3])
        bufferNoteRiga= self.riga_testo.get_buffer()
        bufferNoteRiga.set_text(self.rigaIter[5])
        self.riga_testo.set_buffer(bufferNoteRiga)

        self.editRiga = self.rigaIter[0]


    def saveDao(self, chiusura=False):
        """ Salvataggio della commessa nel tabase
        """
        model = self.riga_commessa_treeview.get_model()
        righe_ = []
        for m in model:
            righe_.append(m[0])
        self.dao.note = self.note_entry.get_text()
        self.dao.righecommessa = righe_
        if chiusura:
            self.dao.data_fine = datetime.datetime.now()
        self.dao.persist()
        self.clear()
