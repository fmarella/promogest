# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

from decimal import *
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.modules.GestioneCommesse.dao.TestataCommessa import TestataCommessa
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.Ricerca import Ricerca


class AnagraficaCommesseFilter(AnagraficaFilter):
    """ Filtro per la ricerca nella gestione commesse"""

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          root='anagrafica_commessa_filter_table',
                          path='GestioneCommesse/gui/_anagrafica_commessa_elements.glade',
                          isModule=True)
        self._widgetFirstFocus = self.numero_filter_entry
        self.da_data_inizio_datetimewidget.set_text('01/01/' + Environment.workingYear)


    def draw(self):
        """ """
        self.refresh()

    def clear(self):
        # Annullamento filtro
        self.da_data_inizio_datetimewidget.set_text('01/01/' + Environment.workingYear)
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
            return TestataCommessa().select(
                numero=numero,
                daDataInizio = da_data_inizio,
                aDataInizio = a_data_inizio,
                daDataFine = da_data_fine,
                aDataFine = a_data_fine,
                orderBy=self.orderBy,
                offset=offset,
                batchSize=batchSize)
        self._filterClosure = filterClosure

        valis = self.runFilter()
        self.commesse_filter_listore.clear()
        for i in valis:
            self.commesse_filter_listore.append((i,
                                        (str(i.numero) or ''),
                                        (dateToString(i.data_inizio) or ''),
                                        (dateToString(i.data_fine) or ''),
                                        i.cliente,
                                        i.denominazione,
                                        i.stadio_commessa,
                                        i.articolo))

class RicercaCommessa(Ricerca):
    """ Ricerca clienti """
    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca commessa',
                         AnagraficaCommesseFilter(self))

    def insert(self, toggleButton, returnWindow):

        def refresh():
            self.filter.refresh()
            self.filter.denominazione_filter_entry.grab_focus()

        anag = AnagraficaCommesse()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)
        anag.on_record_new_activate(anag.record_new_button)
