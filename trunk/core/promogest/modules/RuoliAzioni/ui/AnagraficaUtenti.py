# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

import hashlib
import datetime
import base64
from base64 import b64decode
import Image

from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaEdit import AnagraficaEdit
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter

from promogest import Environment
from promogest.dao.User import User
from promogest.dao.Azienda import Azienda
from promogest.dao.UtenteImmagine import UtenteImmagine
from promogest.modules.GestioneFile.dao.Immagine import ImageFile
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
from promogest.ui.gtk_compat import *

class AnagraficaUtenti(Anagrafica):
    """ Anagrafica utenti """

    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
            windowTitle='Promogest - Anagrafica utenti',
            recordMenuLabel='_Utenti',
            filterElement=AnagraficaUtentiFilter(self),
            htmlHandler=AnagraficaUtentiHtml(self),
            reportHandler=AnagraficaUtentiReport(self),
            editElement=AnagraficaUtentiEdit(self),
            aziendaStr=aziendaStr)


class AnagraficaUtentiFilter(AnagraficaFilter):
    """ Filtro per la ricerca nell'anagrafica degli utenti"""

    def __init__(self, anagrafica):
        AnagraficaFilter.__init__(self,
            anagrafica,
            'anagrafica_utenti_filter_table',
            gladeFile='RuoliAzioni/gui/_anagrafica_utenti_elements.glade',
            module=True)
        self._widgetFirstFocus = self.username_filter_entry


    def draw(self, cplx=False):
        # Colonne della Treeview per il filtro
        treeview = self._anagrafica.anagrafica_filter_treeview
        renderer = gtk.CellRendererText()

        column = gtk.TreeViewColumn('Username', renderer, text=1)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'username'))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('E-mail', renderer,text=2)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None,'email'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ruolo', renderer,text=3)
        column.set_sizing(GTK_COLUMN_GROWN_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, 'ruolo')
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        treeview.set_search_column(1)

        self._treeViewModel = gtk.ListStore(object, str, str, str)
        self._anagrafica.anagrafica_filter_treeview.set_model(self._treeViewModel)

        self.clear()
        #self.refresh()


    def clear(self):
        # Annullamento filtro
        self.username_filter_entry.set_text('')
        self.email_filter_entry.set_text('')
        fillComboboxRole(self.id_role_filter_combobox, True)
        self.active_filter_checkbutton.set_active(True)
        self.refresh()


    def refresh(self):
        # Aggiornamento TreeView
        username = prepareFilterString(self.username_filter_entry.get_text())
        email = prepareFilterString(self.email_filter_entry.get_text())
        idRole = findIdFromCombobox(self.id_role_filter_combobox)
        active = self.active_filter_checkbutton.get_active()

        def filterCountClosure():
            return User().count(usern=username,
                                email=email,
                                role=idRole,
                                active=active)

        self._filterCountClosure = filterCountClosure

        self.numRecords = self.countFilterResults()

        self._refreshPageCount()

        # Let's save the current search as a closure
        def filterClosure(offset, batchSize):
            return User().select(usern=username,
                                email=email,
                                role=idRole,
                                #active=active,
                                orderBy=self.orderBy,
                                offset=offset,
                                batchSize=batchSize)

        self._filterClosure = filterClosure

        utenti = self.runFilter()

        self._treeViewModel.clear()

        for i in utenti:
            self._treeViewModel.append((i,
                                        (i.username or ''),
                                        (i.email or ''),
                                        (i.ruolo or '')))



class AnagraficaUtentiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'utente',
                                'Dettaglio utenti')



class AnagraficaUtentiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli utenti',
                                  defaultFileName='utenti',
                                  htmlTemplate='utenti',
                                  sxwTemplate='utenti')


class AnagraficaUtentiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica degli utenti  """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
            anagrafica,
            'anagrafica_utenti_detail_table',
            'Dati Utente',
            gladeFile='RuoliAzioni/gui/_anagrafica_utenti_elements.glade',
            module=True)
        self.imgblob = None
        self._widgetFirstFocus = self.username_entry

    def draw(self, cplx=False):
        #Popola combobox tipi utenti
        fillComboboxRole(self.id_role_combobox)
        fillComboboxLang(self.id_language_combobox)
        azs = Azienda().select(batchSize = None, orderBy=Azienda.schemaa)
        for a in azs:
            self.azienda_listore.append((a.schemaa,))
        self.azienda_combobox.set_model(self.azienda_listore)

    def setDao(self, dao, from_other_dao=None):
        self.from_other_dao = from_other_dao
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = User()
            self.aggiornamento=False
        else:
            self.dao = User().getRecord(id=dao.id)
            self.aggiornamento=True
        self._refresh()


    def _refresh(self):
        self.username_entry.set_text(self.dao.username or '')
#        if self.aggiornamento:
#            self.username_entry.set_sensitive(False)
        if self.dao.tipo_user =="PLAIN":
            self.password_entry.set_text(self.dao.password)
            self.confirm_password_entry.set_text(self.dao.password)
            self.password_entry.set_visibility(True)
            self.confirm_password_entry.set_visibility(True)
        else:
            self.password_entry.set_text('')
            self.confirm_password_entry.set_text('')
        self.email_entry.set_text(self.dao.email or '')
        self.url_entry.set_text(self.dao.photo_src or '')
        act = 0
        if self.dao.active:
            act = 1
        self.active_user_checkbutton.set_active(act)
        findComboboxRowFromId(self.id_role_combobox, self.dao.id_role)
        findComboboxRowFromStr(self.azienda_combobox, self.dao.schemaa_azienda,0)
        self.data_registrazione_label.set_text(dateToString(self.dao.registration_date))
        self.ultima_modifica_label.set_text(dateToString(self.dao.last_modified))
        if self.dao.id:
            imgBlobb = UtenteImmagine().select(idUtente = self.dao.id)
            if imgBlobb:
                try:
                    img = ImageFile().getRecord(id=imgBlobb[0].id_immagine)
                    fingerprint =Environment.CACHE+"/"+img.fingerprint
                    f = open(fingerprint, "w")
                    f.write(b64decode(img.data))
                    f.close()
                    self.userlogo_image.set_from_file(fingerprint)
                except:
                    self.userlogo_image.set_from_file("")

# ----- Per il momento non è utilizzato ma andrà ripristinato
# ---- il prima possibile
#        findComboboxRowFromId(self.id_language_combobox, self.dao.id_language)

    def saveDao(self, tipo=None):
        if (self.username_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.username_entry)

        if (self.email_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.email_entry)

        if (self.password_entry.get_text() == '') and not self.aggiornamento:
            obligatoryField(self.dialogTopLevel, self.password_entry)

        if (findIdFromCombobox(self.id_role_combobox) is None):
            obligatoryField(self.dialogTopLevel, self.id_role_combobox)

        username = self.username_entry.get_text()
        password = self.password_entry.get_text()
        confirm_passowrd = self.confirm_password_entry.get_text()
        if password != confirm_passowrd:
            messageInfo(msg='Le due Password non corrispondono !!!')
            return
        passwordmd5 = hashlib.md5(username + str(password)).hexdigest()

        self.dao.username = username
        if (self.password_entry.get_text() != '') or (self.password_entry.get_text() != '' and self.aggiornamento):
            if self.dao.tipo_user =="PLAIN":
                self.dao.password = self.password_entry.get_text()
            else:
                self.dao.password = passwordmd5
        self.dao.email = self.email_entry.get_text()
        self.dao.photo_src = self.url_entry.get_text()
        self.dao.id_role = findIdFromCombobox(self.id_role_combobox)
        self.dao.schemaa_azienda = findStrFromCombobox(self.azienda_combobox,0)
        self.dao.last_modified = datetime.datetime.now()
#        self.dao.id_language = findIdFromCombobox(self.id_language_combobox)
        self.dao.active = self.active_user_checkbutton.get_active()
        if not self.aggiornamento:
            self.dao.registration_date = datetime.datetime.now()
        self.dao.persist()

        if self.from_other_dao:
            self.from_other_dao.id_user = self.dao.id
            #self.from_other_dao.id_user.persist()
        if self.imgblob:
            idutente = self.dao.id
            a = UtenteImmagine().select(idUtente=self.dao.id)
            if a:
                a=a[0]
                img = ImageFile().getRecord(id=a.id_immagine)
            else:
                a= UtenteImmagine()
                img = ImageFile()
            img.denominazione = "nessuno"
            #img.altezza
            img.larghezza = 200
            img.fingerprint = hashlib.md5(self.imgblob).hexdigest()
            img.data = self.imgblob
            img.persist()
            a.id_utente = self.dao.id
            a.id_immagine = img.id
            a.persist()

    def on_rimuovi_foto_button_clicked(self, button):
        self.imgblob = "RIMUOVO"
        self.userlogo_image.set_from_file("")

    def on_filechooserbutton1_file_set(self, filechooser):
        #import StringIO
        #output = StringIO.StringIO()
        #image.save(output)
        #contents = output.getvalue()
        #output.close()

        print "LA FOTO SELEZIONATA",  filechooser.get_file().get_path(), filechooser.get_file()
        size = 200, 200
        self.photo_src= filechooser.get_filename()
        self.userlogo_image.set_from_file(self.photo_src)
        #im1 = Image.fromstring(self.photo_src)
        f = open(self.photo_src, "r")
        g = f.read()
        #im = Image.open(g)
        #im.thumbnail(size, Image.ANTIALIAS)
        #im.tostring(self.photo_src + ".thumbnail)
        self.imgblob = base64.b64encode(str(g))
        f.close()
