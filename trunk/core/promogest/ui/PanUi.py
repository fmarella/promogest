# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
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

from promogest.ui.gtk_compat import *
import hashlib
from threading import Timer
from promogest.ui.utils import orda, messageInfo, setconf
from promogest.dao.Setconf import SetConf
from promogest import Environment
from GladeWidget import GladeWidget
import webbrowser
import datetime
import urllib, urllib2
try:
    import json
except:
    None

def checkPan(main):
    print "TIPO PG", Environment.tipo_pg, Environment.modulesList, ("FULL" not in Environment.modulesList)
    for a in Environment.modulesList:
        if a:
            if ("FULL" in a) or ("STANDARD" in a) or ("PRO" in a):
                text = "OPZIONE: <b>%s</b>" %(Environment.tipo_pg)
                main.pan_label_info.set_markup(text)
                Environment.pg2log.info(text)
                if "+S" in a:
                    print "ATTIVARE SHOP"
                    if not setconf("VenditaDettaglio","mod_enable",value="yes"):
                        a = SetConf()
                        a.section = "VenditaDettaglio"
                        a.tipo_section ="Modulo"
                        a.description = "Modulo Vendita Dettaglio"
                        a.tipo = "bool"
                        a.key = "mod_enable"
                        a.value = "yes"
                        a.persist()

                        a = SetConf()
                        a.section = "VenditaDettaglio"
                        a.tipo_section ="Modulo"
                        a.description = "Nome del movimento generato"
                        a.tipo = "str"
                        a.key = "operazione"
                        a.value = "Scarico venduto da cassa"
                        a.persist()

                        a = SetConf()
                        a.section = "VenditaDettaglio"
                        a.tipo_section ="Modulo"
                        a.description = "disabilita_stampa"
                        a.tipo = "bool"
                        a.key = "disabilita_stampa"
                        a.value = "True"
                        a.active = True
                        a.persist()
                return
    if  Environment.tipodb!="postgresql":
        pp = PanUi(main).draw()
        a = gtk.Label()
        a.set_text("OPZIONI MODULI")
        main.main_notebook.prepend_page(pp.pan_frame, a)
        main.main_notebook.set_current_page(0)
        text = "OPZIONE: <b>%s!</b>" %("ONE BASIC")
        main.pan_label_info.set_markup(text)
        return pp
    else:
        text = "OPZIONE: <b>%s</b>" %(Environment.tipo_pg)
        main.pan_label_info.set_markup(text)
        Environment.pg2log.info(text)
#        main.main_notebook.set_current_page(4)


class PanUi(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, main):
        GladeWidget.__init__(self, 'pan_vbox',
                                    'pan_dialog.glade')
#        self.placeWindow(self.getTopLevel())
        self.rowBackGround = None
        self.main = main


    def draw(self):
        return self

    def on_registrati_button_clicked(self, button):
        url ="http://www.promogest.me/userRegistration"
        webbrowser.open_new_tab(url)

    def on_one_main_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/preventivo_one"
        webbrowser.open_new_tab(url)

    def on_pro_main_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)

    def on_promowear_main_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)

    def on_promoshop_main_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)

    def on_promowear_one_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/preventivo_one"
        webbrowser.open_new_tab(url)


    def on_promowear_pro_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)

    def on_promoshop_one_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/preventivo_one"
        webbrowser.open_new_tab(url)

    def on_promoshop_pro_button_clicked(self, button):
        url ="http://www.promogest.me/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)


    def on_acquista_button_clicked(self, button):
        if self.main.pp.lite_radio.get_active():
            url ="http://www.promogest.me/promoGest/preventivo_lite"
            webbrowser.open_new_tab(url)
        elif self.main.pp.pro_radio.get_active():
            url ="http://www.promogest.me/promoGest/preventivo_pro"
            webbrowser.open_new_tab(url)
        elif self.main.pp.promowear_radio.get_active():
            messageInfo(msg="NON ancora disponibile")
            return
            url ="http://www.promogest.me/promoGest/preventivo_promowear"
            webbrowser.open_new_tab(url)
        elif self.main.pp.promoshop_radio.get_active():
            messageInfo(msg="NON ancora disponibile")
            return
            url ="http://www.promogest.met/promoGest/preventivo_promoshop"
            webbrowser.open_new_tab(url)
