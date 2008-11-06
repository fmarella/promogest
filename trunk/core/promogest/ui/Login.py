# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>
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

import os, md5
import gtk, gobject
import datetime
from GladeApp import GladeApp


#from promogest.db.Connection import Connection
#from promogest.dao import Azienda
from promogest.dao.User import User
from promogest.dao.Dao import Dao
from promogest.dao.Azienda import Azienda
import promogest.dao.Azienda
from promogest import Environment
from GtkExceptionHandler import GtkExceptionHandler
from utils import hasAction,on_status_activate
from utilsCombobox import findComboboxRowFromStr
from promogest.ui.SendEmail import SendEmail
from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
import threading
from promogest.lib import feedparser

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

    def __init__(self):
        self.azienda=None
        self._dbConnString = ''

        Environment.exceptionHandler = GtkExceptionHandler()

        #azs = Dao(Azienda, isList=True).select(orderBy="schemaa")
        azs = Azienda(isList=True).select(orderBy="schemaa")
        usrs = User(isList=True).select()
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
        model_usr = gtk.ListStore(str, str)
        model_usr.clear()
        for a in usrs:
            model_usr.append((a.username, a.ruolo))
        renderer_usr = gtk.CellRendererText()
        self.username_comboxentry.pack_start(renderer_usr, True)
        self.username_comboxentry.add_attribute(renderer_usr, 'text', 0)
        self.username_comboxentry.add_attribute(renderer_usr, 'text', 1)
        self.username_comboxentry.set_model(model_usr)
        self.username_comboxentry.set_text_column(0)
        #self.username_comboxentry.set_active(0)
        data = datetime.datetime.now()
        self.anno_lavoro_spinbutton.set_value(data.year)
        if Environment.feed == "True":
            thread = threading.Thread(target=self.feddretreive)
            thread.start()
            #thread.join(1.3)
        self.getTopLevel().show_all()


    def randomSplash(self):
        import random
        randomFile = random.sample([1,2,3,4,5,6,7,8],1)[0]
        fileName = Environment.conf.guiDir + "splash["+str(randomFile)+"].png"
        return fileName


    def feddretreive(self):
        d = feedparser.parse("http://blog.promotux.it/?feed=rss2")
        Environment.feedAll = d
        #print d
        return

    def on_azienda_comboboxentry_changed(self, combo):
        index = combo.get_active()
        if index >= 0:
            combo.child.set_text(combo.get_model()[index][0])

    def on_button_help_clicked(self, button):
        sendemail = SendEmail()

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
            users = User(isList=True).select(username=username,
                                    password=md5.new(username+password).hexdigest())

            if len(users) ==1:
                Environment.workingYear = str(self.anno_lavoro_spinbutton.get_value_as_int())
                Environment.azienda = self.azienda
                Environment.set_configuration(Environment.azienda,Environment.workingYear)
                Environment.usernameLoggedList = [users[0].id, users[0].username,users[0].id_role]
                if hasAction(actionID=1):
                    Environment.params["schema"]=self.azienda
                    Environment.meta = MetaData().reflect(Environment.engine,schema=self.azienda )
                    self.login_window.hide()
                    global windowGroup
                    windowGroup.remove(self.getTopLevel())
                    from Main import Main
                    main = Main(self.azienda)
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
                do_login = False

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
