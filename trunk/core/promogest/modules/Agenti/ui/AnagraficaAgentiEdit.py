# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Authors: Francesco Meloni  <francesco@promotux.it>
#             Andrea Argiolas   <andrea@promotux.it>
#             Francesco Marella <francesco.marella@gmail.com>

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


from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.modules.Agenti.dao.Agente import Agente, getNuovoCodiceAgente
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaAgentiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica degli agenti """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_agenti_detail_table',
                                'Dati agente',
                                gladeFile='Agenti/gui/_anagrafica_agenti_elements.glade',
                                module=True)
        self._widgetFirstFocus = self.codice_entry


    def draw(self, cplx=False):
        self.nome_entry.destroy()
        self.cognome_entry.destroy()
        self.insegna_entry.destroy()
        self.insegna_label.destroy()
        self.cognome_label.destroy()
        self.nome_label.destroy()
        pass


    def on_codice_entry_icon_press(self,entry,position,event):
        if position.value_nick == "primary":
            codice = getNuovoCodiceAgente()
            self.codice_entry.set_text(codice)

    def setDao(self, dao):
        """ Istanzia un  oggetto nuovo se non presente """
        self.dao = dao
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = Agente()
            self.dao.codice = getNuovoCodiceAgente()
        self._refresh()

    def _refresh(self):
        """ Aggiorna gli oggetti della gui """
        if self.dao.ragione_sociale:
            rag_soc = self.dao.ragione_sociale
        elif self.dao.cognome or self.dao.nome:
            rag_soc = str(self.dao.cognome) + " " + str(self.dao.nome)
        elif self.dao.insegna:
            rag_soc = self.dao.insegna
        else:
            rag_soc = ""
        self.codice_entry.set_text(self.dao.codice or '')
        self.ragione_sociale_entry.set_text(rag_soc)
#        self.insegna_entry.set_text(self.dao.insegna or '')
#        self.cognome_entry.set_text(self.dao.cognome or '')
#        self.nome_entry.set_text(self.dao.nome or '')
        self.indirizzo_sede_operativa_entry.set_text(self.dao.sede_operativa_indirizzo or '')
        self.cap_sede_operativa_entry.set_text(self.dao.sede_operativa_cap or '')
        self.localita_sede_operativa_entry.set_text(self.dao.sede_operativa_localita or '')
        self.provincia_sede_operativa_entry.set_text(self.dao.sede_operativa_provincia or '')
        self.indirizzo_sede_legale_entry.set_text(self.dao.sede_legale_indirizzo or '')
        self.cap_sede_legale_entry.set_text(self.dao.sede_legale_cap or '')
        self.localita_sede_legale_entry.set_text(self.dao.sede_legale_localita or '')
        self.provincia_sede_legale_entry.set_text(self.dao.sede_legale_provincia or '')
        self.codice_fiscale_entry.set_text(self.dao.codice_fiscale or '')
        self.partita_iva_entry.set_text(self.dao.partita_iva or '')
        self.percentuale_entry.set_text(str(self.dao.percentuale) or '')


    def saveDao(self, tipo=None):
        """ Save data to DB """
        self.dao.codice = self.codice_entry.get_text().upper()
#        self.dao.codice = omogeneousCode(section="Agenti", string=self.dao.codice )
        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()
#        self.dao.insegna = self.insegna_entry.get_text()
#        self.dao.cognome = self.cognome_entry.get_text()
#        self.dao.nome = self.nome_entry.get_text()
        if (self.dao.codice and (self.dao.ragione_sociale or self.dao.insegna or self.dao.cognome or self.dao.nome)) =='':
            msg="""Il codice è obbligatorio!
    Inserire almeno un campo a scelta tra:
    ragione sociale, insegna, cognome o nome """
            messageInfo(msg)
            return
        self.dao.sede_operativa_indirizzo = self.indirizzo_sede_operativa_entry.get_text()
        self.dao.sede_operativa_cap = self.cap_sede_operativa_entry.get_text()
        self.dao.sede_operativa_localita = self.localita_sede_operativa_entry.get_text()
        self.dao.sede_operativa_provincia = self.provincia_sede_operativa_entry.get_text()
        self.dao.sede_legale_indirizzo = self.indirizzo_sede_legale_entry.get_text()
        self.dao.sede_legale_cap = self.cap_sede_legale_entry.get_text()
        self.dao.sede_legale_localita = self.localita_sede_legale_entry.get_text()
        self.dao.sede_legale_provincia = self.provincia_sede_legale_entry.get_text()
        self.dao.codice_fiscale = self.codice_fiscale_entry.get_text()
        if self.dao.codice_fiscale != '':
            codfis = checkCodFisc(self.dao.codice_fiscale)
            if not codfis:
                return
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        if self.dao.partita_iva != '':
            partiva = checkPartIva(self.dao.partita_iva)
            if not partiva:
                return
        if self.percentuale_entry.get_text() and self.percentuale_entry.get_text() != "None":
            self.dao.percentuale = float(self.percentuale_entry.get_text())
        else:
            self.dao.percentuale = float(0)
        self.dao.persist()
