# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
import gtk
import datetime
import threading
from  subprocess import *
from GladeApp import GladeApp
from promogest import Environment
from promogest.dao.User import User
from promogest.dao.Azienda import Azienda
from GtkExceptionHandler import GtkExceptionHandler
from utils import hasAction,checkAggiorna, aggiorna, checkInstallation, setconf
from utilsCombobox import findComboboxRowFromStr
from promogest.ui.SendEmail import SendEmail
import sqlalchemy
Environment.pg2log.info("SQLALCHEMY:"+str(sqlalchemy.__version__))
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.lib import feedparser
from promogest.lib import HtmlHandler
from promogest.ui.StatusBar import Pg2StatusIcon

#754181316

class Login(GladeApp):

    def __init__(self, debugSQL=None, debugALL=None, shop=False):
        """
        Login windows
        @param debugSQL=None: not used at this moment
        @type debugSQL=None: Boolean
        @param debugALL=None: not used at this moment
        @type debugALL=None: Boolean
        """

        statu = Pg2StatusIcon()
        self.azienda=None
        self._dbConnString = ''
        self.modules = {}
        self.shop =shop
        GladeApp.__init__(self, 'login_window')
        Environment.exceptionHandler = GtkExceptionHandler()
        checkAggiorna()
        self.draw()
        self.getTopLevel().show_all()


    def draw(self):
        model = gtk.ListStore(str, str)
        model.clear()
        usrs = User().select(batchSize = None)
        azs = Azienda().select(batchSize = None,orderBy=Azienda.schemaa) #lista aziende
        for a in azs:
            model.append((a.schemaa, a.denominazione))
        Environment.windowGroup.append(self.getTopLevel())
        if Environment.engine.name == "sqlite": #forzo lo splash per lite
            fileSplashImage = "gui/splash_pg2_lite.png"
        else:
            fileSplashImage=self.randomSplash() #splash random
        self.splash_image.set_from_file(fileSplashImage)
        dateTimeLabel = datetime.datetime.now().strftime('%d/%m/%Y  %H:%M')
        self.date_label.set_text(dateTimeLabel)
        renderer = gtk.CellRendererText()
        self.azienda_comboboxentry.pack_start(renderer, True)
        self.azienda_comboboxentry.add_attribute(renderer, 'text', 0)
        self.azienda_comboboxentry.set_model(model)
        self.azienda_comboboxentry.set_text_column(0)
        self.azienda_comboboxentry.set_active(0)
        #ATTENZIONE METTO COME RUOLO ADMIN PER IL MOMENTO RICONTROLLARE
        model_usr = gtk.ListStore(str, str)
        model_usr.clear()
        if hasattr(Environment.conf, "RuoliAzioni") and getattr(Environment.conf.RuoliAzioni,'mod_enable')=="yes":
            for a in usrs:
                model_usr.append((a.username, a.email))
        else:
            model_usr.append(("admin", "admin"))

        renderer_usr = gtk.CellRendererText()
        self.username_comboxentry.pack_start(renderer_usr, True)
        self.username_comboxentry.add_attribute(renderer_usr, 'text', 0)
        self.username_comboxentry.add_attribute(renderer_usr, 'text', 1)
        self.username_comboxentry.set_model(model_usr)
        self.username_comboxentry.set_text_column(0)
        self.username_comboxentry.grab_focus()
        data = datetime.datetime.now()
        self.anno_lavoro_spinbutton.set_value(data.year)

    def randomSplash(self):
        """
        take a random splash for pg2 login window
        """
        import random
        randomFile = random.sample([1,2,3,4,5,6,7,8],1)[0]
        fileName = Environment.conf.guiDir + "splash["+str(randomFile)+"].png"
        return fileName

    def feddretreive(self):
        """ FIXME """
        d = feedparser.parse("http://www.promotux.it/newsfeed")
        Environment.feedAll = d
        return

    def on_azienda_comboboxentry_changed(self, combo):
        """
        company combobox manage
        """
        index = combo.get_active()
        if index >= 0:
            combo.child.set_text(combo.get_model()[index][0])

    def on_help_button_clicked(self, button):
        return
        #"""
        #Help button, open sendmail widget
        #"""
        #docu = DocuView()
        ##sendemail = SendEmail()
        ##print "INIZIAMO MALE"

    def on_button_login_clicked(self, button=None):
        """
        """
        username = self.username_comboxentry.child.get_text()
        password = self.password_entry.get_text()
        do_login = True
        if username=='' or password=='':
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                       'Inserire nome utente e password')
            response = dialog.run()
            dialog.destroy()
            do_login = False
        elif self.azienda_comboboxentry.child.get_text() == '':
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                       "Occorre selezionare un'azienda")
            response = dialog.run()
            dialog.destroy()
            do_login = False
        else:
            self.azienda = self.azienda_comboboxentry.child.get_text()
            findComboboxRowFromStr(self.azienda_comboboxentry, self.azienda, 0)
            found = self.azienda_comboboxentry.get_active() != -1
            if not found:
                dialog = gtk.MessageDialog(self.getTopLevel(),
                                            gtk.DIALOG_MODAL
                                            | gtk.DIALOG_DESTROY_WITH_PARENT,
                                            gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                            "Selezionare un'azienda esistente")
                response = dialog.run()
                dialog.destroy()
                do_login = False
        if do_login: #superati i check di login
            users = User().select(username=username,
                                        password=hashlib.md5(username+password).hexdigest())
            if len(users) ==1:
                if users[0].active == False:
                    dialog = gtk.MessageDialog(self.getTopLevel(),
                                    gtk.DIALOG_MODAL
                                    | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                    'Utente Presente Ma non ATTIVO')
                    response = dialog.run()
                    dialog.destroy()
                    #saveAppLog(action="login", status=False,value=username)
                    do_login = False
                else:
                    Environment.workingYear = str(self.anno_lavoro_spinbutton.get_value_as_int())
                    Environment.azienda = self.azienda
                    if Environment.tipodb !="sqlite":
                        Environment.params["schema"]=self.azienda
                    # Lancio la funzione di generazione della dir di configurazione
                    Environment.set_configuration(Environment.azienda,Environment.workingYear)
#                    if setconf("Feed","feed"):
#                    if True == True:
#                        thread = threading.Thread(target=self.feddretreive)
#                        thread.start()
#                        thread.join(2.3)
                    Environment.params['usernameLoggedList'][0] = users[0].id
                    Environment.params['usernameLoggedList'][1] = users[0].username

                    if hasattr(Environment.conf, "RuoliAzioni") and getattr(Environment.conf.RuoliAzioni,'mod_enable')=="yes":
                        #from promogest.modules.RuoliAzioni.dao.Role import Role
                        #idruolo = Role().select(denominazione=users[0].id_role)
                        #if idruolo:
                        Environment.params['usernameLoggedList'][2] = users[0].id_role
                    else:
                        Environment.params['usernameLoggedList'][2] = "Admin"
                    if hasAction(actionID=1):
                        self.login_window.hide()
                        Environment.windowGroup.remove(self.getTopLevel())

                        import promogest.lib.UpdateDB
                        self.importModulesFromDir('promogest/modules')
                        #saveAppLog(action="login", status=True,value=username)
                        Environment.pg2log.info("LOGIN  id, user, role azienda: %s, %s" %(repr(Environment.params['usernameLoggedList']),self.azienda) )
                        import promogest.ui.SetConf
                        checkInstallation()
                        from Main import Main
                        main = Main(self.azienda,
                                    self.anagrafiche_modules,
                                    self.parametri_modules,
                                    self.anagrafiche_dirette_modules,
                                    self.frame_modules,
                                    self.permanent_frames)
                        main.getTopLevel().connect("destroy", on_main_window_closed,
                                            self.login_window)
                        main.show()

                    else:
                        do_login=False
            else:
                dialog = gtk.MessageDialog(self.getTopLevel(),
                                    gtk.DIALOG_MODAL
                                    | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                    'Nome utente o password errati')
                response = dialog.run()
                dialog.destroy()
                #saveAppLog(action="login", status=False,value=username)
                do_login = False

    def on_aggiorna_button_clicked(self, widget):
        """
        Upgrande button signal clicked
        """
        aggiorna(self)

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
            """
            Check the modules directory and automatically try to load all available modules
            """
            #global jinja_env
            Environment.modulesList=[]
            modules_folders = [folder for folder in os.listdir(modules_dir) \
                            if (os.path.isdir(os.path.join(modules_dir, folder)) \
                            and os.path.isfile(os.path.join(modules_dir, folder, 'module.py')))]
            for m_str in modules_folders:
                if hasattr(Environment.conf,m_str):
                    exec "mod_enable = hasattr(Environment.conf.%s,'mod_enable')" %m_str
                    if mod_enable:
                        exec "mod_enableyes = getattr(Environment.conf.%s,'mod_enable','yes')" %m_str
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
            HtmlHandler.jinja_env = HtmlHandler.env(HtmlHandler.templates_dir)
            self.groupModulesByType()

    def on_login_window_key_press_event(self, widget, event):
        """
        key press signal on login window
        """
        if event.type == gtk.gdk.KEY_PRESS:
            if event.state & gtk.gdk.CONTROL_MASK:
                key = str(gtk.gdk.keyval_name(event.keyval))
                if key.upper() == "L":
                    self.username_comboxentry.set_active(0)
                    self.password_entry.set_text('admin')
                    self.on_button_login_clicked()

def on_main_window_closed(main_window, login_window):
    """
    main windows close event in login windows
    """
    login_window.show()
    Environment.windowGroup.append(login_window)
    Environment.windowGroup.remove(main_window)
