# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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

from promogest.ui.AnagraficaSemplice import \
                Anagrafica, AnagraficaDetail, AnagraficaFilter
from promogest.dao.Banca import Banca
from promogest.ui.utils import prepareFilterString


class AnagraficaBanche(Anagrafica):
    """ Anagrafica banche """

    def __init__(self):
        Anagrafica.__init__(self, 'Promogest - Anagrafica banche',
                            '_Banche',
                            AnagraficaBancheFilter(self),
                            AnagraficaBancheDetail(self))

    def draw(self):
        self.filter.denominazione_column.get_cells()[0].set_data(
                                                        'max_length', 200)
        self.filter.agenzia_column.get_cells()[0].set_data('max_length', 200)
        self.filter.iban_column.get_cells()[0].set_data('max_length', 30)
        self.filter.abi_column.get_cells()[0].set_data('max_length', 30)
        self.filter.cab_column.get_cells()[0].set_data('max_length', 30)
        self._treeViewModel = self.filter.filter_listore
        self.refresh()

    def refresh(self):
        # Aggiornamento TreeView
        denominazione = prepareFilterString(
            self.filter.denominazione_filter_entry.get_text())
        agenzia = prepareFilterString(
            self.filter.agenzia_filter_entry.get_text())
        iban = prepareFilterString(self.filter.iban_filter_entry.get_text())
        abi = prepareFilterString(self.filter.abi_filter_entry.get_text())
        cab = prepareFilterString(self.filter.cab_filter_entry.get_text())
        bic_swift = prepareFilterString(
            self.filter.bic_swift_filter_entry.get_text())
        self.numRecords = Banca().count(denominazione=denominazione,
                                                    agenzia=agenzia,
                                                    iban=iban,
                                                    abi=abi,
                                                    cab=cab,
                                                    bic_swift=bic_swift)
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Banca().select(denominazione=denominazione,
                                            agenzia=agenzia,
                                            iban=iban,
                                            abi=abi,
                                            cab=cab,
                                            bic_swift=bic_swift,
                                            orderBy=self.orderBy,
                                            offset=self.offset,
                                            batchSize=self.batchSize)

        self._filterClosure = filterClosure

        bans = self.runFilter()

        self._treeViewModel.clear()

        for b in bans:
            self._treeViewModel.append((b,
                                        (b.denominazione or ''),
                                        (b.agenzia or ''),
                                        (b.iban or ''),
                                        (b.abi or ''),
                                        (b.cab or ''),
                                        (b.bic_swift or '')))


class AnagraficaBancheFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle banche """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_banche_filter_table',
                                  gladeFile='_anagrafica_banche_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry

    def _reOrderBy(self, column):
        if column.get_name() == "denominazione_column":
            return self._anagrafica._changeOrderBy(
                column, (None, Banca.denominazione))
        elif column.get_name() == "agenzia_column":
            return self._anagrafica._changeOrderBy(
                column, (None, Banca.agenzia))
        elif column.get_name() == "iban_column":
            return self._anagrafica._changeOrderBy(
                column, (None, Banca.iban))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.agenzia_filter_entry.set_text('')
        self.iban_filter_entry.set_text('')
        self.abi_filter_entry.set_text('')
        self.cab_filter_entry.set_text('')
        self.bic_swift_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()
        self._anagrafica.refresh()


class AnagraficaBancheDetail(AnagraficaDetail):
    """ Dettaglio dell'anagrafica delle banche """

    def __init__(self, anagrafica):
        pass

    def setDao(self, dao):
        if dao is None:
            self.dao = Banca()
        else:
            self.dao = dao

    def updateDao(self):
        self.dao = Banca().getRecord(id=self.dao.id)
