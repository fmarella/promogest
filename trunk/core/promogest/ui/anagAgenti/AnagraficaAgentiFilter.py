# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Authors: Francesco Meloni  <francesco@promotux.it>
#             Andrea Argiolas   <andrea@promotux.it>
#             Francesco Marella <francesco.marella@anche.no>

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
from promogest import Environment
from promogest.dao.daoAgenti.Agente import Agente
from promogest.dao.PersonaGiuridica import PersonaGiuridica_
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.Ricerca import Ricerca


class AnagraficaAgentiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli agenti """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
                            anagrafica,
                            root='anagrafica_agenti_filter_table',
                            path='/Agenti/_anagrafica_agenti_elements.glade',
                            isModule=False)
     ##   self._widgetFirstFocus = self.ragione_sociale_filter_entry
        self.orderBy = 'ragione_sociale'
        persona_giuridica=Table('persona_giuridica', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        agenti=Table('agente', Environment.params['metadata'],schema = Environment.params['schema'], autoload=True)
        self.joinT = join(agenti, persona_giuridica)

    def draw(self):
        """ Disegno la treeview e gli altri oggetti della gui """
        self.clear()

    def _reOrderBy(self, column):
        if column.get_name() == "codice_column":
            return self._changeOrderBy(column,(None,PersonaGiuridica_.codice))
        if column.get_name() == "ragione_sociale_column":
            return self._changeOrderBy(column,(None,PersonaGiuridica_.ragione_sociale))


    def clear(self):
        """ Annullamento filtro"""
        self.codice_filter_entry.set_text('')
        self.ragione_sociale_filter_entry.set_text('')
        self.insegna_filter_entry.set_text('')
        self.cognome_nome_filter_entry.set_text('')
        self.localita_filter_entry.set_text('')
        self.codice_fiscale_filter_entry.set_text('')
        self.partita_iva_filter_entry.set_text('')
        self.percentuale_entry.set_text('')
        self.ragione_sociale_filter_entry.grab_focus()
        self.refresh()


    def refresh(self):
        """ Aggiornamento TreeView"""
        codice = prepareFilterString(self.codice_filter_entry.get_text())
        ragioneSociale = prepareFilterString(self.ragione_sociale_filter_entry.get_text())
        insegna = prepareFilterString(self.insegna_filter_entry.get_text())
        cognomeNome = prepareFilterString(self.cognome_nome_filter_entry.get_text())
        localita = prepareFilterString(self.localita_filter_entry.get_text())
        partitaIva = prepareFilterString(self.partita_iva_filter_entry.get_text())
        codiceFiscale = prepareFilterString(self.codice_fiscale_filter_entry.get_text())

        def filterCountClosure():
            return Agente().count(codice=codice,
                                    ragioneSociale=ragioneSociale,
                                    insegna=insegna,
                                    cognomeNome=cognomeNome,
                                    localita=localita,
                                    partitaIva=partitaIva,
                                    codiceFiscale=codiceFiscale)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return Agente().select(orderBy=self.orderBy,
                                    join=self.join,
                                    codice=codice,
                                    ragioneSociale=ragioneSociale,
                                    insegna=insegna,
                                    cognomeNome=cognomeNome,
                                    localita=localita,
                                    partitaIva=partitaIva,
                                    codiceFiscale=codiceFiscale,
                                    offset=offset,
                                    batchSize=batchSize)

        self._filterClosure = filterClosure

        fors = self.runFilter()

        self.filter_listore.clear()

        for f in fors:
            pvcf = ''
            if (f.ragione_sociale or '') == '':
                pvcf = f.codice_fiscale
            else:
                pvcf = f.partita_iva
            self.filter_listore.append((f,
                                        (f.codice or ''),
                                        (f.ragione_sociale or ''),
                                        (f.cognome or '') + ' ' + (f.nome or ''),
                                        (f.sede_operativa_localita or ''),
                                        pvcf))


def ricercaDaoAgenti(model, keyname):
    cli = Agente().select(ragioneSociale=keyname, batchSize=40)
    for m in cli:
        rag = m.ragione_sociale or m.cognome + " " + m.nome
        model.append(('empty', m.id, rag, m))


class RicercaAgenti(Ricerca):
    """ Ricerca agenti
    """
    def __init__(self):
        Ricerca.__init__(self, 'Promogest - Ricerca agenti',
                         AnagraficaAgentiFilter(self))

    def insert(self, toggleButton, returnWindow):

        def refresh():
            self.filter.refresh()
            self.filter.ragione_sociale_filter_entry.grab_focus()

        from promogest.ui.anagAgenti.AnagraficaAgenti import AnagraficaAgenti
        anag = AnagraficaAgenti()
        anagWindow = anag.getTopLevel()
        showAnagraficaRichiamata(returnWindow, anagWindow, toggleButton, refresh)
        anag.on_record_new_activate(anag.record_new_button)
