# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
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

class SendEmail(GladeWidget):
    """ Frame per la spedizione email """

    def __init__(self, string=None, d=False):
        GladeWidget.__init__(self, 'send_email', fileName= 'email_dialog.glade')
        self.placeWindow(self.getTopLevel())
        self.getTopLevel().set_modal(modal=True)
        self.getTopLevel().show_all()
        self.title_label.set_markup("""
    Questo semplice form ti permette di inviare
    <b>E-mail</b> al team di sviluppo o al settore commerciale,
    L'email verrà inviata A: <b>info@promotux.it</b>

    Grazie per il tuo contributo
                                    """)
        if string != None:
            self.preSetEmailBody(string)
        self.dist = d
        self.sobject = ""
        self.obj = ""
        try:
            from promogest.ui.utils import setconf
            if setconf("Smtp", "emailmittente"):
                self.fromaddr = str(setconf("Smtp", "emailmittente"))
                self.from_email_entry.set_text(self.fromaddr)
        except:
            pass
        try:
            fileName = Environment.conf.guiDir + 'logo_promogest.png'
            f = open(fileName,'rb')
            content = f.read()
            f.close()
            self.codec = 'Codice installazione: ' + str(hashlib.md5(content).hexdigest().upper())
        except:
            pass
            #msg = 'Impossibile generare il codice !!!'
        #self.anagrafica()
        #self.placeWindow()
        #self.setFocus()

    def preSetEmailBody(self, string=""):
        textBuffer = self.emailBody_textview.get_buffer()
        #textBuffer.set_text(self.dao.note)
        textBuffer.set_text(string)
        self.emailBody_textview.set_buffer(textBuffer)
        self.obj = self.obj_combobox.set_active(0)
        self.sobject = self.object_email_entry.set_text("Errore")

    def on_send_button_clicked(self,button):
        textBuffer = self.emailBody_textview.get_buffer()
        self.bodytext = textBuffer.get_text(textBuffer.get_start_iter(),
                                            textBuffer.get_end_iter())
        try:
            if not self.sobject:
                self.sobject= self.object_email_entry.get_text()
        except:
            pass
        self.fromm = self.from_email_entry.get_text()
        try:
            if not self.obj:
                self.obj = self.obj_combobox.get_active_text()
        except:
            pass
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
        self.toaddrs  = ["info@promotux.it"]
        msg = """%s

        %s""" %(self.codec,self.bodytext)
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
            server.login("promogestlogs@gmail.com", "pr0m0t0x")
            server.sendmail(fromaddr, total_addrs , msg)
            msg = """Invio della email riuscito!!!
            grazie per la segnalazione
             """
            messageInfo(msg=msg)
        except:
            msg = """Invio non riuscito!!!
            Riprovare in un altro momento """
            messageInfo(msg=msg)
