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
from promogest.modules.CSA.dao.ServCSA import ServCSA , t_serv_csa


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
        fillComboboxLuogoInstallazione(self.luogo_installazione_combobox.combobox)
        self.luogo_installazione_combobox.connect('clicked',
                                            on_luogo_installazione_combobox_clicked)
        model = self.manutenzione_combobox.get_model()
        model.clear()
        for t in ["MENSILE","ANNUALE","BIENNALE"]:
            model.append((t,))

    def setDao(self, dao):
        """ Si istanzia un nuovo DAO o nuovo o prelevato dalla Treeview
        principale
        """
        if dao is None:
            self.dao = ServCSA()
        else:
            self.dao = dao
        self._refresh()
        #self.daoDict = self.dao.dictionary(complete=True)
        self.daoDict = dict(t_serv_csa.columns)
        return self.dao

    def _refresh(self):
        """Funzione che rinfresca la UI all'apertura e dopo alcune operazioni
        di modifica
        """
        findComboboxRowFromId(self.luogo_installazione_combobox.combobox, self.dao.id_luogo_installazione)

        #self.tipo_provv_euro_radiobutton.set_active(tippo)
        self.serv_csa_cliente_ClienteSearchWidget.setId(self.dao.id_cliente)
        #self.provv_FornitoreSearchWidget.setId(self.dao.id_persona_giuridica_to)
        #self.provv_ArticoloSearchWidget.setId(self.dao.id_articolo)

    def on_commesse_button_clicked(self, button):
        from promogest.modules.GestioneCommesse.ui.AnagraficaCommesseFilter import RicercaCommessa
        def returnDao(anagWindow):
            if anag.dao:
                self.commesse_button.set_label(anag.dao.denominazione[0:50])
                self.daoDict["id_testata_commessa"] = anag.dao.id
        anag = RicercaCommessa()
        anagWindow = anag.getTopLevel()
        anagWindow.show_all()
        anagWindow.connect("hide",returnDao)


    def on_cancel_commessa_button_clicked(self,button):
        self.commesse_button.set_label("Click me")
        self.daoDict["id_testata_commessa"] = None



    def clear(self):
        """ Funzione di reset o pulizia della UI """
        return

    def saveDao(self, tipo=None):
        """ Si effettuano controlli di coerenza, eventuale presenza
        di campi obbligatori ei provvedere a salvare il record dopo
        aver assegnato i valori necessari
        """
        print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", self.daoDict
        #provv_valore = self.valore_provv_entry.get_value()
        #if self.tipo_provv_euro_radiobutton.get_active():
            #tippo = "€"
        #else:
            #tippo = "%"
        #provv_tipo = tippo
        #self.__dao_provv.valore_provv = provv_valore
        #self.__dao_provv.tipo_provv = provv_tipo
        #self.__dao_provv.persist()
        #self.clear()
