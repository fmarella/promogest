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
from promogest.dao.DaoUtils import get_columns
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
        self._widgetFirstFocus = self.id_articolo_customcombobox
        self.anagrafica = anagrafica

        self.daoFrom = daoFrom
        self.tipo = tipo

    def draw(self, cplx=False):
        """ Funzione che "disegna l'interfaccia, devi annullare alcune combo
        a seconda di cosa richiama la finestra...iniziamo dal caso cliente
        """
        self.id_commessa_customcombobox.setHandler("commessa")

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
        return self.dao

    def _refresh(self):
        """Funzione che rinfresca la UI all'apertura e dopo alcune operazioni
        di modifica
        """
        findComboboxRowFromId(self.luogo_installazione_combobox.combobox, self.dao.id_luogo_installazione)
        self.numero_seriale_entry.set_text(self.dao.numero_serie or "")
        self.combustibile_entry.set_text(self.dao.combustibile or "")
        self.id_cliente_customcombobox.setId(self.dao.id_cliente)
        self.id_persona_giuridica_customcombobox.setId(self.dao.id_persona_giuridica)
        self.id_articolo_customcombobox.setId(self.dao.id_articolo)
        #self.id_commessa_customcombobox.setId(self.dao.id_testata_commessa)

    def clear(self):
        """ Funzione di reset o pulizia della UI """
        return

    def saveDao(self, tipo=None):
        #if findIdFromCombobox(
                        #self.id_magazzino_customcombobox.combobox) is None:
            #obligatoryField(self.dialogTopLevel,
                    #self.id_magazzino_customcombobox.combobox)
        #idMagazzino = findIdFromCombobox(
                    #self.id_magazzino_customcombobox.combobox)
        #idArticolo = self.id_articolo_customcombobox.getId()

        self.dao.id_cliente = self.id_cliente_customcombobox.getId()
        self.dao.id_articolo = self.id_articolo_customcombobox.getId()
        #self.dao.id_commessa = self.id_articolo_customcombobox.getId()
        self.dao.combustibile = self.combustibile_entry.get_text()
        self.dao.tenuta_libretto = bool(self.libretto_checkbutton.get_active())
        self.dao.persist()
