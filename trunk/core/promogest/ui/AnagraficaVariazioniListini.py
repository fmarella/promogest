# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from promogest.ui.gtk_compat import *
from AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.dao.Listino import Listino
from promogest.dao.VariazioneListino import VariazioneListino
from promogest.lib.relativedelta import relativedelta
from promogest.lib.utils import *
from utilsCombobox import *


class AnagraficaVariazioniListini(Anagrafica):
    """ Anagrafica Variazioni Listini """

    def __init__(self, idListino = None, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica Variazioni Listini',
                            recordMenuLabel='_Variazioni Listini',
                            filterElement=AnagraficaVariazioniListiniFilter(self),
                            htmlHandler=AnagraficaVariazioniListiniHtml(self),
                            reportHandler=AnagraficaVariazioniListiniReport(self),
                            editElement=AnagraficaVariazioniListiniEdit(self),
                            aziendaStr=aziendaStr)
        self.idListino = idListino

class AnagraficaVariazioniListiniFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle aliquote IVA """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          root='anagrafica_variazioni_listini_filter_table',
                          path='_anagrafica_variazioni_listini_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Denominazione', renderer, text=2, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'denominazione'))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Listino', renderer, text=3, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None, 'listino'))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(70)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data Inizio', renderer, text=4, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None, 'data_inizio'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Data Fine', renderer, text=5, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None, 'data_fine'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Valore', renderer, text=6, background=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None, 'valore'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str,str, str, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        fillComboboxListini(self.listino_filter_ccb.combobox)

        self.refresh()

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.listino_filter_ccb.set_active(-1)
        self.da_data_inizio_datetimewidget.set_text('')
        self.a_data_inizio_datetimewidget.set_text('')
        self.da_data_fine_datetimewidget.set_text('')
        self.a_data_fine_datetimewidget.set_text('')
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        id_listino = findIdFromCombobox(self.listino_filter_ccb.combobox)
        da_data_inizio = stringToDateTime(emptyStringToNone(self.da_data_inizio_datetimewidget.get_text()))
        a_data_inizio = stringToDateTime(emptyStringToNone(self.a_data_inizio_datetimewidget.get_text()))
        da_data_fine = stringToDateTime(emptyStringToNone(self.da_data_fine_datetimewidget.get_text()))
        a_data_fine = stringToDateTime(emptyStringToNone(self.a_data_fine_datetimewidget.get_text()))

        def filterCountClosure():
            return VariazioneListino().count(denominazione=denominazione,
                                idListino=id_listino,
                                daDataInizio = da_data_inizio,
                                aDataInizio = a_data_inizio,
                                daDataFine = da_data_fine,
                                aDataFine = a_data_fine)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return VariazioneListino().select(denominazione=denominazione,
                                            idListino=id_listino,
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
#        one_day = relativedelta(days=1)
        for i in valis:
            if i.tipo == "moltiplicatore":
                a = i.valore.split("|")
                valore = a[0]+"x"+a[1] +" "+ a[2] +" articolo"
            else:
                valore = i.valore + " " + i.tipo
            col = None
            if i.data_fine > datetime.datetime.today():
                col = "green"
            listino_denominazione = ''
            if i.id_listino:
                listino_denominazione = Listino().select(idListino=i.id_listino)[0].denominazione
            self._treeViewModel.append((i,col,
                                        (i.denominazione or ''),
                                        (listino_denominazione),
                                        (dateTimeToString(i.data_inizio) or ''),
                                        (dateTimeToString(i.data_fine) or ''),
                                        (valore or 0)))


class AnagraficaVariazioniListiniHtml(AnagraficaHtml):

    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'variazioni_listini',
                                'Dettaglio variazioni listini')


class AnagraficaVariazioniListiniReport(AnagraficaReport):

    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco delle Variazioni Listino',
                                  defaultFileName='variazioni_listini',
                                  htmlTemplate='variazioni_listini',
                                  sxwTemplate='variazioni_listini')


class AnagraficaVariazioniListiniEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle variazioni listino """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'Dati Variazioni Listino.',
                                root='anagrafica_variazioni_listini_detail_table',
                                path='_anagrafica_variazioni_listini_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry
        self.anagrafica = anagrafica

    def draw(self, cplx=False):
        self.primo_moltiplicatore_entry.set_sensitive(False)
        self.secondo_moltiplicatore_entry.set_sensitive(False)
        self.stesso_articolo_radiobutton.set_sensitive(False)
        self.ogni_articolo_radiobutton.set_sensitive(False)
        fillComboboxListini(self.listino_ccb.combobox)

    def on_a_sconto_radiobutton_toggled(self, radiobutton):
        if not self.a_sconto_radiobutton.get_active():
            self.primo_moltiplicatore_entry.set_sensitive(True)
            self.secondo_moltiplicatore_entry.set_sensitive(True)
            self.stesso_articolo_radiobutton.set_sensitive(True)
            self.ogni_articolo_radiobutton.set_sensitive(True)
            self.a_valore_scontowidget.set_sensitive(False)
            self.plus_radio.set_sensitive(False)
            self.minus_radio.set_sensitive(False)
        else:
            self.primo_moltiplicatore_entry.set_sensitive(False)
            self.secondo_moltiplicatore_entry.set_sensitive(False)
            self.stesso_articolo_radiobutton.set_sensitive(False)
            self.ogni_articolo_radiobutton.set_sensitive(False)
            self.a_valore_scontowidget.set_sensitive(True)
            self.plus_radio.set_sensitive(True)
            self.minus_radio.set_sensitive(True)

    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = VariazioneListino()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = VariazioneListino().getRecord(id=dao.id)
        self._refresh()
        return self.dao

    def _clear(self):
        self.denominazione_entry.set_text('')
        findComboboxRowFromId(self.listino_ccb.combobox, -1)
        self.data_inizio_datetimewidget.set_text('')
        self.data_fine_datetimewidget.set_text('')
        self.a_valore_scontowidget.set_text('')
        self.primo_moltiplicatore_entry.set_text('')
        self.secondo_moltiplicatore_entry.set_text('')
        self.priorita_checkbutton.set_active(True)
        self.a_sconto_radiobutton.set_active(True)

    def _refresh(self):
        self._clear()
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        findComboboxRowFromId(self.listino_ccb.combobox, self.dao.id_listino or -1)
        self.data_inizio_datetimewidget.set_text(dateTimeToString(self.dao.data_inizio) or '')
        self.data_fine_datetimewidget.set_text(dateTimeToString(self.dao.data_fine) or '')
        if self.dao.id:
            if self.dao.tipo == "percentuale" or self.dao.tipo == "valore":
                self.a_valore_scontowidget.set_text(self.dao.valore or "")
                self.a_valore_scontowidget.tipoSconto = self.dao.tipo
                self.a_sconto_radiobutton.set_active(True)
            else:
                self.a_moltiplicatore_radiobutton.set_active(True)
                if self.dao.valore:
                    values = self.dao.valore.split("|")
                    self.primo_moltiplicatore_entry.set_text(values[0] or "")
                    self.secondo_moltiplicatore_entry.set_text(values[1] or "" )
                    if values and values[2] == "stesso":
                        self.stesso_articolo_radiobutton.set_active(True)
                    else:
                        self.ogni_articolo_radiobutton.set_active(True)
            self.on_a_sconto_radiobutton_toggled(self.a_sconto_radiobutton )
        self.priorita_checkbutton.set_active(self.dao.priorita or True)


    def saveDao(self, tipo=None):
        if (self.denominazione_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)

        if self.data_fine_datetimewidget.get_text() == "":
            obligatoryField(self.dialogTopLevel, self.data_fine_datetimewidget)

        if self.data_inizio_datetimewidget.get_text() == "":
            obligatoryField(self.dialogTopLevel, self.data_inizio_datetimewidget)

        self.dao.data_inizio = stringToDateTime(self.data_inizio_datetimewidget.get_text())
        self.dao.data_fine = stringToDateTime(self.data_fine_datetimewidget.get_text())

        self.dao.id_listino = findIdFromCombobox(self.listino_ccb.combobox)

        if self.dao.data_inizio > self.dao.data_fine:
            messageInfo(msg="La data di inizio dev'essere successiva alla data di fine ...valore impossibile!!!")
            raise Exception, 'Operation aborted:La data di inizio dev essere successiva alla data di fine'


        if str(self.dao.data_fine - self.dao.data_inizio) == "0:00:00":
            messageInfo(msg="La durata della variazione è pari a zero ...valore impossibile!!!")
            raise Exception, 'Operation aborted: La durata della variazione è pari a zero ...valore impossibile'

        check1 = VariazioneListino().select(aDataFine = emptyStringToNone(self.dao.data_inizio))
        if check1:
            messageInfo(msg="La data di inizio di questa offerta è precedente alla data di fine di un'altra ...valore impossibile!!")
            raise Exception, 'Operation aborted: La data di inizio di questa offerta è precedente alla data di fine di un altra ...valore impossibile!!'


        if self.a_sconto_radiobutton.get_active():
            if (self.a_valore_scontowidget.get_text() == ''):
                obligatoryField(self.dialogTopLevel, self.a_valore_scontowidget)

            self.dao.tipo = self.a_valore_scontowidget.tipoSconto
            self.dao.valore = self.a_valore_scontowidget.get_text()
            if self.plus_radio.get_active():
                self.dao.segno = "+"
            else:
                self.dao.segno = "-"
        else:
            if self.primo_moltiplicatore_entry.get_text() == '':
                obligatoryField(self.dialogTopLevel, self.primo_moltiplicatore_entry)
            if self.secondo_moltiplicatore_entry.get_text() == '':
                obligatoryField(self.dialogTopLevel, self.secondo_moltiplicatore_entry)

            a = self.primo_moltiplicatore_entry.get_text()
            b = self.secondo_moltiplicatore_entry.get_text()
            if self.stesso_articolo_radiobutton.get_active():
                c = "stesso"
            else:
                c= "ogni"
            self.dao.valore = a+"|"+b+"|"+c
            self.dao.tipo = "moltiplicatore"
        self.dao.denominazione = self.denominazione_entry.get_text()
        #self.dao.id_listino = self.anagrafica.idListino
        self.dao.priorita = self.priorita_checkbutton.get_active()
        self.dao.persist()
