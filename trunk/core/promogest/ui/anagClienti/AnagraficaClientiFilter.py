# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas <andrea@promotux.it>
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
from promogest.dao.Cliente import Cliente
from promogest.dao.PersonaGiuridica import PersonaGiuridica_
from promogest.dao.DaoUtils import *
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaClientiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei clienti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  root='anagrafica_clienti_filter_vbox',
                                  path='_ricerca_clienti.glade')
        self._widgetFirstFocus = self.ragione_sociale_filter_entry
        self.orderBy = 'ragione_sociale'
        self.ricerca_avanzata_clienti_filter_hbox.destroy()
        self.ricerca_avanzata_clienti_filter_vbox.destroy()
        self.joinT = None
        #join(cliente, perso_giuri)

    def draw(self):
        """ Disegno la treeview e gli altri oggetti della gui """
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "codice_column":
            return self._changeOrderBy(column, (
                                    None, PersonaGiuridica_.codice))
        if column.get_name() == "ragione_sociale_column":
            return self._changeOrderBy(column, (
                                    None, PersonaGiuridica_.ragione_sociale))

    def clear(self):
        # Annullamento filtro
        self.codice_filter_entry.set_text('')
        self.ragione_sociale_filter_entry.set_text('')
        self.insegna_filter_entry.set_text('')
        self.cognome_nome_filter_entry.set_text('')
        self.localita_filter_entry.set_text('')
        self.provincia_filter_entry.set_text('')
        self.codice_fiscale_filter_entry.set_text('')
        self.partita_iva_filter_entry.set_text('')
        fillComboboxCategorieClienti(
                        self.id_categoria_cliente_filter_combobox, True)
        self.id_categoria_cliente_filter_combobox.set_active(0)
        self.refresh()

    def refresh(self):
        """
        Aggiorno l'interfaccia con i dati filtrati
        """
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        ragioneSociale = prepareFilterString(
                        self.ragione_sociale_filter_entry.get_text())
        insegna = prepareFilterString(self.insegna_filter_entry.get_text())
        cognomeNome = prepareFilterString(
                        self.cognome_nome_filter_entry.get_text())
        localita = prepareFilterString(self.localita_filter_entry.get_text())
        provincia = prepareFilterString(self.provincia_filter_entry.get_text())
        partitaIva = prepareFilterString(
                        self.partita_iva_filter_entry.get_text())
        codiceFiscale = prepareFilterString(
                        self.codice_fiscale_filter_entry.get_text())
        idCategoria = findIdFromCombobox(
                        self.id_categoria_cliente_filter_combobox)

        def filterCountClosure():
            return Cliente().count(codice=codice,
                                    ragioneSociale=ragioneSociale,
                                    insegna=insegna,
                                    cognomeNome=cognomeNome,
                                    localita=localita,
                                    provincia=provincia,
                                    partitaIva=partitaIva,
                                    codiceFiscale=codiceFiscale,
                                    idCategoria=idCategoria)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Cliente().select(orderBy=self.orderBy,
                                    join=self.join,
                                    codice=codice,
                                    ragioneSociale=ragioneSociale,
                                    insegna=insegna,
                                    cognomeNome=cognomeNome,
                                    localita=localita,
                                    provincia=provincia,
                                    partitaIva=partitaIva,
                                    codiceFiscale=codiceFiscale,
                                    idCategoria=idCategoria,
                                    offset=offset,
                                    batchSize=batchSize)

        self._filterClosure = filterClosure

        clis = self.runFilter()

        self.filter_listore.clear()

        for c in clis:
            t = (c.sede_legale_localita + " (" + c.sede_legale_provincia + ")" or
                    c.sede_operativa_localita + " (" + c.sede_operativa_provincia + ")" or "")
            if t == " ()":
                t = ""
            self.filter_listore.append((
                c,
                c.codice,
                c.ragione_sociale or ((c.cognome or '') + ' ' + (c.nome or '')),
                t,
                c.telefono_principale or c.cellulare_principale or c.email_principale or "",
                c.partita_iva or c.codice_fiscale or ""))
