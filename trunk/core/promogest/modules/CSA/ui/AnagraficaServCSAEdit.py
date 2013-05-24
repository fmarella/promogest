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
        self._clear()
        findComboboxRowFromId(self.luogo_installazione_combobox.combobox, self.dao.id_luogo_installazione)
        self.numero_seriale_entry.set_text(self.dao.numero_serie or "")
        self.combustibile_entry.set_text(self.dao.combustibile or "")
        self.id_cliente_customcombobox.setId(self.dao.id_cliente)
        self.id_persona_giuridica_customcombobox.setId(self.dao.id_persona_giuridica)
        self.id_articolo_customcombobox.setId(self.dao.id_articolo)
        findComboboxRowFromStr(self.manutenzione_combobox, self.dao.manutenzione,0)
        self.data_avviamento_datewidget.set_text(dateToString(self.dao.data_avviamento))
        self.libretto_checkbutton.set_active(bool(self.dao.tenuta_libretto))
        #self.id_commessa_customcombobox.setId(self.dao.id_testata_commessa)

    def setMonth(self):
        mesi = self.dao.cadenza.split() or []
        if "01" in mesi: self.checkbutton_01.set_active(True)
        else: self.checkbutton_01.set_active(False)
        if "02" in mesi: self.checkbutton_02.set_active(True)
        else: self.checkbutton_02.set_active(False)
        if "03" in mesi: self.checkbutton_03.set_active(True)
        else: self.checkbutton_03.set_active(False)
        if "04" in mesi: self.checkbutton_04.set_active(True)
        else: self.checkbutton_04.set_active(False)
        if "05" in mesi: self.checkbutton_05.set_active(True)
        else: self.checkbutton_05.set_active(False)
        if "06" in mesi: self.checkbutton_06.set_active(True)
        else: self.checkbutton_06.set_active(False)
        if "07" in mesi: self.checkbutton_07.set_active(True)
        else: self.checkbutton_07.set_active(False)
        if "08" in mesi: self.checkbutton_08.set_active(True)
        else: self.checkbutton_08.set_active(False)
        if "09" in mesi: self.checkbutton_09.set_active(True)
        else: self.checkbutton_09.set_active(False)
        if "10" in mesi: self.checkbutton_10.set_active(True)
        else: self.checkbutton_10.set_active(False)
        if "11" in mesi: self.checkbutton_11.set_active(True)
        else: self.checkbutton_11.set_active(False)
        if "12" in mesi: self.checkbutton_12.set_active(True)
        else: self.checkbutton_12.set_active(False)

    def getMonth(self):
        mesi = []
        if self.checkbutton_01.get_active() and "01" not in mesi:
            mesi.append("01")
        if self.checkbutton_02.get_active() and "02" not in mesi:
            mesi.append("02")
        if self.checkbutton_03.get_active() and "03" not in mesi:
            mesi.append("03")
        if self.checkbutton_04.get_active() and "04" not in mesi:
            mesi.append("04")
        if self.checkbutton_05.get_active() and "05" not in mesi:
            mesi.append("05")
        if self.checkbutton_06.get_active() and "06" not in mesi:
            mesi.append("06")
        if self.checkbutton_07.get_active() and "07" not in mesi:
            mesi.append("07")
        if self.checkbutton_08.get_active() and "08" not in mesi:
            mesi.append("08")
        if self.checkbutton_09.get_active() and "09" not in mesi:
            mesi.append("09")
        if self.checkbutton_10.get_active() and "10" not in mesi:
            mesi.append("10")
        if self.checkbutton_11.get_active() and "11" not in mesi:
            mesi.append("11")
        if self.checkbutton_12.get_active() and "12" not in mesi:
            mesi.append("12")
        return mesi

    def _clear(self):
        """ Funzione di reset o pulizia della UI """
        self.data_avviamento_datewidget.insert_today()
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
        self.dao.numero_serie = self.numero_seriale_entry.get_text()
        self.dao.manutenzione = findStrFromCombobox(self.manutenzione_combobox,0)
        self.dao.tenuta_libretto = bool(self.libretto_checkbutton.get_active())
        self.dao.data_avviamento = stringToDate(self.data_avviamento_datewidget.get_text())
        self.dao.id_luogo_installazione = findIdFromCombobox(self.luogo_installazione_combobox.combobox)
        self.dao.cadenza = self.getMonth()
        self.dao.persist()
