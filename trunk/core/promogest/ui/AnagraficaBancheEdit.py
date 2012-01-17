# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from promogest.dao.Banca import Banca
from promogest.ui.GladeWidget import GladeWidget
from promogest.ui.utils import obligatoryField, messageWarning,\
    messageError, messageInfo
from promogest.lib.iban import check_iban, IBANError


class AnagraficaBancheEdit(GladeWidget):
    """ Dettaglio dell'anagrafica delle banche """

    def __init__(self, anagrafica, dao=None, codice=None):
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
        self._refresh()
        return self.dao

    def updateDao(self):
        self.dao = Banca().getRecord(id=self.dao.id)

    def _refresh(self):
        if self.dao and self.dao.denominazione:
            self.denominazione_banca_entry.set_text(str(self.dao.denominazione))
            self.agenzia_entry.set_text(str(self.dao.agenzia or ''))
            self.iban_entry.set_text(str(self.dao.iban or ''))
            self.abi_entry.set_text(str(self.dao.abi or ''))
            self.cab_entry.set_text(str(self.dao.cab or ''))
            self.bic_swift_entry.set_text(str(self.dao.bic_swift or ''))

    def on_calcola_da_iban_button_clicked(self, button):
        iban = self.iban_entry.get_text() or ''
        if iban:
            try:
                cc, cs, cin, abi, cab, conto = check_iban(iban.upper())
            except IBANError as e:
                messageWarning(msg="Il codice IBAN inserito non è corretto.",
                               transient=self.getTopLevel())
            else:
                messageInfo(msg="Il codice IBAN è formalmente corretto.",
                            transient=self.getTopLevel())


    def saveDao(self, tipo=None):
        denominazione = self.denominazione_banca_entry.get_text()
        if not denominazione:
            obligatoryField(self.anagrafica.getTopLevel(), self.denominazione_banca_entry)
            return
        self.dao.denominazione = denominazione
        self.dao.agenzia = self.agenzia_entry.get_text()
        self.dao.bic_swift = self.bic_swift_entry.get_text()
        self.dao.abi = self.abi_entry.get_text()
        self.dao.cab = self.cab_entry.get_text()
        
        iban = self.iban_entry.get_text() or ''
        if iban:
            iban = iban.upper()
            try:
                cc, cs, cin, abi, cab, conto = check_iban(iban)
            except IBANError:
                messageError(msg="Il codice IBAN inserito non è corretto.",
                                   transient=self.getTopLevel())
                return
            else:
                self.dao.abi = abi
                self.dao.cab = cab
                self.dao.iban = iban
        else:
            self.dao.iban = ''

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
