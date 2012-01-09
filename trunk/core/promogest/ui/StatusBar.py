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
from promogest.ui.gtk_compat import *
import datetime
from  subprocess import *
from promogest import Environment
from utils import on_status_activate, checkInstallation, setconf
from utilsCombobox import findComboboxRowFromStr
from sqlalchemy import *
from sqlalchemy.orm import *


visible = 1
blink = 0
screens = []


class Pg2StatusIcon(gtk.StatusIcon):
    def __init__(self):

        gtk.StatusIcon.__init__(self)
        menu = '''
            <ui>
             <menubar name="Menubar">
              <menu action="Menu">
               <menuitem action="Preferences"/>
               <separator/>
               <menuitem action="About"/>
               <menuitem action="Exit"/>
              </menu>
             </menubar>
            </ui>
        '''

        actions = [
            ('Menu',  None, 'Menu'),
            ('Preferences', gtk.STOCK_PREFERENCES, '_Preferences...', None,
                                'tooltip preferences', self.on_preferences),
            ('About', gtk.STOCK_ABOUT, '_About', None, 'tooltip About',
                                 self.on_about),
            ('Exit', gtk.STOCK_QUIT, '_Exit', None, 'tooltip Exit',
                                 self.on_close)
            ]
        actionGroup = gtk.ActionGroup("Actions")
        actionGroup.add_actions(actions)
        self.manager = gtk.UIManager()
        self.manager.insert_action_group(actionGroup, 0)
        self.manager.add_ui_from_string(menu)
        self.menu = self.manager.get_widget('/Menubar/Menu/About').props.parent
        #self.set_from_file(Environment.conf.guiDir + 'logo_promogest_piccolo.png')
        #self.set_tooltip('Promogest, il Gestionale open source per la tua azienda')
        self.connect('activate', self.on_activate)
        self.connect('popup-menu', self.on_popup_menu)

    def on_activate(self, data):
        """
        Funzione per la gestione dell'icona nel sys tray
        """
#        windowGroup = Environment.windowGroup
        global visible,blink, screens
        visible, blink,screens = on_status_activate(self,
                                                     Environment.windowGroup,
                                                      visible, blink, screens)
                                #statusIcon.connect('activate', on_activate)

    def on_popup_menu(self, status, button, time):
        self.menu.popup(None, None, None, button, time)

    def on_close(self, data):
        gtk.main_quit()

    def on_preferences(self, data):
        #if not hasAction(actionID=14):return
        #from promogest.ui.Main import ConfiguraWindow
        #configuraWindow = ConfiguraWindow(self)
        #showAnagrafica(self.getTopLevel(), configuraWindow)
        print "clicked on preferences"


    def on_about(self, data):
        """ and this one to show the about box """
        about = gtk.AboutDialog()
        about.set_name("PromoGest2")
        about.set_version("svn")
        about.set_copyright("Promotux 2011")
        about.set_license("license")
        about.set_website("http://www.promogest.me")
        about.set_authors(["Francesco <francesco@promotux.it>"])
        try:
            about.set_logo(GDK_PIXBUF_NEW_FROM_FILE(Environment.conf.guiDir + 'logo_promogest_piccolo.png'))
        except:
            pass
        about.set_comments("Gestionale multipiattaforma per la tua impresa")
        about.run()
        about.destroy()
