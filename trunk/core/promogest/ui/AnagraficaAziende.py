# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/
#    Copyright (C) 2013 Francesco Marella <francesco.marella@anche.no>

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from promogest.ui.GladeWidget import GladeWidget
from PIL import Image
import os
try:
    import keyring
except:
    keyring = None
from promogest import Environment
from promogest.Environment import session, azienda
from promogest.dao.Azienda import Azienda
from promogest.dao.AccountEmail import AccountEmail
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *


class AnagraficaAziende(GladeWidget):
    """ Anagrafica aziende """
    filename = None
    account_model = None

    def __init__(self, mainWindow):
        self._mainWindow = mainWindow
        self.dao = Azienda()
        GladeWidget.__init__(self,
            root='anagrafica_azienda',
            path='anagrafica_azienda.glade')
        self.getTopLevel()
        self.placeWindow(self.getTopLevel())
        self.getTopLevel().set_modal(modal=True)

        self.draw()

    def draw(self):
        # Popolamento campi in maschera dal dao
        self.setDao()
        self.__load_account_email()
        self.denominazione_entry.grab_focus()
        if session.query(AccountEmail).count() == 0:
            self.on_new_account_button_clicked(None)

    def show_all(self):
        """ Visualizza/aggiorna tutta la struttura dell'anagrafica """
        self.show()

    def setDao(self):
        # Creazione dao azienda corrente
        self.dao = Azienda().getRecord(id=Environment.params["schema"])
        if not self.dao:
            self.dao = Azienda().getRecord(id=Environment.azienda)
        self._refresh()

    def _refresh(self):
        self.denominazione_entry.set_text(
            self.dao.denominazione or '')
        self.ragione_sociale_entry.set_text(
            self.dao.ragione_sociale or '')
        self.localita_sede_operativa_entry.set_text(
            self.dao.sede_operativa_localita or '')
        self.indirizzo_sede_operativa_entry.set_text(
            self.dao.sede_operativa_indirizzo or '')
        self.numero_sede_operativa_entry.set_text(
            self.dao.sede_operativa_numero or '')
        self.cap_sede_operativa_entry.set_text(
            self.dao.sede_operativa_cap or '')
        self.provincia_sede_operativa_entry.set_text(
            self.dao.sede_operativa_provincia or '')
        self.localita_sede_legale_entry.set_text(
            self.dao.sede_legale_localita or '')
        self.indirizzo_sede_legale_entry.set_text(
            self.dao.sede_legale_indirizzo or '')
        self.numero_sede_legale_entry.set_text(
            self.dao.sede_legale_numero or '')
        self.cap_sede_legale_entry.set_text(
            self.dao.sede_legale_cap or '')
        self.provincia_sede_legale_entry.set_text(
            self.dao.sede_legale_provincia or '')
        self.codice_fiscale_entry.set_text(
            self.dao.codice_fiscale or '')
        self.partita_iva_entry.set_text(
            self.dao.partita_iva or '')
        self.data_iscrizione_cciaa_entry.set_text(
            dateToString(self.dao.iscrizione_cciaa_data or ''))
        self.numero_iscrizione_cciaa_entry.set_text(
            self.dao.iscrizione_cciaa_numero or '')
        self.data_iscrizione_tribunale_entry.set_text(
            dateToString(self.dao.iscrizione_tribunale_data or ''))
        self.numero_iscrizione_tribunale_entry.set_text(
            self.dao.iscrizione_tribunale_numero or '')
        self.codice_rea_entry.set_text(
            self.dao.codice_rea or '')
        self.matricola_inps_entry.set_text(
            self.dao.matricola_inps or '')
        #self.path_label.set_text(self.dao.percorso_immagine or '')
        self.logo_azienda.set_from_file(
            self.dao.percorso_immagine or "")

        #self.percorso_immagine_entry.set_text(self.dao.percorso_immagine or '')

    def saveDao(self):
        self.dao.denominazione = self.denominazione_entry.get_text()
        self.dao.ragione_sociale = self.ragione_sociale_entry.get_text()
        self.dao.sede_operativa_localita = \
                                self.localita_sede_operativa_entry.get_text()
        self.dao.sede_operativa_indirizzo = \
                                self.indirizzo_sede_operativa_entry.get_text()
        self.dao.sede_operativa_numero = \
                                self.numero_sede_operativa_entry.get_text()
        self.dao.sede_operativa_cap = self.cap_sede_operativa_entry.get_text()
        self.dao.sede_operativa_provincia = \
                                self.provincia_sede_operativa_entry.get_text()
        self.dao.sede_legale_localita =\
                                 self.localita_sede_legale_entry.get_text()
        self.dao.sede_legale_indirizzo = \
                                self.indirizzo_sede_legale_entry.get_text()
        self.dao.sede_legale_numero = self.numero_sede_legale_entry.get_text()
        self.dao.sede_legale_cap = self.cap_sede_legale_entry.get_text()
        self.dao.sede_legale_provincia = \
                                self.provincia_sede_legale_entry.get_text()
        self.dao.codice_fiscale = self.codice_fiscale_entry.get_text()
        self.dao.partita_iva = self.partita_iva_entry.get_text()
        self.dao.iscrizione_cciaa_data = \
                    stringToDate(self.data_iscrizione_cciaa_entry.get_text())
        self.dao.iscrizione_cciaa_numero = \
                    self.numero_iscrizione_cciaa_entry.get_text()
        self.dao.iscrizione_tribunale_data = \
                stringToDate(self.data_iscrizione_tribunale_entry.get_text())
        self.dao.iscrizione_tribunale_numero = \
                            self.numero_iscrizione_tribunale_entry.get_text()
        self.dao.codice_rea = self.codice_rea_entry.get_text()
        self.dao.matricola_inps = self.matricola_inps_entry.get_text()

        self.dao.percorso_immagine = self.filename or ''
        #self.path_label.get_text() #+"/"+self.filena
        if self.dao.codice_fiscale != '':
            codfis = checkCodFisc(self.dao.codice_fiscale)
            if not codfis:
                return False
        if self.dao.partita_iva != '':
            partiva = checkPartIva(self.dao.partita_iva)
            if not partiva:
                return False
        return True

    def on_seleziona_logo_button_clicked(self, widget):
        self.logo_filechooserdialog.run()
        if self.dao.percorso_immagine:
            self.logo_filechooserdialog.set_filename(self.dao.percorso_immagine)

#    def on_logo_filechooserdialog_file_activated(self, widget):
#        filename = self.logo_filechooserdialog.get_filename()
#        self.path_label.set_text(filename)
#        f = self.resizeImgThumbnailGeneric(filename = filename)
##        self.logo_azienda.set_from_file(f)
#        self.logo_image2.set_from_file(f)

    def on_chiudi_button_clicked(self, button):
        self.logo_filechooserdialog.hide()

    def on_apri_button_clicked(self, button):
        self.filename = self.logo_filechooserdialog.get_filename()
        #self.path_label.set_text(filename)
#        f = self.resizeImgThumbnailGeneric(filename = filename)
        self.logo_azienda.set_from_file(self.filename)
        self.logo_filechooserdialog.hide()

    def on_rimuovi_logo_clicked(self, button):
        self.logo_azienda.set_from_file(None)
        #self.path_label.set_text("")

    def resizeImgThumbnailGeneric(self, req=None, filename=None):
        """
        funzione di ridimensionamento immagine per la lista, di fatto
        crea un thumnail dell'immagine stessa
        """
        if filename:
            try:
                self.filena = filename.split("/")[-1]
                im1 = Image.open(filename)
                width = int(setconf("Documenti", "larghezza_logo"))
                height = int(setconf("Documenti", "altezza_logo"))
                im5 = im1.resize((width, height), Image.ANTIALIAS)
                newname = 'resize_' + self.filena
                p = os.path.dirname(filename)
                im5.save(p + "/" + newname)
                return p + "/" + newname
            except:
                print "ERRORE NEL LOGO", filename
        return ""

    def on_apply_button_clicked(self, button):
        save = self.saveDao()
        if save:
            self.dao.persist()
            self.getTopLevel().destroy()

    def on_cancel_button_clicked(self, button):
        self.setDao()

    def on_close_button_clicked(self, button):
        self.getTopLevel().destroy()

    def on_contatti_togglebutton_toggled(self, toggleButton):
        if not(toggleButton.get_active()):
            toggleButton.set_active(False)
            return
        if posso("CN"):
            from promogest.ui.Contatti.AnagraficaContatti import\
                                                         AnagraficaContatti
            anag = AnagraficaContatti(self.dao.schemaa, 'azienda')
            anagWindow = anag.getTopLevel()

            showAnagraficaRichiamata(self._mainWindow.getTopLevel(),
                                                    anagWindow, toggleButton)
        else:
            fenceDialog()
            toggleButton.set_active(False)

    def on_banche_azienda_button_clicked(self, button):
        from promogest.ui.AnagraficaBancheAzienda import AnagraficaBancheAzienda
        anag = AnagraficaBancheAzienda(self.dao.schemaa)
        anagWindow = anag.getTopLevel()
        returnWindow = button.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

    # GESTIONE ACCOUNT EMAIL
    def __clear_account_email(self):
        self.nome_entry.set_text('')
        self.indirizzo_entry.set_text('')
        self.preferito_checkbutton.set_active(False)
        self.server_smtp_entry.set_text('')
        self.porta_smtp_entry.set_text('')
        self.crypto_ssl_checkbutton.set_active(False)
        self.username_entry.set_text('')
        self.password_entry.set_text('')
        self.memo_password_checkbutton.set_active(False)
        self.save_button.set_sensitive(False)

    def __load_account_email(self):
        self.accounts_liststore.clear()
        for account in session.query(AccountEmail).all():
            self.accounts_liststore.append([account, account.denominazione])

    def on_accounts_treeview_cursor_changed(self, treeview):
        sel = treeview.get_selection()
        (model, iterator) = sel.get_selected()
        if iterator:
            account = model.get_value(iterator, 0)
            self.nome_entry.set_text(account.denominazione)
            self.indirizzo_entry.set_text(account.indirizzo or '')
            self.preferito_checkbutton.set_active(account.preferito or False)
            self.server_smtp_entry.set_text(account.server_smtp or '')
            self.porta_smtp_entry.set_text(str(account.porta_smtp) or 0)
            self.crypto_ssl_checkbutton.set_active(account.cripto_SSL or False)
            self.username_entry.set_text(account.username or '')
            #self.password_entry.set_text(account.password or '')
            #self.memo_password_checkbutton.set_active(False)
            # keyring.get_password('promogest2', account.username)
            self.account_model = account
            self.save_button.set_sensitive(True)

    def on_new_account_button_clicked(self, button):
        self.__clear_account_email()
        self.save_button.set_sensitive(True)
        self.account_model = AccountEmail()
        self.nome_entry.grab_focus()

    def on_remove_account_button_clicked(self, button):
        self.__clear_account_email()
        self.account_model.delete()
        self.__load_account_email()

    def on_save_button_clicked(self, button):
        self.account_model.id_azienda = azienda
        self.account_model.denominazione = self.nome_entry.get_text()
        self.account_model.indirizzo = self.indirizzo_entry.get_text()
        self.account_model.preferito = self.preferito_checkbutton.get_active()
        self.account_model.server_smtp = self.server_smtp_entry.get_text()
        self.account_model.porta_smtp = int(self.porta_smtp_entry.get_text() or 0)
        self.account_model.cripto_SSL = self.crypto_ssl_checkbutton.get_active()
        self.account_model.username = self.username_entry.get_text()
        #self.account_model.memo_password = self.memo_password_checkbutton.get_active()
        self.account_model.persist()
        if keyring:
            password = self.password_entry.get_text()
            try:
                keyring.set_password('promogest2', self.account_model.username, password)
            except Exception as ex:
                messageWarning('Impossibile salvare la password nel portachiavi di sistema:\n\n%s.' % str(ex))
        self.__clear_account_email()
        self.__load_account_email()
    # FINE GESTIONE ACCOUNT EMAIL
