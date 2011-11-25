# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas   <andrea@promotux.it>
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
from promogest.dao.PersonaGiuridica import PersonaGiuridica_
from promogest import Environment
import promogest.dao.Fornitore
from promogest.dao.Fornitore import Fornitore
from promogest.dao.DaoUtils import *
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *


class AnagraficaFornitoriFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica dei fornitori """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                                  anagrafica,
                                  'anagrafica_fornitori_filter_vbox',
                                  gladeFile='_ricerca_fornitori.glade')
        self._widgetFirstFocus = self.ragione_sociale_filter_entry
        self.orderBy = 'ragione_sociale'
        persona_giuridica=Table('persona_giuridica', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        fornitore=Table('fornitore', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        self.joinT = join(fornitore, persona_giuridica)
        self.ricerca_avanzata_fornitori_filter_hbox.destroy()
        self.ricerca_avanzata_fornitori_filter_vbox.destroy()


    def draw(self):
        """ Disegno la treeview e gli altri oggetti della gui """
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "codice_column":
            return self._changeOrderBy(column,(None,PersonaGiuridica_.codice))
        if column.get_name() == "ragione_sociale_column":
            return self._changeOrderBy(column,(None,PersonaGiuridica_.ragione_sociale))

    def clear(self):
        # Annullamento filtro
        self.codice_filter_entry.set_text('')
        self.ragione_sociale_filter_entry.set_text('')
        self.insegna_filter_entry.set_text('')
        self.cognome_nome_filter_entry.set_text('')
        self.localita_filter_entry.set_text('')
        self.codice_fiscale_filter_entry.set_text('')
        self.partita_iva_filter_entry.set_text('')
        fillComboboxCategorieFornitori(self.id_categoria_fornitore_filter_combobox, True)
        self.id_categoria_fornitore_filter_combobox.set_active(0)
        self.refresh()

    def on_filter_entry_changed(self, text):
        stringa = text.get_text()
        def bobo():
            self.refresh()
        gobject.idle_add(bobo)

    def refresh(self):
        # Aggiornamento TreeView
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        ragioneSociale = prepareFilterString(self.ragione_sociale_filter_entry.get_text())
        insegna = prepareFilterString(self.insegna_filter_entry.get_text())
        cognomeNome = prepareFilterString(self.cognome_nome_filter_entry.get_text())
        localita = prepareFilterString(self.localita_filter_entry.get_text())
        partitaIva = prepareFilterString(self.partita_iva_filter_entry.get_text())
        codiceFiscale = prepareFilterString(self.codice_fiscale_filter_entry.get_text())
        idCategoria = findIdFromCombobox(self.id_categoria_fornitore_filter_combobox)

        def filterCountClosure():
            return Fornitore().count(codice=codice,
                                    ragioneSociale=ragioneSociale,
                                    insegna=insegna,
                                    cognomeNome=cognomeNome,
                                    localita=localita,
                                    partitaIva=partitaIva,
                                    codiceFiscale=codiceFiscale,
                                    idCategoria=idCategoria)

        self._filterCountClosure = filterCountClosure
        self.numRecords = self.countFilterResults()
        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Fornitore().select(orderBy=self.orderBy,
                                                    codice=codice,
                                                    ragioneSociale=ragioneSociale,
                                                    insegna=insegna,
                                                    cognomeNome=cognomeNome,
                                                    localita=localita,
                                                    partitaIva=partitaIva,
                                                    codiceFiscale=codiceFiscale,
                                                    idCategoria=idCategoria,
                                                    offset=offset,
                                                    batchSize=batchSize)

        self._filterClosure = filterClosure

        fors = self.runFilter()

        self.filter_listore.clear()

        for f in fors:
            pvcf = ''
            if (f.ragione_sociale or '') == '':
                pvcf = (f.codice_fiscale or '')
            else:
                pvcf = (f.partita_iva or '')
            self.filter_listore.append((f,
                                        (f.codice or ''),
                                        (f.ragione_sociale or ''),
                                        (f.cognome or '') + ' ' + (f.nome or ''),
                                        (f.sede_operativa_localita or ''),
                                        pvcf))
