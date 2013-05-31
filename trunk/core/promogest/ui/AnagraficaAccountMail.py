# -*- coding: utf-8 -*-

#    Copyright (C) 2013 Francesco Marella <francesco.marella@anche.no>

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

import time
import smtplib
from promogest import Environment as env
from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.dao.AccountEmail import AccountEmail
from promogest.lib.utils import prepareFilterString, obligatoryField,\
    messageWarning, textview_get_text, textview_set_text

try:
    import keyring
except:
    keyring = None
    msg = """Attenzione: la libreria "keyring" necessaria per salvare la password
in modo sicuro non è installata."""
    messageWarning(msg)


class AnagraficaAccountMail(Anagrafica):
    """ Anagrafica account posta elettronica """

    def __init__(self, idAzienda=None, aziendaStr=None):
        self._aziendaFissata = (idAzienda != None)
        self._idAzienda = idAzienda
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica account di posta elettronica',
                            recordMenuLabel='_Account',
                            filterElement=AnagraficaAccountMailFilter(self),
                            htmlHandler=AnagraficaAccountMailHtml(self),
                            reportHandler=AnagraficaAccountMailReport(self),
                            editElement=AnagraficaAccountMailEdit(self),
                            aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)


class AnagraficaAccountMailFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica delle banche azienda """

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
              anagrafica,
              root='anagrafica_account_mail_filter_table',
              path='_anagrafica_account_mail_elements.glade')
        self._widgetFirstFocus = self.denominazione_filter_entry
        self.orderBy = 'denominazione'

    def draw(self, cplx=False):
        self._treeViewModel = self.filter_listore
        self.refresh()

    def _reOrderBy(self, column):
        if column.get_name() == "denominazione_column":
            return self._changeOrderBy(
                column, (None, AccountEmail.denominazione))

    def clear(self):
        # Annullamento filtro
        self.denominazione_filter_entry.set_text('')
        self.indirizzo_filter_entry.set_text('')
        self.denominazione_filter_entry.grab_focus()

    def refresh(self):
        # Aggiornamento TreeView
        idAzienda = self._anagrafica._idAzienda
        denominazione = prepareFilterString(self.denominazione_filter_entry.get_text())
        indirizzo = prepareFilterString(self.indirizzo_filter_entry.get_text())

        def filterCountClosure():
            return AccountEmail().count(idAzienda=idAzienda,
                                        denominazione=denominazione,
                                        indirizzo=indirizzo)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return AccountEmail().select(orderBy=self.orderBy,
                                          idAzienda=idAzienda,
                                          denominazione=denominazione,
                                          indirizzo=indirizzo,
                                          offset=offset,
                                          batchSize=batchSize)

        self._filterClosure = filterClosure

        daos = self.runFilter()

        self._treeViewModel.clear()

        for dao in daos:
            self._treeViewModel.append((dao,
                                        (dao.denominazione),
                                        (dao.indirizzo or ''),
                                        (dao.preferito or False)))


class AnagraficaAccountMailHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'account_mail',
                                'Dettaglio degli account di posta elettronica')


class AnagraficaAccountMailReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli account di posta elettronica',
                                  defaultFileName='account_mail',
                                  htmlTemplate='account_mail',
                                  sxwTemplate='account_mail')


class AnagraficaAccountMailEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica account di posta elettronica """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
            anagrafica,
            'Dati account di posta elettronica',
            root='anagrafica_account_mail_detail_table',
            path='_anagrafica_account_mail_elements.glade')
        self._widgetFirstFocus = self.denominazione_entry

    def draw(self, cplx=False):
        pass

    def setDao(self, dao):
        self.dao = dao
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = AccountEmail()
        self._refresh()
        return self.dao

    def clear(self):
        self.denominazione_entry.set_text('')
        self.indirizzo_entry.set_text('')
        self.preferito_checkbutton.set_active(False)
        self.server_smtp_entry.set_text('')
        self.porta_smtp_entry.set_text('')
        self.crypto_ssl_checkbutton.set_active(False)
        self.username_entry.set_text('')
        self.password_entry.set_text('')
        self.memo_password_checkbutton.set_active(False)
        self.oggetto_entry.set_text('')
        textview_set_text(self.firma_textview, 'Documento creato e inviato tramite Promogest http://www.promogest.me')
        textview_set_text(self.body_textview, '')
        self.result_test_label.set_text('')

    def _refresh(self):
        self.clear()
        self.denominazione_entry.set_text(self.dao.denominazione or '')
        self.indirizzo_entry.set_text(self.dao.indirizzo or '')
        self.preferito_checkbutton.set_active(self.dao.preferito or False)
        self.server_smtp_entry.set_text(self.dao.server_smtp or '')
        self.porta_smtp_entry.set_text(str(self.dao.porta_smtp or '465'))
        self.crypto_ssl_checkbutton.set_active(self.dao.cripto_SSL or False)
        self.username_entry.set_text(self.dao.username or '')
        self.oggetto_entry.set_text(self.dao.oggetto or '')
        textview_set_text(self.firma_textview, self.dao.firma or 'Documento creato e inviato tramite Promogest http://www.promogest.me')
        textview_set_text(self.body_textview, self.dao.body or '')
        password = ''
        try:
            password = keyring.get_password('promogest2',
                                            self.dao.username)
        except:
            pass
        self.password_entry.set_text(password or '')
        del password
        #self.memo_password_checkbutton.set_active(False)

    def saveDao(self, tipo=None):
        denominazione = self.denominazione_entry.get_text()
        if denominazione == '':
            obligatoryField(self.dialogTopLevel, self.denominazione_entry)
        self.dao.denominazione = denominazione
        self.dao.id_azienda = env.azienda
        self.dao.indirizzo = self.indirizzo_entry.get_text()
        self.dao.preferito = self.preferito_checkbutton.get_active()
        self.dao.server_smtp = self.server_smtp_entry.get_text()
        self.dao.porta_smtp = int(self.porta_smtp_entry.get_text())
        self.dao.cripto_SSL = self.crypto_ssl_checkbutton.get_active()
        self.dao.username = self.username_entry.get_text()
        self.dao.oggetto = self.oggetto_entry.get_text()
        self.dao.firma = textview_get_text(self.firma_textview)
        self.dao.body = textview_get_text(self.body_textview)
        #self.dao.memo_password = self.memo_password_checkbutton.get_active()
        self.dao.persist()

        if keyring:
            password = self.password_entry.get_text()
            try:
                keyring.set_password('promogest2', self.dao.username, password)
            except Exception as ex:
                messageWarning('Impossibile salvare la password nel portachiavi di sistema:\n\n%s.' % str(ex))

    def on_test_conn_button_clicked(self, widget):
        s = None
        self.result_test_label.set_text('Connessione in corso...')

        if self.crypto_ssl_checkbutton.get_active():
            try:
                s = smtplib.SMTP_SSL(self.server_smtp_entry.get_text(),
                                    port=self.porta_smtp_entry.get_text())
            except:
                self.result_test_label.set_text('Connessione al server non riuscita.')
                return
        else:
            try:
                s = smtplib.SMTP(self.server_smtp_entry.get_text(),
                                 port=self.porta_smtp_entry.get_text())
                time.sleep(1)
                s.ehlo()
                time.sleep(1)
                s.starttls()
            except:
                self.result_test_label.set_text('Connessione al server non riuscita.')
                return
        try:
            s.login(self.username_entry.get_text(),
                    self.password_entry.get_text())
        except:
            self.result_test_label.set_text('Nome utente o password non validi.')
            return
        if s:
            s.quit()
        self.result_test_label.set_text('Connessione riuscita con successo.')

