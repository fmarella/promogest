# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaMovimentiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nei movimenti """

    def __init__(self, anagrafica):
        """
        FIXME
        @param anagrafica:
        @type anagrafica:
        """
        AnagraficaFilter.__init__(self,
                              anagrafica,
                              root='anagrafica_movimenti_filter_table',
                              path='_ricerca_semplice_movimenti.glade')
        self._widgetFirstFocus = self.da_data_filter_entry
        self.orderBy = 'id'
        self.aa = 1

    def draw(self, cplx=False):
        """
        FIXME
        """
        fillComboboxOperazioni(self.id_operazione_filter_combobox, 'movimento',
                               True)
        self.id_operazione_filter_combobox.set_active(0)
        fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
        if self._anagrafica._magazzinoFissato:
            findComboboxRowFromId(self.id_magazzino_filter_combobox,
                                  self._anagrafica._idMagazzino)
        else:
            self.id_magazzino_filter_combobox.set_active(0)
        self.cliente_filter_radiobutton.connect('toggled',
                                            self.on_filter_radiobutton_toggled)
        self.fornitore_filter_radiobutton.connect('toggled',
                                          self.on_filter_radiobutton_toggled)
        self.cliente_filter_radiobutton.set_active(True)
        self.on_filter_radiobutton_toggled()
        self.clear()


    def _reOrderBy(self, column):
        if column.get_name() == "numero_column":
            self.funzione_ordinamento = None
            return self._changeOrderBy(column, (None, TestataMovimento.numero))
        if column.get_name() == "data_column":
            self.funzione_ordinamento = None
            return self._changeOrderBy(column,
                                       (None, TestataMovimento.data_movimento))
        if column.get_name() == "causale_column":
            self.funzione_ordinamento = None
            return self._changeOrderBy(column, (None, TestataMovimento.operazione))
        if column.get_name() == "cliente_fornitore_column":
            self.aa = -1 * self.aa
            self.funzione_ordinamento = "cliforn"
            self.refresh()
        self._anagrafica.funzione_ordinamento = self.funzione_ordinamento
        self._anagrafica.aa = self.aa


    def clear(self):
        """ FIXME """
        # Annullamento filtro
        self.da_data_filter_entry.set_text('01/01/' + Environment.workingYear)
        self.a_data_filter_entry.set_text('')
        self.da_numero_filter_entry.set_text('')
        self.a_numero_filter_entry.set_text('')
        self.id_operazione_filter_combobox.set_active(0)
        if not self._anagrafica._magazzinoFissato:
            fillComboboxMagazzini(self.id_magazzino_filter_combobox, True)
            self.id_magazzino_filter_combobox.set_active(0)
        self.id_cliente_filter_customcombobox.set_active(0)
        self.id_fornitore_filter_customcombobox.set_active(0)
        self.refresh()

    def refresh(self):
        """  """
        # Aggiornamento TreeView
        daData = stringToDate(self.da_data_filter_entry.get_text())
        aData = stringToDate(self.a_data_filter_entry.get_text())
        daNumero = prepareFilterString(self.da_numero_filter_entry.get_text())
        aNumero = prepareFilterString(self.a_numero_filter_entry.get_text())
        idOperazione = prepareFilterString(findIdFromCombobox(self.id_operazione_filter_combobox))
        idMagazzino = findIdFromCombobox(self.id_magazzino_filter_combobox)
#        idMagazzino = 1
        idCliente = self.id_cliente_filter_customcombobox.getId()
        idFornitore = self.id_fornitore_filter_customcombobox.getId()

        def filterCountClosure():
            """
            """
            return TestataMovimento().count(daNumero=daNumero,
                                                    aNumero=aNumero,
                                                    daParte=None,
                                                    aParte=None,
                                                    daData=daData,
                                                    aData=aData,
                                                    idOperazione=idOperazione,
                                                    idMagazzino=idMagazzino,
                                                    idCliente=idCliente,
                                                    idFornitore=idFornitore)
        self._filterCountClosure = filterCountClosure
        self.numRecords = self.countFilterResults()
        self._refreshPageCount()
        def filterClosure(offset, batchSize):
            """
            """
            return TestataMovimento().select(orderBy=self.orderBy,
                                                 daNumero=daNumero,
                                                 aNumero=aNumero,
                                                 daParte=None,
                                                 aParte=None,
                                                 daData=daData,
                                                 aData=aData,
                                                 idOperazione=idOperazione,
                                                 idMagazzino=idMagazzino,
                                                 idCliente=idCliente,
                                                 idFornitore=idFornitore,
                                                 offset=offset,
                                                 batchSize=batchSize)


        if self.funzione_ordinamento == "cliforn":
            self._filterClosure = filterClosure
            tdoss = self.runFilter(batchSizeForce=True)
            if self.aa < 0:
                tdoss.sort(key=lambda x: x.intestatario.strip().upper())
            else:
                tdoss.sort(key=lambda x: x.intestatario.strip().upper(), reverse=True)
            tdos = tdoss[self.offset:self.batchSize2 + self.offset]
        else:
            self._filterClosure = filterClosure
            tdos = self.runFilter()
        for l in self.filter_listore:
            # print l.iter
            self.filter_listore[l.iter][0] = None
            # self.filter_listore.remove(l.iter)
        self.filter_listore.clear()
        for t in tdos:
            soggetto = ''
            if t.id_cliente is not None:
                soggetto = t.ragione_sociale_cliente or ''
                if soggetto == '':
                    soggetto = (t.cognome_cliente or '') + ' ' + (t.nome_cliente or '')
            elif t.id_fornitore is not None:
                soggetto = t.ragione_sociale_fornitore or ''
                if soggetto == '':
                    soggetto = (t.cognome_fornitore or '') + ' ' + (t.nome_fornitore or '')
            self.filter_listore.append([t,
                                        dateToString(t.data_movimento),
                                        str(t.numero) or "0",
                                        t.operazione or '',
                                        soggetto or '',
                                        t.note_interne or ''])
    def on_filter_radiobutton_toggled(self, widget=None):
        """ FIXME
        """
        if self.cliente_filter_radiobutton.get_active():
            self.id_cliente_filter_customcombobox.set_sensitive(True)
            self.id_cliente_filter_customcombobox.grab_focus()
            self.id_fornitore_filter_customcombobox.set_active(0)
            self.id_fornitore_filter_customcombobox.set_sensitive(False)
        elif self.fornitore_filter_radiobutton.get_active():
            self.id_fornitore_filter_customcombobox.set_sensitive(True)
            self.id_fornitore_filter_customcombobox.grab_focus()
            self.id_cliente_filter_customcombobox.set_active(0)
            self.id_cliente_filter_customcombobox.set_sensitive(False)
