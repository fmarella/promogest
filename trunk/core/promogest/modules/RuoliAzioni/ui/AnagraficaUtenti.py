# -*- coding: utf-8 -*-

# Promogest2
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

import gtk
import hashlib
from promogest.ui.AnagraficaComplessa import Anagrafica, AnagraficaFilter, AnagraficaHtml, AnagraficaReport, AnagraficaEdit

from promogest import Environment
from promogest.dao.User import User

from promogest.ui.utils import *
from promogest.ui.utilsCombobox import *

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
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect("clicked", self._changeOrderBy, (None,'username'))
        column.set_resizable(True)
        column.set_expand(True)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('E-mail', renderer,text=2)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
        column.set_clickable(True)
        column.connect('clicked', self._changeOrderBy, (None,'email'))
        column.set_resizable(True)
        column.set_expand(False)
        column.set_min_width(100)
        treeview.append_column(column)

        column = gtk.TreeViewColumn('Ruolo', renderer,text=3)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
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
                                  description='Elenco delle aliquote I.V.A.',
                                  defaultFileName='aliquote_iva',
                                  htmlTemplate='aliquote_iva',
                                  sxwTemplate='aliquote_iva')



class AnagraficaUtentiEdit(AnagraficaEdit):
    """ Modifica un record dell'anagrafica degli utenti  """

    def __init__(self, anagrafica):
        AnagraficaEdit.__init__(self,
                                anagrafica,
                                'anagrafica_utenti_detail_table',
                                'Dati Utente',
                                gladeFile='RuoliAzioni/gui/_anagrafica_utenti_elements.glade',
                                module=True)
        self._widgetFirstFocus = self.username_entry


    def draw(self, cplx=False):
        #Popola combobox tipi utenti
        fillComboboxRole(self.id_role_combobox)
        fillComboboxLang(self.id_language_combobox)


    def setDao(self, dao):
        if dao is None:
            # Crea un nuovo Dao vuoto
            self.dao = User()
            self.aggiornamento = False
        else:
            # Ricrea il Dao con una connessione al DBMS SQL
            self.dao = User().getRecord(id=dao.id)
            self.aggiornamento=True
        self._refresh()


    def _refresh(self):
        self.username_entry.set_text(self.dao.username or '')
        if self.aggiornamento:
            self.username_entry.set_sensitive(False)
        self.password_entry.set_text('')
        self.confirm_password_entry.set_text('')
        self.email_entry.set_text(self.dao.email or '')
        self.url_entry.set_text(self.dao.photo_src or '')
        act = 0
        if self.dao.active:
            act = 1
        self.active_user_checkbutton.set_active(act)
        findComboboxRowFromId(self.id_role_combobox, self.dao.id_role)
        findComboboxRowFromId(self.id_language_combobox, self.dao.id_language)


    def saveDao(self):
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
            msg = 'Le due Password non corrispondono !!!'
            dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
            dialog.run()
            dialog.destroy()
            return
        passwordmd5 = hashlib.md5(username + str(password)).hexdigest()

        self.dao.username = username
        if (self.password_entry.get_text() != '') or (self.password_entry.get_text() != '' and self.aggiornamento):
            self.dao.password = passwordmd5
        self.dao.email = self.email_entry.get_text()
        self.dao.photo_src = self.url_entry.get_text()
        self.dao.id_role = findIdFromCombobox(self.id_role_combobox)
        self.dao.id_language = findIdFromCombobox(self.id_language_combobox)
        self.dao.active = self.active_user_checkbutton.get_active()
        self.dao.persist()
