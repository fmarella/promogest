# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import hashlib
import os
import gtk
import datetime
import locale
from GladeApp import GladeApp
from GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.User import User
from promogest.dao.Azienda import Azienda
from promogest.dao.AppLog import AppLog
from promogest.dao.DaoUtils import saveToAppLog
from GtkExceptionHandler import GtkExceptionHandler
from utils import hasAction,on_status_activate
from utilsCombobox import findComboboxRowFromStr
from promogest.ui.SendEmail import SendEmail
from sqlalchemy import *
from sqlalchemy.orm import *
import threading
from promogest.lib import feedparser

#if hasattr(Environment.conf, "RuoliAzioni") and getattr(Environment.conf.RuoliAzioni,'mod_enable')=="yes":
    #from promogest.modules.RuoliAzioni.data.RuoliAzioniDB import *


windowGroup = []
statusIcon = gtk.StatusIcon()
statusIcon.set_from_file(Environment.conf.guiDir + 'logo_promogest_piccolo.png')
statusIcon.set_tooltip('Promogest, il Gestionale open source per la tua azienda')
visible = 1
blink = 0
screens = []

def on_activate(status):
    global visible,blink, windowGroup, screens
    visible, blink,screens = on_status_activate(status, windowGroup, visible, blink, screens)
statusIcon.connect('activate', on_activate)


class Login(GladeApp):

    def __init__(self, debugSQL=None, debugALL=None):
        self.azienda=None
        self._dbConnString = ''
        self.modules = {}
        Environment.exceptionHandler = GtkExceptionHandler()

        azs = Azienda().select(orderBy="schemaa")
        usrs = User().select()
        GladeApp.__init__(self, 'login_window')
        model = gtk.ListStore(str, str)
        model.clear()
        for a in azs:
            model.append((a.schemaa, a.denominazione))
        global windowGroup
        windowGroup.append(self.getTopLevel())
        fileSplashImage=self.randomSplash()
        self.splash_image.set_from_file(fileSplashImage)
        self.date_label.set_text(datetime.datetime.now().strftime('%d/%m/%Y  %H:%M'))
        renderer = gtk.CellRendererText()
        self.azienda_comboboxentry.pack_start(renderer, True)
        self.azienda_comboboxentry.add_attribute(renderer, 'text', 0)
        self.azienda_comboboxentry.set_model(model)
        self.azienda_comboboxentry.set_text_column(0)
        self.azienda_comboboxentry.set_active(0)

        #ATTENZIONE METTO COME RUOLO ADMIN PER IL MOMENTO RICONTROLLARE
        model_usr = gtk.ListStore(str, str)
        model_usr.clear()
        for a in usrs:
            if hasattr(Environment.conf, "RuoliAzioni") and getattr(Environment.conf.RuoliAzioni,'mod_enable')=="yes":
                model_usr.append((a.username, a.user))
            else:
                model_usr.append((a.username, "Admin"))

        renderer_usr = gtk.CellRendererText()
        self.username_comboxentry.pack_start(renderer_usr, True)
        self.username_comboxentry.add_attribute(renderer_usr, 'text', 0)
        self.username_comboxentry.add_attribute(renderer_usr, 'text', 1)
        self.username_comboxentry.set_model(model_usr)
        self.username_comboxentry.set_text_column(0)
        self.username_comboxentry.grab_focus()
        #self.username_comboxentry.set_active(0)
        data = datetime.datetime.now()
        self.anno_lavoro_spinbutton.set_value(data.year)
        #self.button_login.connect('clicked', self.on_button_login_clicked )
        self.getTopLevel().show_all()


    def randomSplash(self):
        import random
        randomFile = random.sample([1,2,3,4,5,6,7,8],1)[0]
        fileName = Environment.conf.guiDir + "splash["+str(randomFile)+"].png"
        return fileName



    def feddretreive(self):
        d = feedparser.parse("http://blog.promotux.it/?feed=rss2")
        #self.checkUpdate()
        Environment.feedAll = d
        return

    def on_azienda_comboboxentry_changed(self, combo):
        index = combo.get_active()
        if index >= 0:
            combo.child.set_text(combo.get_model()[index][0])

    def on_button_help_clicked(self, button):
        from sqlalchemy.ext.serializer import loads, dumps

        app = Environment.params["session"].query(AppLog).filter(and_(AppLog.schema_azienda =="aaaaa",AppLog.message=="INSERT Articolo")).all()
        for a in app:
            #print a.pkid
            print a.pk[0].pk_integer
            a =  loads(a.object)
            print "GGGGGGGGGG", dir(a)
            #dao = a.message.split(" ")[1]
            #query= Environment.params["session"].query(Articolo).get(id=eval(a.pkid)[0])
            #print query
        #print "INIZIAMOOOO", app
        #serialized = dumps(app)
        #print serialized
            
        #sendemail = SendEmail()

    def on_button_login_clicked(self, button=None):
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
        if do_login:
            users = User().select(username=username,
                                    password=hashlib.md5(username+password).hexdigest())

            if len(users) ==1:
                Environment.workingYear = str(self.anno_lavoro_spinbutton.get_value_as_int())
                Environment.azienda = self.azienda
                Environment.set_configuration(Environment.azienda,Environment.workingYear)
                if Environment.feed:
                    thread = threading.Thread(target=self.feddretreive)
                    thread.start()
                    #thread.join(1.3)
                Environment.params['usernameLoggedList'][0] = users[0].id
                Environment.params['usernameLoggedList'][1] = users[0].username
                if hasattr(Environment.conf, "RuoliAzioni") and getattr(Environment.conf.RuoliAzioni,'mod_enable')=="yes":
                    from promogest.modules.RuoliAzioni.dao.UserRole import UserRole
                    idruolo = UserRole().select(idUser=users[0].id)
                    if idruolo:
                        Environment.params['usernameLoggedList'][2] = idruolo[0].id_role
                else:
                    Environment.params['usernameLoggedList'][2] = "Admin"

                if hasAction(actionID=1):
                    Environment.params["schema"]=self.azienda
                    #from promogest.lib.UpdateDB import *
                    Environment.meta = MetaData().reflect(Environment.engine,schema=self.azienda )
                    self.login_window.hide()
                    global windowGroup
                    windowGroup.remove(self.getTopLevel())
                    self.importModulesFromDir('promogest/modules')
                    saveToAppLog(action="login", status=True,value=username)
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
                                    'Nome utente o password Errati')
                response = dialog.run()
                dialog.destroy()
                saveToAppLog(action="login", status=False,value=username)
                do_login = False

    def on_aggiorna_button_clicked(self, widget):
        svndialog = GladeWidget('svnupdate_dialog', callbacks_proxy=self)
        svndialog.getTopLevel().set_transient_for(self.getTopLevel())
        encoding = locale.getlocale()[1]
        utf8conv = lambda x : unicode(x, encoding).encode('utf8')
        licenseText = ''
        textBuffer = svndialog.svn_textview.get_buffer()
        textBuffer.set_text(licenseText)
        svndialog.svn_textview.set_buffer(textBuffer)
        svndialog.getTopLevel().show_all()
        response = svndialog.svnupdate_dialog.run()
        if response == gtk.RESPONSE_OK:
            command = 'svn co http://svn.promotux.it/svn/promogest2/trunk/ ~/pg2'
            p = Popen(command, shell=True,stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            (stdin, stdouterr) = (p.stdin, p.stdout)
            for line in stdouterr.readlines():
                textBuffer.insert(textBuffer.get_end_iter(), utf8conv(line))
            msg = """ Se è apparsa la dicitura "Estratta Revisione XXXX
    l'aggiornamento è riuscito, nel caso di messaggio fosse differente
    potete contattare l'assistenza tramite il numero verde 80034561
    o tramite email all'indirizzo info@promotux.it

        Aggiornamento de|l Promogest2 terminato !!!
        Riavviare l'applicazione per rendere le modifiche effettive
                    """
            dialog = gtk.MessageDialog(self.getTopLevel(),
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_OK,
                                   msg)
            dialog.run()
            dialog.destroy()
            svndialog.svnupdate_dialog.destroy()

    def groupModulesByType(self):
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
            """Check the modules directory and automatically try to load all available modules"""
            Environment.modulesList=[]
            modules_folders = [folder for folder in os.listdir(modules_dir) \
                            if (os.path.isdir(os.path.join(modules_dir, folder)) \
                            and os.path.isfile(os.path.join(modules_dir, folder, 'module.py')))]
            for m_str in modules_folders:
                if hasattr(Environment.conf,m_str):
                    exec "mod_enable = getattr(Environment.conf.%s,'mod_enable','yes')" %m_str
                    if mod_enable=="yes":
                        exec "import %s.%s.module as m" % (modules_dir.replace("/", "."), m_str)
                        Environment.modulesList.append(str(m.MODULES_NAME))
                        for class_name in m.MODULES_FOR_EXPORT:
                            exec 'module = m.'+ class_name
                            self.modules[class_name] = {
                                'module': module(),
                                'type': module.VIEW_TYPE[0],
                                'module_dir': "%s" % (m_str),
                                'guiDir':m.GUI_DIR}
            print "LISTA DEI MODULI CARICATI E FUNZIONANTI", repr(Environment.modulesList)
            self.groupModulesByType()

    def on_login_window_key_press_event(self, widget, event):
        if event.type == gtk.gdk.KEY_PRESS:
            if event.state & gtk.gdk.CONTROL_MASK:
                #try:
                key = str(gtk.gdk.keyval_name(event.keyval))
                if key.upper() == "L":
                    self.username_comboxentry.set_active(0)
                    #self.username_comboxentry.set_text('admin')
                    self.password_entry.set_text('admin')
                    self.on_button_login_clicked()
                #except:
                    #print u'Trovato!! il login non è andato a buon fine. Spiacente.'
                    #raise SystemExit


def on_main_window_closed(main_window, login_window):
    login_window.show()
    global windowGroup
    windowGroup.append(login_window)
    windowGroup.remove(main_window)
