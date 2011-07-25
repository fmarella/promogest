# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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
from promogest.dao.Banca import Banca
#from promogest.lib.ControlloIBAN import *
from promogest.lib.iban import country_data, check_iban, IBANError
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaBancheEdit(GladeWidget):
    """ Dettaglio dell'anagrafica delle banche """

    def __init__(self, anagrafica,dao=None, codice=None):
        GladeWidget.__init__(self,
                              'banca_edit_window',
                             fileName='_anagrafica_banche_edit.glade')
        self.codice = codice
        self.setDao(dao)
        self.anagrafica = anagrafica
        self._refresh()

    def setDao(self, dao):
        if dao is None:
            self.dao = Banca()
        else:
            self.dao = dao

    def updateDao(self):
        self.dao = Banca().getRecord(id= self.dao.id)
#        self._refresh()

    def _refresh(self):
        """ qui ci vanno i dati per riempire le entry e la label"""
        if self.dao and self.dao.denominazione:
            self.denominazione_banca_entry.set_text(str(self.dao.denominazione))
            self.agenzia_entry.set_text(str(self.dao.agenzia))
            self.iban_entry.set_text(str(self.dao.iban))
            self.abi_entry.set_text(str(self.dao.abi))
            self.cab_entry.set_text(str(self.dao.cab))
            self.checkIban()

    def on_calcola_da_iban_button_clicked(self, button):
        self.checkIban()

    def checkIban(self):
        iban = self.iban_entry.get_text().upper()
        try:
            code, checksum, bank, account = check_iban(iban)
            nazione = country_data(code) or ""
            cin = bank[:nazione.bank[0][0]] or ""
            abi = bank[nazione.bank[0][0]:(nazione.bank[0][0]+nazione.bank[1][0])] or ""
            cab = bank[(nazione.bank[0][0]+nazione.bank[1][0]):(nazione.bank[0][0]+nazione.bank[1][0]+ nazione.bank[2][0])] or ""
        except IBANError, err:
            self.info_label.set_markup(str(err))
            return False
        else:
            self.info_label.set_markup("""<b>IBAN CORRETTO!</b>

    NAZIONE: <b>%s</b>  CODE: <b>%s</b> CHECKSUM: <b>%s</b>
    DATI BANCA: <b>%s</b>  ( CIN: <b>%s</b>, ABI: <b>%s</b>, CAB : <b>%s</b> )
    N° C/CORRENTE: <b>%s</b>

    Assegna queste coordinate ad un cliente/fornitore
    o altro contatto se necessario e provvedi al salvataggio.

""" % (nazione.__dict__["name"], code, checksum, bank,cin,abi,cab,account))
        return iban

    def saveDao(self, tipo=None):
        denominazione = self.denominazione_banca_entry.get_text()
        agenzia = self.agenzia_entry.get_text()
        iban = self.iban_entry.get_text()
        abi = self.abi_entry.get_text()
        cab = self.cab_entry.get_text()
        if not denominazione :
            obligatoryField(self.anagrafica.getTopLevel(), self.denominazione_banca_entry)
            return
#        elif (iban == ''):
#            obligatoryField(self.anagrafica.getTopLevel(), self.iban_entry)
#            return
        self.dao.denominazione = denominazione
        self.dao.agenzia = agenzia
        self.dao.abi = abi
        self.dao.cab = cab
        ib =  self.checkIban()
        if ib:
            self.dao.iban = ib
            self.dao.persist()
        else:
            msg = """Attenzione! NON e' stato inserito nessun IBAN
Proseguire comunque?
"""
            if YesNoDialog(msg=msg, transient=self.getTopLevel()):
                self.dao.persist()


    def deleteDao(self):
        if self.dao and self.dao.denominazione:
            self.dao.delete()

    def on_elimina_banca_button_clicked(self, button):
        self.deleteDao()
        self.anagrafica.refresh()
#        self.duplica_button.set_sensitive(False)
        self.anagrafica.record_new_button.set_sensitive(True)
        self.anagrafica.record_new_menu.set_sensitive(True)

        self.anagrafica.record_edit_button.set_sensitive(False)
        self.anagrafica.record_edit_menu.set_sensitive(False)

        self.anagrafica.record_save_button.set_sensitive(False)
        self.anagrafica.record_save_menu.set_sensitive(False)

        self.anagrafica.record_cancel_button.set_sensitive(False)
        self.anagrafica.record_cancel_menu.set_sensitive(False)

        self.anagrafica.record_undo_button.set_sensitive(False)
        self.anagrafica.record_undo_menu.set_sensitive(False)

        self.anagrafica.record_delete_button.set_sensitive(False)
        self.anagrafica.record_delete_menu.set_sensitive(False)
        self.getTopLevel().destroy()
#        self.anagrafica.setToolTip(False)
        self.anagrafica.setFocus()



    def on_ok_banche_edit_button_clicked(self, button):
        self.saveDao()
        self.anagrafica.refresh()

        self.anagrafica.record_new_button.set_sensitive(True)
        self.anagrafica.record_new_menu.set_sensitive(True)
#        self.duplica_button.set_sensitive(False)
        self.anagrafica.record_edit_button.set_sensitive(False)
        self.anagrafica.record_edit_menu.set_sensitive(False)

        self.anagrafica.record_save_button.set_sensitive(False)
        self.anagrafica.record_save_menu.set_sensitive(False)

        self.anagrafica.record_cancel_button.set_sensitive(False)
        self.anagrafica.record_cancel_menu.set_sensitive(False)

        self.anagrafica.record_undo_button.set_sensitive(False)
        self.anagrafica.record_undo_menu.set_sensitive(False)

        self.anagrafica.record_delete_button.set_sensitive(False)
        self.anagrafica.record_delete_menu.set_sensitive(False)
        self.getTopLevel().destroy()
#        self.anagrafica.setToolTip(False)
        self.anagrafica.setFocus()


    def on_chiudi_banche_edit_button_clicked(self, button):
#        self.anagrafica.refresh()
#        self.anagrafica.anagrafica_treeview.grab_focus()
        self.anagrafica.filterTopLevel.set_sensitive(True)
#        self.anagrafica.anagrafica_filter_navigation_hbox.set_sensitive(True)
#        self.anagrafica.anagrafica_filter_frame.set_sensitive(True)
#        self.anagrafica.anagrafica_treeview_set_edit(False)
#        self.anagrafica.anagrafica_treeview.set_headers_clickable(True)
#        self.anagrafica.anagrafica_treeview.set_enable_search(True)

        self.anagrafica.refresh()

        self.anagrafica.record_new_button.set_sensitive(True)
        self.anagrafica.record_new_menu.set_sensitive(True)
#        self.duplica_button.set_sensitive(False)
        self.anagrafica.record_edit_button.set_sensitive(False)
        self.anagrafica.record_edit_menu.set_sensitive(False)

        self.anagrafica.record_save_button.set_sensitive(False)
        self.anagrafica.record_save_menu.set_sensitive(False)

        self.anagrafica.record_cancel_button.set_sensitive(False)
        self.anagrafica.record_cancel_menu.set_sensitive(False)

        self.anagrafica.record_undo_button.set_sensitive(False)
        self.anagrafica.record_undo_menu.set_sensitive(False)

        self.anagrafica.record_delete_button.set_sensitive(False)
        self.anagrafica.record_delete_menu.set_sensitive(False)
        self.getTopLevel().destroy()
#        self.anagrafica.setToolTip(False)
        self.anagrafica.setFocus()
