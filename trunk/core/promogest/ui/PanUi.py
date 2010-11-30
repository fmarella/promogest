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

import gtk
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
    print "TIPO PG", Environment.tipo_pg
    if "Pagamenti" not in  Environment.modulesList and \
        "Promemoria" not in Environment.modulesList and \
        "ONE STANDARD" not in Environment.modulesList and \
        "ONE FULL" not in Environment.modulesList and \
        "PRO BASIC" not in Environment.modulesList and \
        "PRO STANDARD" not in  Environment.modulesList and\
        Environment.tipodb=="postgresql":
        pp = PanUi(main).draw()
        a = gtk.Label()
        a.set_text("OPZIONI MODULI")
        main.main_notebook.prepend_page(pp.pan_frame, a)
        main.main_notebook.set_current_page(0)
        text = "OPZIONE:<b>%s!</b>" %("NESSUNA")
        main.pan_label_info.set_markup(text)
        return pp
    else:
        text = "OPZIONE:<b>%s!</b>" %(Environment.tipo_pg)
        main.pan_label_info.set_markup(text)
        main.main_notebook.set_current_page(4)


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
        url ="http://www.promotux.it/userRegistration"
        webbrowser.open_new_tab(url)

    def on_one_main_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/preventivo_one"
        webbrowser.open_new_tab(url)

    def on_pro_main_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)

    def on_promowear_main_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)

    def on_promoshop_main_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)

    def on_promowear_one_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/preventivo_one"
        webbrowser.open_new_tab(url)


    def on_promowear_pro_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)

    def on_promoshop_one_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/preventivo_one"
        webbrowser.open_new_tab(url)

    def on_promoshop_pro_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/preventivo_pro"
        webbrowser.open_new_tab(url)


    def on_acquista_button_clicked(self, button):
        if self.main.pp.lite_radio.get_active():
            url ="http://www.promotux.it/promoGest/preventivo_lite"
            webbrowser.open_new_tab(url)
        elif self.main.pp.pro_radio.get_active():
            url ="http://www.promotux.it/promoGest/preventivo_pro"
            webbrowser.open_new_tab(url)
        elif self.main.pp.promowear_radio.get_active():
            messageInfo(msg="NON ancora disponibile")
            return
            url ="http://www.promotux.it/promoGest/preventivo_promowear"
            webbrowser.open_new_tab(url)
        elif self.main.pp.promoshop_radio.get_active():
            messageInfo(msg="NON ancora disponibile")
            return
            url ="http://www.promotux.it/promoGest/preventivo_promoshop"
            webbrowser.open_new_tab(url)


    def on_pan_esegui_button_clicked(self,button):
        username = self.main.pp.pan_entry_username.get_text()
        passw = self.main.pp.pan_password_entry.get_text()
        company = Environment.azienda
        if self.main.pp.pan_radio_si.get_active():
            azione = "PAN"
#        elif self.main.pp.pan_radio_no.get_active():
#            azione = "NO"
        elif self.main.pp.basic_radio.get_active():
            azione = "BASIC"
        if (azione == "PAN" or azione == "BASIC") and (username =="" or passw == ""):
            messageInfo(msg = """Nessun Username o password sono state inserite,
se non sei registrato fallo premendo il pulsante 'registrati sito'""")
        else:
            url = "http://www.promotux.it/trial"
#            url = "http://localhost:8080/trial"
            password = hashlib.md5(username + passw).hexdigest()
            data = {"username" : username,"password":password, "company":company,
                        "pan":azione}
            if azione =="PAN" or azione == "BASIC":
                values = urllib.urlencode(data)
                req = urllib2.Request(url, values)
                response = urllib2.urlopen(req)
                t = Timer(5.0, response.close)
                t.start()
                content = response.read()
                conte = json.loads(content)
                if conte["rows"] > 0 and (conte["pan"] == "PAN" or conte["pan"] == "BASIC"):
                    conf = SetConf().select(key="pan", section="Master")
                    if conf:
                        c = conf[0]
                    else:
                        c = SetConf()
                    c.key="pan"
                    c.section= "Master"
                    c.value = conte["pan"]
                    c.active = True
                    c.visible = False
                    c.persist()
                    dd = SetConf().select(key="username", section="Master")
                    if dd:
                        d = dd[0]
                    else:
                        d = SetConf()
                    d.key="username"
                    d.value = username
                    d.section = "Master"
                    d.active = True
                    d.visible = False
                    d.persist()
                    ee = SetConf().select(key="password", section="Master")
                    if ee:
                        e = ee[0]
                    else:
                        e = SetConf()
                    e.key= "password"
                    e.section = "Master"
                    e.value = password
                    e.visible = False
                    e.active = True
                    e.persist()
                    if conte["pan"] == "PAN":
                        Environment.modulesList.append("pan")
                        text = "OPZIONE:<b>PAN!</b>,GIORNI RESIDUI: <b>%s</b>" %str(conte["residui"])
                    elif conte["pan"] == "BASIC":
                        Environment.modulesList.append("basic")
                        text = "OPZIONE:<b>BASIC!</b>,GIORNI RESIDUI: <b>%s</b>" %str(conte["residui"])
                    self.main.pan_label_info.set_markup(text)
                    self.main.main_notebook.remove_page(0)
                elif conte["rows"] < 1:
                    messageInfo(msg=""" Username o password errate, riprovare""")
                else:
                    messageInfo(msg="""NON e' possibile attivare l'opzione
Probabilmente sono scaduti i trenta giorni, o è stata attivata e poi disattivata
prova comunque a contattarci per una soluzione""")
