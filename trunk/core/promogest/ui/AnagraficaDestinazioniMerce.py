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

import gtk
import gobject

from AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.Dao import Dao
import promogest.dao.DestinazioneMerce
from promogest.dao.DestinazioneMerce import DestinazioneMerce

from utils import *



class AnagraficaDestinazioniMerce(Anagrafica):
    """ Anagrafica destinazioni merce """

    def __init__(self, idCliente = None, aziendaStr=None):
        self._clienteFissato = (idCliente <> None)
        self._idCliente=idCliente
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica destinazioni merce',
                            recordMenuLabel='_Destinazioni',
                            filterElement=AnagraficaDestinazioniMerceFilter(self),
                            htmlHandler=AnagraficaDestinazioniMerceHtml(self),
                            reportHandler=AnagraficaDestinazioniMerceReport(self),
                            editElement=AnagraficaDestinazioniMerceEdit(self),
                            aziendaStr=aziendaStr)



class AnagraficaDestinazioniMerceFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle destinazioni merce """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_destinazioni_merce_filter_table',
                                  gladeFile='_anagrafica_destinazioni_merce_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.orderBy = 'denominazione'


    def draw(self):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Denominazione', renderer, text=1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'denominazione')
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(250)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Indirizzo', renderer, text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'indirizzo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Localita''', renderer, text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, 'localita')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(200)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.refresh()


    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.indirizzo_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()


    def refresh(self):
        # Aggiornamento TreeView
        idCliente = self._anagrafica._idCliente
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        indirizzo = prepareFilterString(self.indirizzo_filter_entry.get_text())
        localita = prepareFilterString(self.localita_filter_entry.get_text())
        provincia = prepareFilterString(self.provincia_filter_entry.get_text())

        def filterCountClosure():
            return DestinazioneMerce(isList=True).count(idCliente=idCliente,
                                                         denominazione=denominazione,
                                                         indirizzo=indirizzo,
                                                         localita=localita,
                                                         provincia=provincia)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return DestinazioneMerce(isList=True).select(orderBy=self.orderBy,
                                                          idCliente=idCliente,
                                                          denominazione=denominazione,
                                                          indirizzo=indirizzo,
                                                          localita=localita,
                                                          provincia=provincia,
                                                          offset=offset,
                                                          batchSize=batchSize)

        self._filterClosure = filterClosure

        dems = self.runFilter()

        self._treeViewModel.clear()

        for d in dems:
            self._treeViewModel.append((d,
                                        (d.denominazione or ''),
                                        (d.indirizzo or ''),
                                        (d.localita or '')))



class AnagraficaDestinazioniMerceHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'destinazione_merce',
                                'Dettaglio della destinazione merce')



class AnagraficaDestinazioniMerceReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco dei destinazioni merce',
                                  defaultFileName='destinazioni_merce',
                                  htmlTemplate='destinazioni_merce',
                                  sxwTemplate='destinazioni_merce')



class AnagraficaDestinazioniMerceEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica delle destinazioni merce """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_destinazioni_merce_detail_table',
                                'Dati destinazione merce',
                                gladeFile='_anagrafica_destinazioni_merce_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry


    def draw(self):
        pass


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = DestinazioneMerce().getRecord()
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = DestinazioneMerce(id= dao.id).getRecord()
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

        self.dao.id_cliente = self._anagrafica._idCliente
        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.indirizzo = self.indirizzo_entry.get_text()
        self.dao.localita = self.localita_entry.get_text()
        self.dao.cap = self.cap_entry.get_text()
        self.dao.provincia = self.provincia_entry.get_text()
        self.dao.persist()
