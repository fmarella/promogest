#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2012,
#                         by Promotux Informatica - http://www.promotux.it/
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

from optparse import OptionParser
import os
import shutil
import zipfile
from  subprocess import *
import smtplib
import string
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email.mime.image import MIMEImage
from email.Header import Header
from email import Encoders
import datetime

__Version__ = "0.5"
__Author__ = "Francesco Meloni"


""" Su linux è necessario configurarlo e poi inserirlo in un crontab
che ne consenta la pianificazione
una riga di esempio è:

#esecuzione alle 23 e 50, tutti i giorni
50 23 * * *     python /home/miahome/Pg2BackupAndSend.py

Su windows dovrebbe bastare inserire lo script nelle operazioni pianificate
all'orario prescelto
"""

#SU WINDOWS SPOSTARE E LANCIARE LO SCRIPT DALLA CARTELLA BIN dentro c:\programmi\postgresql\9.0
# aggiungere .exe al pg_dump

# questa è la cartella in cui si andranno a copiare i backup
# creare una cartella e mettere il percorso completo qui
#Mettere lo / alla fine del percorso
WORKING_DIRECTORY = "/home/vete/pg-bkp/" #cambiare ma prima creare la cartella
#su windows ha bisogno dei doppi slash sempre!!!


#CARTELLA DI LAVORO DEL PROMOGEST
#Normalmente è /home/tuahome/pg2
#su windows invece è c://Document And Settings/utente/pg2


#Nome dell'azienda di cui si sta facendo il backup, nella ONE sarà
# AziendaPromo, nella PRO è il nome azienda utilizzato
AZIENDA = "AziendaPromo"

#Tipo di PromoGest installato
#Opzioni possibili ONE e PRO
TIPO_DB = "ONE"

#OPZIONI SOLO PER LA VERSIONE PRO
#Host del database
HOST = "localhost"
#Username di connessione al database
USER = "cambiare"
#password di connessione al database
DBPASSWORD = "cambiare"
#nome del database
DB_NAME = "promogest_db"
#porta di connessione
PORT = "5432"
#Livello di compressione
LIVELLO_COMPRESSIONE = "7"


#OPZIONI DI INVIO DELL'EMAIL
#Inserire gli indizzi email
MITTENTE = "cambiare"
DESTINATARIO = "cambiare"
COPIACONOSCENZA = ""
#Parte iniziale dell'oggetto dell'email
OGGETTO = "[Backup PromoGest2] "

#Questo script è in grado di utilizzare come smtp per l'invio della
#email GMAIL, questo rende lo script indipendente dal tipo di connessione utilizzata
# SE SI USA GMAIL METTERE A TRUE LA VARIAVILE GMAIL e SETTARE CORRETTAMENTE ACCOUNT E PASSWORD
# mettendo smtp.gmail.com come SMTP_SERVER

#Opzioni possibili False o True
GMAIL = False

SMTP_SERVER = "smtp.tiscali.it"
GMAIL_ACCOUNT = "indirizzo_gmail@gmail.com"
GMAIL_PASSWORD = "password_account_gmail"

CORPO_MESSAGGIO=  """

NESSUNO AL MOMENTO
"""

class Pg2BackupAndSend( object):
    """ __Versione __
        0.2 prima versione funzionante
        0.3 aggiunge l'autenticazione gmail
        0.4 Fix quando si usa con crontab è necessario usare close() e non quit()
        0.5 Aggiunta gestione Pg2 ONE
    """

    def __init__(self):
        pass

    def run(self):
        self.bakup()
        self.sendmail()
        self.server.close()
        return

    def startdir(self):
        startDir = "promogest2"
        promogestStartDir = os.path.expanduser('~') + os.sep + startDir + os.sep
        return promogestStartDir

    def bakup(self):
        """ Si prepara un file zip con il dump del DB """
        self.nameDump = "pg2_dump_"+AZIENDA+"_"+datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
        self.stname = WORKING_DIRECTORY+self.nameDump

        if TIPO_DB =="PRO":
            os.environ["PGPASSWORD"]=DBPASSWORD
            retcode = call(["pg_dump",
                            "-h",HOST,
                            "-p",PORT,
    #                        "-F","c", #compresso ma non mi piace
    #                        "-n","promotux2", # solo questo schema
    #                        "-n","promogest2", #solo questo schema
                            "-Z",LIVELLO_COMPRESSIONE,
                            "-U",USER,
                            "-f",self.stname,
                            DB_NAME])
        else:
            if os.path.exists(WORKING_DIRECTORY):
                retcode = shutil.copy(self.startdir()+"db",WORKING_DIRECTORY+self.nameDump)
                self.fileZippato = WORKING_DIRECTORY+self.nameDump+".zip"
                self.filez = zipfile.ZipFile(self.fileZippato, "w")
                self.filez.write(WORKING_DIRECTORY+self.nameDump, os.path.basename(WORKING_DIRECTORY+self.nameDump), zipfile.ZIP_DEFLATED)
                self.filez.close()
                os.remove(WORKING_DIRECTORY+self.nameDump)


        if not retcode:
            self.corpo_messaggio = "BACKUP %s EFFETTUATO CON SUCCESSO" %str(datetime.datetime.now().strftime('%d %m %Y %H %M'))
        else:
            self.corpo_messaggio = "ATTENZIONE %s  BACKUP NON RIUSCITO" %str(datetime.datetime.now().strftime('%d %m %Y %H %M'))
        return

    def _msgDef(self, text="", html="",img="", subject=""):
        msgg = MIMEMultipart()
        msgg['Subject'] = OGGETTO+str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M'))
        msgg['From'] = self._from
        msgg['To'] = self.s_toaddrs
        msgg.attach(MIMEText(text))
#        fp = open(self.stname, 'rb')
        part = MIMEBase('application','octet-stream')
        if TIPO_DB =="PRO":
            fp =open(self.stname, 'rb')
        else:
            fp =open(self.fileZippato,"rb")
        part.set_payload(fp.read())
        fp.close()
        Encoders.encode_base64(part)
        if TIPO_DB=="PRO":
            part.add_header('Content-Disposition','attachment', filename=self.nameDump+".rimuovere_questa_parte_e_mettere_zip")
        else:
            part.add_header('Content-Disposition','attachment', filename=self.fileZippato[:-4]+".rimuovere_questa_parte_e_mettere_zip")
        msgg.attach(part)

        self._send(fromaddr=self._from, total_addrs=self.s_toaddrs, msg=msgg)

    def sendmail(self):
        """ ok """
        self.s_toaddrs = string.join([x for x in [DESTINATARIO]], ",")
        self.s_bccaddrs = ""
        self._from = MITTENTE
        msg = self.corpo_messaggio
        return self._msgDef(text=msg)

    def _send(self,fromaddr=None, total_addrs=None, msg=None):
        self.server = smtplib.SMTP(SMTP_SERVER)
#        self.server.set_debuglevel(1)
        if GMAIL ==True:
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
        return self.server.sendmail(fromaddr, total_addrs , msg.as_string())


class Pg2BKP(object):
    def __init__(self):
        sla22 = Pg2BackupAndSend().run()

if __name__ == '__main__':
    Pg2BKP()
