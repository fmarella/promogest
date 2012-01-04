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

from decimal import *
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.modules.GestioneCommesse.dao.TestataCommessa import TestataCommessa
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaCommesseFilter(AnagraficaFilter):
    """ Filtro per la ricerca nella gestione commesse"""

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                          anagrafica,
                          'anagrafica_commessa_filter_table',
                          gladeFile='GestioneCommesse/gui/_anagrafica_commessa_elements.glade',
                          module=True)
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
                                        i.cliente,
                                        i.denominazione,
                                        (dateToString(i.data_inizio) or ''),
                                        (dateToString(i.data_fine) or ''),
                                        i.stadio_commessa,
                                        i.articolo))
