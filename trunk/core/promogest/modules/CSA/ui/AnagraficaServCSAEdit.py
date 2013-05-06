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


from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.dao.Fornitore import Fornitore
from promogest.modules.CSA.dao.ServCSA import ServCSA


class AnagraficaServCSAEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica dei servizi CSA
    """
    def __init__(self, anagrafica, daoFrom=None, tipo="Cliente"):
        AnagraficaEdit.__init__(self,
                anagrafica,
                'Gestione Servizi CSA',
                root='anagrafica_serv_csa_detail_vbox',
                path='CSA/gui/_anagrafica_serv_csa_elements.glade',
                isModule=True)
        self._widgetFirstFocus = self.provv_ArticoloSearchWidget
        self.anagrafica = anagrafica

        self.daoFrom = daoFrom
        self.tipo = tipo

    def draw(self, cplx=False):
        """ Funzione che "disegna l'interfaccia, devi annullare alcune combo
        a seconda di cosa richiama la finestra...iniziamo dal caso cliente
        """
        return

    def setDao(self, dao):
        """ Si istanzia un nuovo DAO o nuovo o prelevato dalla Treeview
        principale
        """
        if dao is None:
            self.dao = ServCSA()
        else:
            self.dao = dao
        self._refresh()
        return self.dao

    def _refresh(self):
        """Funzione che rinfresca la UI all'apertura e dopo alcune operazioni
        di modifica
        """
        if self.dao:
            self.valore_provv_entry.set_value(mN(self.dao.provv.valore_provv,1))
        else:
            self.valore_provv_entry.set_text("")

        self.tipo_provv_euro_radiobutton.set_active(tippo)
        self.provv_ClienteSearchWidget.setId(self.daoFrom.id)
        self.provv_FornitoreSearchWidget.setId(self.dao.id_persona_giuridica_to)
        self.provv_ArticoloSearchWidget.setId(self.dao.id_articolo)


    def clear(self):
        """ Funzione di reset o pulizia della UI """
        return

    def saveDao(self, tipo=None):
        """ Si effettuano controlli di coerenza, eventuale presenza
        di campi obbligatori ei provvedere a salvare il record dopo
        aver assegnato i valori necessari
        """
        provv_valore = self.valore_provv_entry.get_value()
        if self.tipo_provv_euro_radiobutton.get_active():
            tippo = "€"
        else:
            tippo = "%"
        provv_tipo = tippo
        self.__dao_provv.valore_provv = provv_valore
        self.__dao_provv.tipo_provv = provv_tipo
        self.__dao_provv.persist()
        self.clear()
