# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>
# License: GNU GPLv2

import gtk
import gobject

from promogest import Environment
from promogest.dao.Banca import Banca
#from promogest.lib.ControlloIBAN import *
from promogest.lib.iban import country_data, check_iban, IBANError
from GladeWidget import GladeWidget
from utils import *
from utilsCombobox import *


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
            if Environment.engine.name =="sqlite" and Banca().count() >= 1:
                fenceDialog()
                return
            else:
                self.dao = Banca()
        else:
            self.dao = dao

    def updateDao(self):
        self.dao = Banca().getRecord(id= self.dao.id)
#        self._refresh()

    def _refresh(self):
        """ qui ci vanno i dati per riempire le entry e la label"""
#        print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", self.dao
        if self.dao and self.dao.denominazione:
            self.denominazione_banca_entry.set_text(str(self.dao.denominazione))
            self.agenzia_entry.set_text(str(self.dao.agenzia))
            self.iban_entry.set_text(str(self.dao.iban))
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
            self.info_label.set_markup("""
    <b>IBAN CORRETTO!</b>

    NAZIONE: <b>%s</b>  CODE: <b>%s</b> CHECKSUM: <b>%s</b>
    DATI BANCA: <b>%s</b>  ( CIN: <b>%s</b>, ABI: <b>%s</b>, CAB : <b>%s</b> )
    N° C/CORRENTE: <b>%s</b>

    Assegna queste coordinate ad un cliente/fornitore
    o altro contatto se necessario e provvedi al salvataggio.

""" % (nazione.__dict__["name"], code, checksum, bank,cin,abi,cab,account))
        return iban

    def saveDao(self):
        denominazione = self.denominazione_banca_entry.get_text()
        agenzia = self.agenzia_entry.get_text()
        iban = self.iban_entry.get_text()
        if not denominazione :
            obligatoryField(self._anagrafica.getTopLevel(), self.denominazione_banca_entry)
            return
        elif (iban == ''):
            obligatoryField(self._anagrafica.getTopLevel(), self.iban_entry)
            return
        self.dao.denominazione = denominazione
        self.dao.agenzia = agenzia
        ib =  self.checkIban()
        if ib:
            self.dao.iban = ib
            self.dao.persist()
        else:
            print "ERRORE NEL SALVATAGGIO"

    def deleteDao(self):
        if self.dao and self.dao.denominazione:
            self.dao.delete()

    def on_elimina_banca_button_clicked(self, button):
        self.deleteDao()
        self.anagrafica.refresh()

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
