# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

import hashlib
import os
import sys
from promogest import Environment
from promogest.ui.gtk_compat import *
import datetime
import random
import threading
import webbrowser
from promogest.ui.GladeApp import GladeApp
from promogest.dao.User import User
from promogest.dao.Azienda import Azienda
from GtkExceptionHandler import GtkExceptionHandler
from promogest.ui.SendEmail import SendEmail
from promogest.ui.UpdateDialog import UpdateDialog
from promogest.ui.utils import leggiRevisioni, hasAction, checkInstallation, \
    setconf, posso, installId, messageInfo, findStrFromCombobox
from promogest.ui.utilsCombobox import findComboboxRowFromStr

Environment.pg2log.info("GTK+: " + str(GTK_VERSION))

import sqlalchemy
Environment.pg2log.info("SQLALCHEMY:"+str(sqlalchemy.__version__))
if sqlalchemy.__version__ < "0.5.8":
    messageInfo(msg="""ATTENZIONE!! Versione di python-sqlalchemy inferiore a 0.5.8
Alcune parti potrebbero dare errore
Si consiglia di aggiornare alla versione 0.6.3 o superiore
su forum.promotux.it troverete come fare
""")
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.lib import feedparser
from promogest.lib import HtmlHandler
from promogest.ui.StatusBar import Pg2StatusIcon


class Login(GladeApp):

    def __init__(self, debugSQL=None, debugALL=None, shop=False):
        """Inizializza la finestra di login

        :param debugSQL: boolean, non utilizzato
        :param debugALL: boolean, non utilizzato
        :param shop: default False
        """
        self.azienda=None
        self._dbConnString = ''
        self.modules = {}
        self.shop =shop
        a = GladeApp.__init__(self, 'login_window')
        Environment.exceptionHandler = GtkExceptionHandler()
        self.draw()
        self.getTopLevel().show_all()
        #Pg2StatusIcon() # da risolvere in futuro magari con una soluzione all-glade

    def draw(self):
        """Disegna la finestra di login
        """
        azs = Azienda().select(batchSize = None, orderBy=Azienda.schemaa)
        ultima_azienda = None
        if Environment.engine.name == "sqlite" and len(azs)==1 and azs[0].schemaa=="AziendaPromo":
            self.azienda_combobox.destroy()
            self.azienda_label.destroy()
            self.logina_label.set_markup("Dati accesso <b>ONE</b> : Username: <b>admin</b>, password: <b>admin</b>")
        else:
            self.azienda_combobox_listore.clear()

            for a in azs:
                if a.tipo_schemaa == "last":
                    ultima_azienda = a.schemaa
                self.azienda_combobox_listore.append((a.schemaa, (a.denominazione or "")[0:30]))
            self.azienda_combobox.set_model(self.azienda_combobox_listore)
        #if not Environment.pg3: #necessario per windows, non va bene in gtk3
            #self.azienda_combobox.set_text_column(0)
        Environment.windowGroup.append(self.getTopLevel())

        self.splashHandler()
        dateTimeLabel = datetime.datetime.now().strftime('%d/%m/%Y  %H:%M')
        self.date_label.set_text(dateTimeLabel)
        #if Environment.engine.name != "sqlite" or (len(azs)==1 and azs[0].schemaa !="AziendaPromo") :
        if Environment.aziendaforce:
            ultima_azienda = Environment.aziendaforce
        if ultima_azienda:
            for r in self.azienda_combobox_listore:
                if r[0] == ultima_azienda:
                    self.azienda_combobox.set_active_iter(r.iter)
        else:
            self.azienda_combobox.set_active(0)
        #ATTENZIONE METTO COME RUOLO ADMIN PER IL MOMENTO RICONTROLLARE

        #self.username_combobox_listore.clear()
        #for a in usrs:
            #self.username_combobox_listore.append((a.username, a.email))
        #self.username_comboxentry.set_model(self.username_combobox_listore)
        #if not Environment.pg3:  #necessario per windows
            #self.username_comboxentry.set_text_column(0)
        self.username_entry.grab_focus()
        data = datetime.datetime.now()
        self.anno_lavoro_spinbutton.set_value(data.year)
        leggiRevisioni()


    def on_logo_button_clicked(self, button):
        """Apre il sito web del PromoGest

        :param button: il tasto che ha generato l'evento
        """
        webbrowser.open_new_tab(self.urll)


    def splashHandler(self):
        data = datetime.datetime.now()
        if (data > datetime.datetime(data.year,12,15) and data < datetime.datetime(data.year,12,31)) or \
            (data < datetime.datetime(data.year,1,10) and data > datetime.datetime(data.year,1,1)) :
            randomFile = random.sample([1, 2, 3, 4, 5,6], 1)[0]
            fileSplashImage = Environment.conf.guiDir + "natale["+str(randomFile)+"].png"
            if Environment.engine.name == "sqlite":
                self.login_tipo_label.set_markup("<b>PromoGest 'ONE'</b>")
                self.urll = "http://www.promogest.me/promoGest/preventivo_one"
            else:
                self.login_tipo_label.set_markup("<b>PromoGest 'PRO'</b>")
                self.urll = "http://www.promogest.me/promoGest/preventivo_pro"
        else:
            if Environment.engine.name == "sqlite": #forzo lo splash per lite
                randomFile = random.sample([1, 2, 3, 4, 5, 6], 1)[0]
                fileSplashImage = Environment.conf.guiDir + "one["+str(randomFile)+"].png"
                self.login_tipo_label.set_markup("<b>PromoGest 'ONE'</b>")
                self.urll = "http://www.promogest.me/promoGest/preventivo_one"
            else:
                randomFile = random.sample([1, 2, 3, 4, 5, 6], 1)[0]
                fileSplashImage = Environment.conf.guiDir + "pro["+str(randomFile)+"].png"
                self.login_tipo_label.set_markup("<b>PromoGest 'PRO'</b>")
                self.urll = "http://www.promogest.me/promoGest/preventivo_pro"
        self.splash_image.set_from_file(fileSplashImage)


    def feddretreive(self):
        """Carica il feed RSS
        """
        d = feedparser.parse("http://www.promogest.me/newsfeed")
        Environment.feedAll = d
        return

    def on_azienda_comboboxentry_changed(self, combo):
        """Imposta il nome dell'azienda

        :param combo: la combobox che ha generato l'evento
        """
        index = combo.get_active()
        if index >= 0:
            combo.get_child().set_text(combo.get_model()[index][0])

    def on_help_button_clicked(self, button):
        return

    def on_button_login_clicked(self, button=None):
        """
        """
        #username = self.username_comboxentry.child.get_text()
        username = self.username_entry.get_text()
        password = self.password_entry.get_text()
        do_login = True
        if username=='' or password=='':
            messageInfo(msg=_('Inserire nome utente e password'))
            do_login = False
        elif Environment.engine.name != "sqlite" and \
                findStrFromCombobox(self.azienda_combobox,0) == '':
            messageInfo(msg=_("Occorre selezionare un'azienda"))
            do_login = False
        else:
            #if hasattr(self,"azienda_combobox"):
            self.azienda = findStrFromCombobox(self.azienda_combobox,0)
            findComboboxRowFromStr(self.azienda_combobox, self.azienda, 0)
            found = self.azienda_combobox.get_active() != -1
            #if not found:
                #messageInfo(msg=_("Selezionare un'azienda esistente"))
                #do_login = False
            if not self.azienda:
                self.azienda = "AziendaPromo"

        if do_login: #superati i check di login
            users = User().select(username=username,
                        password=hashlib.md5(username+password).hexdigest())
            if len(users) ==1:
                if users[0].active == False:
                    messageInfo(msg=_('Utente Presente Ma non ATTIVO'))
                    dialog.destroy()
                    #saveAppLog(action="login", status=False,value=username)
                    do_login = False
                else:
                    Environment.workingYear = str(self.anno_lavoro_spinbutton.get_value_as_int())
                    Environment.azienda = self.azienda
                    if Environment.engine.name != "sqlite":
                        azs = Azienda().select(batchSize = None)
                        for a in azs:
                            a.tipo_schemaa = ""
                            a.persist()
                        uaz = Azienda().getRecord(id =self.azienda)
                        uaz.tipo_schemaa = "last"
                        uaz.persist()
                    if Environment.tipodb !="sqlite":
                        Environment.params["schema"] = self.azienda
                    # Lancio la funzione di generazione della dir di configurazione
                    Environment.set_configuration(Environment.azienda,Environment.workingYear)
#                    if setconf("Feed","feed"):
#                    if True == True:
#                        thread = threading.Thread(target=self.feddretreive)
#                        thread.start()
#                        thread.join(2.3)
                    Environment.params['usernameLoggedList'][0] = users[0].id
                    Environment.params['usernameLoggedList'][1] = users[0].username
                    try:
                        Environment.params['usernameLoggedList'][2] = users[0].id_role
                    except:
                        Environment.params['usernameLoggedList'][2] = 1
                    if hasAction(actionID=1):
                        self.login_window.hide()
                        Environment.windowGroup.remove(self.getTopLevel())
                        installId()
                        #import promogest.lib.UpdateDB

                        #saveAppLog(action="login", status=True,value=username)
                        Environment.pg2log.info("LOGIN  id, user, role azienda: %s, %s" %(repr(Environment.params['usernameLoggedList']),self.azienda ) )
                        import promogest.ui.SetConf
                        checkInstallation()
                        #gobject.idle_add(self.importModulesFromDir,'promogest/modules')
                        self.importModulesFromDir('promogest/modules')
                        def mainmain():
                            from Main import Main
                            main = Main(self.azienda or "AziendaPromo",
                                        self.anagrafiche_modules,
                                        self.parametri_modules,
                                        self.anagrafiche_dirette_modules,
                                        self.frame_modules,
                                        self.permanent_frames)
                            main.getTopLevel().connect("destroy", on_main_window_closed,
                                                self.login_window)
                            main.show()
                        gobject.idle_add(mainmain)

                    else:
                        do_login=False
            else:
                messageInfo(msg=_('Nome utente o password errati'))
                #saveAppLog(action="login", status=False,value=username)
                do_login = False

    def on_aggiorna_button_clicked(self, widget):
        """Evento associato alla richiesta di aggiornamento

        :param widget: il widget che ha generato l'evento
        """
        updateDialog = UpdateDialog(self)
        updateDialog.show()


    def groupModulesByType(self):
        """
        There are different types of modules,:
        anagrafica : add one of the principal list like customer,o sellers
        parametro : add one parameter in the parametere frame
        anagrafica_diretta : add a direct list, Vendita dettaglio is one of them
        frame :add one frame like listini or stores
        permanent_frame : ....
        """
        self.anagrafiche_modules = {}
        self.parametri_modules = {}
        self.anagrafiche_dirette_modules = {}
        self.frame_modules = {}
        self.permanent_frames = {}
        for module_name in self.modules.keys():
            if self.modules[module_name]['type'] == 'anagrafica':
                self.anagrafiche_modules[module_name] = self.modules[module_name]
            elif self.modules[module_name]['type'] == 'parametro':
                self.parametri_modules[module_name] = self.modules[module_name]
            elif self.modules[module_name]['type'] == 'anagrafica_diretta':
                self.anagrafiche_dirette_modules[module_name] = self.modules[module_name]
            elif self.modules[module_name]['type'] == 'frame':
                self.frame_modules[module_name] = self.modules[module_name]
            elif self.modules[module_name]['type'] == 'permanent_frame':
                self.permanent_frames[module_name] = self.modules[module_name]


    def importModulesFromDir(self, modules_dir):
            """Check the modules directory and automatically try to load
            all available modules

            """
            #global jinja_env
            Environment.modulesList=[Environment.tipo_pg]
            modules_folders = [folder for folder in os.listdir(modules_dir) \
                            if (os.path.isdir(os.path.join(modules_dir, folder)) \
                            and os.path.isfile(os.path.join(modules_dir, folder, 'module.py')))]
            Environment.modules_folders = modules_folders

            for m_str in modules_folders:
                if hasattr(Environment.conf,m_str) or setconf(m_str,"mod_enable", value="yes"):
                    try:
                        exec "mod_enable = getattr(Environment.conf.%s,'mod_enable')" %m_str
                    except:
                        mod_enable = setconf(m_str,"mod_enable", value="yes")
                    if mod_enable:
                        try:
                            exec "mod_enableyes = getattr(Environment.conf.%s,'mod_enable','yes')" %m_str
                        except:
                            mod_enableyes="yes"
                        if mod_enableyes=="yes":
                            stringa= "%s.%s.module" % (modules_dir.replace("/", "."), m_str)
                            m= __import__(stringa, globals(), locals(), ["m"], -1)
                            Environment.modulesList.append(str(m.MODULES_NAME))
                            if hasattr(m,"TEMPLATES"):
                                HtmlHandler.templates_dir.append(m.TEMPLATES)
                            for class_name in m.MODULES_FOR_EXPORT:
                                exec 'module = m.'+ class_name
                                self.modules[class_name] = {
                                                    'module': module(),
                                                    'type': module.VIEW_TYPE[0],
                                                    'module_dir': "%s" % (m_str),
                                                    'guiDir':m.GUI_DIR}
            Environment.pg2log.info("LISTA DEI MODULI CARICATI E FUNZIONANTI %s" %(str(repr(Environment.modulesList))))
            HtmlHandler.templates_dir.append("promogest/modules/Agenti/templates/") # da aggiungere a mano perchè al momento Agenti non è un vero e proprio modulo
            HtmlHandler.jinja_env = HtmlHandler.env(HtmlHandler.templates_dir)
            self.groupModulesByType()
            for a in Environment.modulesList[:]:
                mm = a.split(" ")
                for m in mm:
                    Environment.modulesList.append(m)
                Environment.modulesList.remove(a)

    def on_login_window_key_press_event(self, widget, event):
        """Gestisce la pressione di alcuni tasti nella finestra di login

        :param widget: -
        :param event: -
        """
        if event.type == GDK_EVENTTYPE_KEY_PRESS:
            if event.get_state() & GDK_CONTROL_MASK:
                key = str(gdk_keyval_name(event.keyval))
                if key.upper() == "L":
                    self.username_entry.set_text("admin")
                    self.password_entry.set_text('admin')
                    self.on_button_login_clicked()


def on_main_window_closed(main_window, login_window):
    """Evento associato alla chiusura della finestra di login

    """
    login_window.show()
    Environment.windowGroup.append(login_window)
    Environment.windowGroup.remove(main_window)
