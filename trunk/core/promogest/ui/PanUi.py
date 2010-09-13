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
    if setconf("Master","pan") =="SI":
        username = setconf("Master", "username")
        password = setconf("Master", "password")
        company = Environment.azienda
        azione = "SI"
        data = {"username" : username,"password":password, "company":company,
                        "pan":azione}
        url = "http://www.promotux.it/trial"
        values = urllib.urlencode(data)
        try:
            req = urllib2.Request(url, values)
            response = urllib2.urlopen(req)
            content = response.read()
            conte = json.loads(content)
            Environment.modulesList.append("pan")
            text = "PAN:<b>SI!</b>,GIORNI RESIDUI:<b> %s</b>" %str(conte["residui"])
            main.pan_label_info.set_markup(text)
        except:
            print " ERRORE NELLA GESTIONE DEL PAN"
            Environment.modulesList.append("pan")
            text = "PAN:<b>SI!</b>  GIORNI RESIDUI: <b>ND</b>"
            main.pan_label_info.set_markup(text)




class PanUi(GladeWidget):
    """ Widget di configurazione del codice installazione e dei parametri
    di configurazione """
    def __init__(self, main):
        GladeWidget.__init__(self, 'pan_window',
                                    'pan_dialog.glade')
        self.placeWindow(self.getTopLevel())
        self.rowBackGround = None
        self.main = main
        username = setconf("Master", "username")
        password = setconf("Master", "password")
        self.pan_entry_username.set_text(username)
        if setconf("Master","pan") =="SI":
            self.pan_radio_si.set_active = True
        else:
            self.pan_radio_no.set_active = True
#        self.rowBoldFont = 'arial bold 11'
#        self.show()

    def on_registrati_button_clicked(self, button):
        url ="http://www.promotux.it/userRegistration"
        webbrowser.open_new_tab(url)

    def on_pan_info_button_clicked(self, button):
        url ="http://www.promotux.it/promoGest/faq"
        webbrowser.open_new_tab(url)

    def on_pan_esegui_button_clicked(self,button):
        username = self.pan_entry_username.get_text()
        passw = self.pan_password_entry.get_text()
        company = Environment.azienda
        if self.pan_radio_si.get_active():
            azione = "SI"
        elif self.pan_radio_no.get_active():
            azione = "NO"
        if azione == "SI" and (username =="" or passw == ""):
            messageInfo(msg = """Nessun Username o password sono state inserite,
se non sei registrato fallo premendo il pulsante""")
        else:
            url = "http://www.promotux.it/trial"
            password = hashlib.md5(username + passw).hexdigest()
            data = {"username" : username,"password":password, "company":company,
                        "pan":azione}
            if azione == "NO":
                values = urllib.urlencode(data)
                req = urllib2.Request(url, values)
                response = urllib2.urlopen(req)
                content = response.read()
                conte = json.loads(content)
                if setconf("Master","pan") =="SI":
                    conf = SetConf().select(key="pan", section="Master")
                    if conf:
                        conf[0].value = "NO"
                        conf[0].persist()
            elif azione =="SI":
                values = urllib.urlencode(data)
                req = urllib2.Request(url, values)
                response = urllib2.urlopen(req)
                content = response.read()
                conte = json.loads(content)
                if conte["rows"] > 0 and conte["pan"] == "SI":
                    if setconf("Master","pan") =="NO":
                        conf = SetConf().select(key="pan", section="Master")
                        if conf:
                            conf[0].value = "SI"
                            conf[0].persist()
                    else:
                        conf = SetConf().select(key="pan", section="Master")
                        if conf:
                            c = conf[0]
                        else:
                            c = SetConf()
                        c.key="pan"
                        c.section= "Master"
                        c.value = "SI"
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
                    Environment.modulesList.append("pan")
                    text = "PAN:<b>SI!</b>,GIORNI RESIDUI: <b>%s</b>" %str(conte["residui"])
                    self.main.pan_label_info.set_markup(text)
                elif conte["rows"] < 1:
                    messageInfo(msg=""" Username o password errate, riprovare""")
                else:
                    messageInfo(msg="""NON e' possibile arrivare l'opzione
Probabilmente sono scaduti i trenta giorni, o è stata attivata e poi disattivata
prova comunque a contattarci per una soluzione""")
        self.destroy()

    def on_pan_chiudi_button_clicked(self, button):
        self.destroy()
