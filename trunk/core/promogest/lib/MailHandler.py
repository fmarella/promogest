#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import smtplib
import string
import hashlib
from promogest.lib.webutils import setconf_web
from promogest.dao.Setconf import SetConf
from promogest import Environment
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.Header import Header


class SendMail(object):

    def __init__(self, req, to=[], _from=[], subdomain=None):
        self.req = req
        self.subdomain = subdomain
        if not self.subdomain:
            self.subdomain = ""
        if to =="me":
            self.to = [setconf("ccn_email")] # mi faccio mandare l'email
        elif to:
            self.to  = [to]
        else:
            self.to  = [req.form.get('email')]
        if _from:
            self._from = _from
        else:
            self._from = setconf("from_email")

    def addDataFormInEmail(self):
        """ Crea una stringa dai dati del form """
        a = ""
        for g,v in self.req.form.iterlists():
            a = a + str(g)+" : "+str(v[0])+"\n"
        return a

    def prepareaddresses(self):
        self.total_addrs = []
        if type(setconf("ccn_email")) == type(["ciao"]):
            self.bccaddrs = setconf("ccn_email")
        else:
            self.bccaddrs = [setconf_web("ccn_email")]
        for i in self.to:
            self.total_addrs.append(i)
        for i in self.bccaddrs:
            self.total_addrs.append(i)
        print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", self.to
        self.s_toaddrs = string.join(self.to, ",")
        self.s_bccaddrs = string.join(self.bccaddrs, ",")


    def sendRegisterUser(self):
        """
        Email abbinata alla registrazione utente
        """
        registrazioneOggetto = "%s Registrazione in attesa di attivazione" %setconf_web("name")
        registrazioneBody = """Gentile utente, la sua richiesta di registrazione e' stata inoltrata correttamente
        ed e' in attesa di essere approvata dal team di %s.

        Le ricordiamo che i suoi dati di connessione saranno:

        %s

        A Presto
        Staff %s
            """ %( setconf_web("name"),
                self.addDataFormInEmail(),
                setconf("name"))

        self._msgDef(text = registrazioneBody, subject = registrazioneOggetto)
#        self.sendRegMail()

    def sendIP(self,form =None):
        """
        Spedisce l'ip
        """
        name = form["name"]
        email = form['email']
        reqs = form['reqs']
        ip = form['ip']
        subject =self.req.url_root[7:]+self.subdomain+" "+ "IP utente: " +ip
        msg = """
        NOME: %s
        EMAIL: %s
        IP: %s

        REQ: %s
        """ %(name, email, ip, reqs)
        self.to  = ["info@promotux.it"]
        self._from = email
        self._msgDef(text=msg, subject = subject)



    def sendRecoveryPassword(self, newpasswd=None):
        """ok"""

        subject = "[Recupera Password] %s " %setconf("name")
        text = """Di seguito trovera' la password generata
in maniera casuale dal sistema. Le ricordiamo che e' possibile
modificarla in qualsiasi momento attraverso l'apposita voce nel menu'.


        %s

Grazie per aver scelto %s
        """ % (newpasswd,setconf("name"))
        html = """\
<html>
  <head></head>
  <body>
    <p>Salve, <br>
       Di seguito trover&aacute; la password generata<br>
in maniera casuale dal sistema. Le ricordiamo che &egrave; possibile<br>
modificarla in qualsiasi momento attraverso l'apposita voce nel men&uacute;.<br>
<br><br>

        %s
<br><br>
Grazie per aver scelto %s
  </body>
</html>
""" % (newpasswd,setconf("name"))
        self._msgDef(text=text,html=html, subject = subject)

    def sendContact(self, form=None):
        """ok"""
        subject = self.req.url_root[7:]+self.subdomain+" "+ form["oggetto"]
        text = """
        Contatto:
        NOME: %s
        COGNOME: %s
        TELEFONO: %s
        AZIENDA: %s
        CITTA': %s
        INDIRIZZO: %s
        EMAIL: %s

        HA FATTO QUESTA RICHIESTA:

        %s
        """ % (form["name"],form["lastname"],form["telephone"],form["company"],
                form["city"],form["address"], form["email"], form["body"] )
#        self.to  = ["info@promotux.it"]
        self._from = form["email"]
        self._msgDef(text=text, subject=subject)
        self.cortesia(to=form["email"], tipo="contatto" )

    def cortesia(self, to=None, tipo=""):
        """ funzione che gestisce le risposte agli utenti """
        subject = self.req.url_root[7:]+self.subdomain+" "+"Risposta di cortesia"
        self.to = [to]
        self._from = "info@promotux.it"
        if tipo =="contatto":
            tp = " averci contattato, riceverete una risposta al piu' presto"
        elif tipo =="registrazione":
            tp =" esservi registrati sul sito , la vostra iscrizione verra' verificata il prima possibile"
        elif tipo=="attivazione":
            tp =" esservi registrati sul sito , Il vostro account è stato attivato"
        msg = """

        Grazie per %s

        Lo Staff

        """ %tp
        self._msgDef(text=msg, subject = subject)


    def sendRegisterCodeToUser(self, to=None, userid=None):
        """
        Spedisce il codice di attivazione
        """
        from promogest.dao.ConfirmRegistration import ConfirmRegistration
        from promogest.lib.webutils import createRandomString
        #code = "PIPPO
        codeencr = createRandomString(num=5).upper()
        cr = ConfirmRegistration()
        cr.id_user= userid
        cr.code = codeencr
        cr.verified = False
        cr.persist()
        registrazioneOggetto = "Conferma email giustopeso"
        registrazioneBody = """Gentile utente, questa è l'email di
        conferma del suo indirizzo email

        Prema su questo link o copi/incolli sul suo browser:

        %s/code/%s

        A Presto
        Staff %s
            """ %( setconf("uri"),
                codeencr,
                setconf("name"))

        self._msgDef(text=registrazioneBody, subject=registrazioneOggetto)
#        self.sendRegMail()

    def sendStdMail(self):
        """ ok """
        msg = """\
        %s
        """ % Environment.params['bodytext']
        self.total_addrs = self.total_addrs[:1]

        self._msgDef(msg, subject = self.subject)


    def sendStdHTMLMail(self, html="",subject=""):
        """ ok """
        self._msgDef(html=html, subject = subject)

    def sendRegMail(self):
        """ ok """
        subject = "[%s] Nuova iscrizione" %setconf("name")
        msg = """
        Iscrizione avvenuta con successo:

        %s
        """ %(  setconf("name"))
        self._msgDef(text=msg, subject = subject)

    def sendActiveUserMail(self):
        """ ok """
        msg = Environment.activeUserBody
        self._msgDef(text=msg, subject = self.subject)


    def _msgDef(self, text="", html="",img="", subject=""):
        self.prepareaddresses()
        header_charset = 'UTF-8'
        for body_charset in 'US-ASCII', 'ISO-8859-15', 'UTF-8':
            try:
                text.encode(body_charset)
                html.encode(body_charset)
            except UnicodeError:
                pass
            else:
                break
        print "ADDRESSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", self._from, self.s_toaddrs, self.s_bccaddrs
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(unicode(subject), header_charset)
        msg['From'] = self._from
        msg['To'] = self.s_toaddrs
#        msg["Bcc"] = self.s_bccaddrs
        if text:
            part1 = MIMEText(text.encode(body_charset), 'plain', body_charset)
            msg.attach(part1)
        if html:
            part2 = MIMEText(html.encode(body_charset), 'html', body_charset)
            msg.attach(part2)
#        if img:
#            fp = open(img, 'rb')
#            imgg = MIMEImage(fp.read())
#            fp.close()
#            msg.attach(imgg)
        self._send(fromaddr=self._from, total_addrs=self.total_addrs, msg=msg)

    def _send(self,fromaddr=None, total_addrs=None, msg=None):
        server = smtplib.SMTP(str(SetConf().select(key="smtpserver")[0].value))
        server.set_debuglevel(1)
        server.sendmail(fromaddr, total_addrs , msg.as_string())
        server.quit()
