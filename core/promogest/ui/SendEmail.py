# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from promogest.ui.gtk_compat import *
import os
from datetime import datetime, timedelta
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
import smtplib, string
import datetime
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import findStrFromCombobox


class SendEmail(GladeWidget):
    """ Frame per la spedizione email """

    def __init__(self, string=None, d=False):
        GladeWidget.__init__(self, root='send_email', path='email_dialog.glade')
        self.placeWindow(self.getTopLevel())
        #self.getTopLevel().set_modal(True)
        self.getTopLevel().show_all()
        if string != None:
            self.preSetEmailBody(string)
        self.dist = d
        self.sobject = ""
        self.obj = ""
        if setconf("Smtp", "emailmittente"):
            self.fromaddr = str(setconf("Smtp", "emailmittente"))
            self.from_email_entry.set_text(self.fromaddr)

    def preSetEmailBody(self, string=""):
        textview_set_text(self.emailBody_textview, string)
        self.obj = self.obj_combobox.set_active(0)
        self.sobject = self.object_email_entry.set_text("Errore")

    def on_send_button_clicked(self,button):
        self.bodytext = textview_get_text(self.emailBody_textview)
        if not self.sobject:
            self.sobject = self.object_email_entry.get_text()
        self.fromm = self.from_email_entry.get_text()
        if "@" not in self.fromm:
            msg = """Indirizzo email non corretto"""
            messageInfo(msg=msg)
            return
        if not self.obj:
            self.obj = findStrFromCombobox(self.obj_combobox, 0)
        if self.bodytext == "" or self.sobject == ""  or self.fromm == "" or self.obj == "":
            msg = """Alcuni campi mancanti, sei pregato di ricontrollare e compilare
            il form in ogni sua parte, Grazie"""
            messageInfo(msg=msg)
        else:
            self.sendMailFunc()
            self.hide()
        if self.dist:
            gtk.main_quit()

    def on_cancel_button_clicked(self, button):
        self.hide()
        if self.dist:
            gtk.main_quit()

    def sendMailFunc(self):
        """ sistemiamo i parametri per la email
            in questa funzione ci sono anche le liste per i CC e BCC oltre al TO:
        """
        self.total_addrs = []
        self.toaddrs  = ["assistenza@promogest.me"]
        msg = """

        %s""" %(self.bodytext)
        subject = self.obj + "  " + self.sobject
        self.fromaddr = self.fromm.strip()
        self.bccaddrs = ["assistenza@promotux.it"]
        for i in self.toaddrs:
            self.total_addrs.append(i)
        for i in self.bccaddrs:
            self.total_addrs.append(i)
        self.s_toaddrs = string.join(self.toaddrs, ",")
        self.s_bccaddrs = string.join(self.bccaddrs, ",")
        self._msgDef(msg, subject)


    def _msgDef(self, msg, subject):
        msg = """\
To: %s
From: %s
Subject: %s
Bcc: %s

    %s

    %s
        """ % (self.s_toaddrs, self.fromaddr, subject, self.s_bccaddrs, msg,self.fromm.strip())
        self._send(fromaddr=self.fromaddr, total_addrs=self.total_addrs, msg=msg)

    def _send(self,fromaddr=None, total_addrs=None, msg=None):
        try:
            server = smtplib.SMTP("smtp.gmail.com")
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("promogestlogs@gmail.com", "pr0m0t0x5")
            #print " fromADDR", fromaddr, total_addrs
            server.sendmail(fromaddr, total_addrs , msg)
            msg = """Invio della email riuscito!!!
            grazie per la segnalazione
             """
            messageInfo(msg=msg)
        except:
            msg = """Invio non riuscito!!!
            Riprovare in un altro momento """
            messageInfo(msg=msg)
