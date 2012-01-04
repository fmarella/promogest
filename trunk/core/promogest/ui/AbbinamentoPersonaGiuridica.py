# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.dao.PersonaGiuridicaPersonaGiuridica import PersonaGiuridicaPersonaGiuridica
from promogest.dao.PersonaGiuridica import PersonaGiuridica_ as PersonaGiuridica
from promogest.modules.RuoliAzioni.dao.Role import Role

class AbbinamentoPersonaGiuridica(GladeWidget):
    """ Classe per la gestione degli scontrini emessi """

    def __init__(self, dao):
        self._dao_pg = dao

        GladeWidget.__init__(self, 'abbinamento_pg_window',
                fileName="abbinamento_persone_giuridiche.glade")
        self._window = self.abbinamento_pg_window
        self.placeWindow(self._window)
        self.draw()

    def draw(self):
        self.tipiDict = {"":None,
                "FORNITORE":"Fornitore",
                "VETTORE":"Vettore",
                "CLIENTE":"Cliente",
                "AGENTE":"Agente"}
        for t in self.tipiDict.keys():
            self.abbinamento_pg_listore.append((t,))
            self.riferimento_pg_listore.append((t,))

        res = Role().select(offset=None,batchSize=None)
        for u in res:
            if u.name =="Admin":
                continue
            else:
                self.abbinamento_pg_listore.append((u.name.upper(),))
                self.riferimento_pg_listore.append((u.name.upper(),))
        self._refresh()

    def _refresh(self):
        """ Uso l'id_dao_pg come id figlio e vedo chi è il suo abbinamento
        e poi faccio una query come id_dao_pg e vedo chi sono i suoi figli
        """
        self.abbinamento_righe_pg_listore.clear()
        self.riferimento_righe_pg_listore.clear()

        padre = PersonaGiuridicaPersonaGiuridica().select(idPersonaGiuridica=self._dao_pg, batchSize=None)
        figli = PersonaGiuridicaPersonaGiuridica().select(idPersonaGiuridicaAbbinata=self._dao_pg, batchSize=None)
        for a in padre:
            p = PersonaGiuridica().getRecord(id=a.id_persona_giuridica_abbinata)
            self.abbinamento_righe_pg_listore.append((p,
                p.ragione_sociale or "",
                p.cognome or "",
                p.nome or ""))

        for a in figli:
            p = PersonaGiuridica().getRecord(id=a.id_persona_giuridica)
            self.riferimento_righe_pg_listore.append((p,
                p.ragione_sociale or "",
                p.cognome or "",
                p.nome or ""))

# ABBINAMENTO

    def on_rimuovi_abbinamento_pg_button_clicked(self, button):
        """ Rimuovo la riga selezionata"""
        sel = self.abbinamento_righe_pg_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.rigaIter = model[iterator]
        self.abbinamento_righe_pg_listore.remove(iterator)

    def on_abbinamento_trova_button_clicked(self, button):
        """ TODO : Farsi passare il tipo di pg anag secondaria dalla
        combo per inizializzare la ricerca in modo corretto"""
        def returnDao(anagWindow):
            if anag.dao:
                self.dao_temp = anag.dao
                self.abbinamento_righe_pg_listore.append((anag.dao,
                    anag.dao.ragione_sociale or "",
                    anag.dao.cognome or "",
                    anag.dao.nome or ""))
            else:
                self.dao_temp = None

        self.tipo_dao = self.abbinamento_pg_listore.get_value(self.abbinamento_pg_combobox.get_active_iter(), 0).lower()
        if self.tipo_dao == "CLIENTE".lower():
            from promogest.ui.SimpleSearch.RicercaClienti import RicercaClienti
            anag = RicercaClienti()
        elif self.tipo_dao =="VETTORE".lower():
            from promogest.ui.SimpleSearch.RicercaVettori import RicercaVettori
            anag = RicercaVettori()
        elif self.tipo_dao =="AGENTE".lower():
            from promogest.ui.SimpleSearch.RicercaAgenti import RicercaAgenti
            anag = RicercaAgenti()
        elif self.tipo_dao =="FORNITORE".lower():
            from promogest.ui.SimpleSearch.RicercaFornitori import RicercaFornitori
            anag = RicercaFornitori()
        else:
            from promogest.ui.SimpleSearch.RicercaAnagraficaSecondaria import RicercaAnagraficaSecondaria
            anag = RicercaAnagraficaSecondaria(tipo_dao=self.tipo_dao)
        anagWindow = anag.getTopLevel()
        anagWindow.show_all()
        anagWindow.connect("hide",returnDao)

# RIFERIMENTO

    def on_rimuovi_riferimento_pg_button_clicked(self, button):
        """ Rimuovo la riga selezionata"""
        sel = self.riferimento_righe_pg_treeview.get_selection()
        (model, iterator) = sel.get_selected()
        self.rigaIter = model[iterator]
        self.riferimento_righe_pg_listore.remove(iterator)

    def on_riferimento_trova_button_clicked(self, button):

        def returnDao(anagWindow):
            if anag.dao:
                self.dao_temp = anag.dao
                self.riferimento_righe_pg_listore.append((anag.dao,
                    anag.dao.ragione_sociale or "",
                    anag.dao.cognome or "",
                    anag.dao.nome or ""))
            else:
                self.dao_temp = None


        self.tipo_dao = self.riferimento_pg_listore.get_value(self.riferimento_pg_combobox.get_active_iter(), 0).lower()
        if self.tipo_dao == "CLIENTE".lower():
            from promogest.ui.SimpleSearch.RicercaClienti import RicercaClienti
            anag = RicercaClienti()
        elif self.tipo_dao =="VETTORE".lower():
            from promogest.ui.SimpleSearch.RicercaVettori import RicercaVettori
            anag = RicercaVettori()
        elif self.tipo_dao =="AGENTE".lower():
            from promogest.ui.SimpleSearch.RicercaAgenti import RicercaAgenti
            anag = RicercaAgenti()
        elif self.tipo_dao =="FORNITORE".lower():
            from promogest.ui.SimpleSearch.RicercaFornitori import RicercaFornitori
            anag = RicercaFornitori()
        else:
            from promogest.ui.SimpleSearch.RicercaAnagraficaSecondaria import RicercaAnagraficaSecondaria
            print "quiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", self.tipo_dao
            anag = RicercaAnagraficaSecondaria(tipo_dao=self.tipo_dao)
        anagWindow = anag.getTopLevel()
        anagWindow.show_all()
        anagWindow.connect("hide",returnDao)


    def clear(self):
        self.quantita_componente_kit_entry.set_text("")
        self.note_componente_kit_entry.set_text("")
        self.data_aggiunta_componente_datewidget.set_text("")
        self.id_articolo_componente_customcombobox.set_active(-1)


    def on_chiudi_abbinamento_pg_button_clicked(self, button):
        padre = PersonaGiuridicaPersonaGiuridica().select(idPersonaGiuridica=self._dao_pg, batchSize=None)
        for p in padre:
            p.delete()
        #print "PAAAAAAAAAAAAAAAAADRE", padre
        figli = PersonaGiuridicaPersonaGiuridica().select(idPersonaGiuridicaAbbinata=self._dao_pg, batchSize=None)
        for p in figli:
            p.delete()
        #print "FIGLIIIIIIIIIIIIIIIIIIIIIIIIIIIIII", figli
        # QUI cancello i vecchi prima salvare di nuovo
        for m in self.abbinamento_righe_pg_listore:
            print "ABBI", m, m[0].id
            a = PersonaGiuridicaPersonaGiuridica()
            a.id_persona_giuridica = self._dao_pg
            a.id_persona_giuridica_abbinata = m[0].id
            a.persist()
        for m in self.riferimento_righe_pg_listore:
            print "RIFFE", m, m[0].id
            a = PersonaGiuridicaPersonaGiuridica()
            a.id_persona_giuridica = m[0].id
            a.id_persona_giuridica_abbinata = self._dao_pg
            a.persist()
        self.destroy()

