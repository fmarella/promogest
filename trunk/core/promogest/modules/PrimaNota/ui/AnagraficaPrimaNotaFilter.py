# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from promogest.dao.TestataPrimaNota import TestataPrimaNota
from promogest.dao.RigaPrimaNota import RigaPrimaNota
from promogest.dao.Banca import Banca
from promogest.dao.RigaPrimaNotaTestataDocumentoScadenza import RigaPrimaNotaTestataDocumentoScadenza
from promogest.lib.relativedelta import relativedelta
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaPrimaNotaFilter(AnagraficaFilter):
    """ Filtro per la ricerca nella prim nota cassa """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_prima_nota_filter_table',
                          gladeFile='_anagrafica_primanota_elements.glade')
        self._widgetFirstFocus = self.numero_filter_entry
        self.da_data_inizio_datetimewidget.set_text('01/01/' + Environment.workingYear+" 00:00")
        self.checkAnnoPrimaNota()

    def checkAnnoPrimaNota(self):

        ddd = TestataPrimaNota().select(daDataInizio=stringToDate("01/01/"+str(int(Environment.workingYear)-1)),
        aDataInizio=stringToDate("31/12/"+str(int(Environment.workingYear)-1)),
        batchSize=None)
        for dd in ddd:
            if not dd.data_fine :
                messageInfo(msg= """ATTENZIONE!!!
C'è una Prima nota Aperta dell'anno scorso. Adesso Verrà chiusa.
Premendo Nuovo se ne creerà una al primo Gennaio del corrente anno di lavoro""")
                dd.data_fine = stringToDate("31/12/"+str(int(Environment.workingYear)-1))
                dd.persist()

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
            return TestataPrimaNota().count(numero=numero,
                                daDataInizio = da_data_inizio,
                                aDataInizio = a_data_inizio,
                                daDataFine = da_data_fine,
                                aDataFine = a_data_fine)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return TestataPrimaNota().select(numero=numero,
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
