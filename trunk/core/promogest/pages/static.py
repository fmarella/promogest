#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
""" gestione delle pagine statiche non gestite da CMS"""

import hashlib
import time
import datetime
from core import Environment
from core.lib.utils import *
from core.lib.page import Page
from core.dao.Setconf import SetConf
from core.dao.StaticPages import StaticPages
from core.lib.MailHandler import SendMail
from core.dao.Province import Province
from core.dao.Regioni import Regioni
from core.dao.PersonaGiuridica import PersonaGiuridica_ as PersonaGiuridica
from core.dao.User import User
from core.dao.DestinazioneMerce import DestinazioneMerce
from core.dao.ConfirmRegistration import ConfirmRegistration
import json
from core.dao.News import News


def dls(req, static=None, subdomain=None):
    """
    Pagina di gestione del download per windows
    """
    href = req.args.get('hf')
    if href =="win":
        pg = StaticPages(req=req).getRecord(id=7)
        if not pg.clicks:
            pg.clicks = 1
        else:
            pg.clicks +=1
        pg.persist()
        pageData = {'file' : 'download_win_exe',
                    "subdomain": addSlash(subdomain),
                    "hf": "ftp://ftp.promotux.it/PromoGest2_setup.exe"}
        return Page(req).render(pageData)
    else:
        redirectUrl=addSlash(subdomain)
        return Page(req).redirect(redirectUrl)

def contacts(req, static=None, subdomain=None):
    """
    funzione per la cattura dati form contatti
    """
    captchamd5=""
    captcha = req.form.get('captcha')
    stringmd5 = req.form.get('string')
    if captcha:
        captchamd5 = hashlib.md5(captcha).hexdigest()
    if not captcha:
        string = createcaptcha()
        pageData = {'file' : 'contacts',
                    "subdomain": subdomain,
                    'string':hashlib.md5(string).hexdigest(),
                    'sent' : "False"}
        return Page(req).render(pageData)
    elif captchamd5 == stringmd5:
        SendMail(req=req, subdomain=subdomain, to="me").sendContact(form=req.form)
        pageData = {'file' : 'contacts',
                    "subdomain": subdomain,
                    'sent' : "True"}
        return Page(req).render(pageData)
    else:
        string = createcaptcha()
        print "ERRORE NEL RICONOSCIMENTO DEL captcha", string ,captcha
        pageData = {'file' : 'contacts',
                    "subdomain": subdomain,
                    'string':hashlib.md5(string).hexdigest(),
                    'sent' : "False"}
        return Page(req).render(pageData)


def registration(req, static=None, subdomain=None):
    captchamd5=""
    ml = True
    forms = req.form.to_dict()
    province = Province().select(batchSize=None)
    regioni = Regioni().select(batchSize=None)
    if req.args.get('new') =="":
        captcha = req.form.get('captcha')
        string = req.form.get('string')
        username = req.form.get('username')
        password = req.form.get('password')
        re_password = req.form.get('re-password')
        citta = req.form.get('citta')
        provincia = req.form.get('provincia')
        regione = req.form.get('regione')
        email = req.form.get('email')
        re_email = req.form.get('re_email')
        url = req.form.get('url')
        nome = req.form.get('nome')
        cognome = req.form.get('cognome')
        mailing_list = req.form.get('mailing_list')
        if not mailing_list:
            ml = False
        if captcha:
            captchamd5 = hashlib.md5(captcha).hexdigest()
        if captchamd5 == string:

            if str(re_email).strip() != str(email).lower().strip():
                error = """<br/><br/><center>I due indirizzi email non sono uguali</center>"""
                string = createcaptcha()
                pageData = {'file' : 'userRegistration',
                            "error": error,
                            "forms":forms,
                            "subdomain": addSlash(subdomain),
                            "province":province ,
                            "regioni" :regioni,
                            'string':hashlib.md5(string).hexdigest(),
                            'sent' : "False"}
            elif re_password.lower().strip() != password.lower().strip():
                error = """<br/><br/><center>Lei due password non coincidono</center>"""
                string = createcaptcha()
                pageData = {'file' : 'userRegistration',
                            "error": error,
                            "forms":forms,
                            "subdomain": addSlash(subdomain),
                            "province":province ,
                            "regioni" :regioni,
                            'string':hashlib.md5(string).hexdigest(),
                            'sent' : "False"}
            elif User().select(emailEM=email) != []:
                error = """<br/><br/><center>Questo indirizzo email &eacute; gi&agrave;<br />
                Presente nel nostro database</center>"""
                string = createcaptcha()
                pageData = {'file' : 'userRegistration',
                            "error": error,
                            "forms":forms,
                            "subdomain": addSlash(subdomain),
                            "province":province ,
                            "regioni" :regioni,
                            'string':hashlib.md5(string).hexdigest(),
                            'sent' : "False"}

            elif User().select(username=username) != []:
                error = """<br/><br/><center>Questo username &eacute; gi&agrave;<br />
                Presente nel nostro database</center>"""
                string = createcaptcha()
                pageData = {'file' : 'userRegistration',
                            "error": error,
                            "forms":forms,
                            "subdomain": addSlash(subdomain),
                            "province":province ,
                            "regioni" :regioni,
                            'string':hashlib.md5(string).hexdigest(),
                            'sent' : "False"}
            elif (username != "") and (password != "") and (email != "") and (User().select(email=email) == []):
                user = User()
                user.username = username
                user.password = hashlib.md5(username + \
                                        password).hexdigest()
                user.email = email
                user.mailing_list = ml
                user.registration_date = datetime.datetime.now()
                user.id_language = 1
                user.id_role = 2
                user.url = url
                user.persist()
                pg = PersonaGiuridica()
                pg.nome = nome
                pg.cognome = cognome
                pg.id_sede_legale_provincia = provincia
                pg.id_sede_legale_regione = regione
                pg.sede_legale_localita = citta
                pg.id_user = user.id
                pg.persist()
                if SetConf().select(key="self_confirm")[0].value:
                    SendMail(req=req,to=email).sendRegisterCodeToUser(userid=user.id)
                    SendMail(req=req,to="me").sendRegisterUser()
                    pageData = {'file' : 'registerCodeSent'}
                else:
                    SendMail(req=req, to=email).sendRegisterUser()
                    pageData = {'file' : 'registerConfirmed'}
            else:
                error = """<br/><br/><center>Dimenticato qualche dato fondamentale?<br />
                </center>"""
                string = createcaptcha()
                pageData = {'file' : 'userRegistration',
                            "error": error,
                            "forms":forms,
                            "subdomain": addSlash(subdomain),
                            "province":province ,
                            "regioni" :regioni,
                            'string':hashlib.md5(string).hexdigest(),
                            'sent' : "False"}

        else:
            string = createcaptcha()
            error = " CAPTCHA ERRATO ...riprova"
            pageData = {'file' : 'userRegistration',
                "error": error,
                "forms":forms,
                "subdomain": addSlash(subdomain),
                "province":province ,
                "regioni" :regioni,
                'string':hashlib.md5(string).hexdigest(),
                'sent' : "False"}
    else:
        province = Province().select(batchSize=None)
        regioni = Regioni().select(batchSize=None)
        string = createcaptcha()
        pageData = {'file' : 'userRegistration',
                    "subdomain": subdomain,
                    "province":province ,
                    "regioni" :regioni,
                    'string':hashlib.md5(string).hexdigest(),
                    'sent' : "False"}
    return Page(req).render(pageData)

def recoverypassword(req,static=None, subdomain=None):
    """ funzione di recupero password
    TODO: aggiungere il prima possibile il captcha
    """
    #    captcha = req.form.get('captcha')
    #    string = req.form.get('string')

    if req.form.get('username') and req.form.get('emailrecovery'):
        user = User().select(username=req.form.get('username'),
                        email=req.form.get('emailrecovery'))
        if not user:
            error = """<br/><br/><center>Qualche dato utente mancante o inesatto.<br />
                Ricontrolla username o indirizzo email</center>"""
            pageData = {'file' : 'error_common',
                        'error' : error}
            return Page(req).render(pageData)
        else:
            newpasswd = createRandomString()
            pageData = {'file' : 'recoveryConfirmed',
                            "subdomain": subdomain}
            user[0].password = hashlib.md5(req.form.get('username') + \
                                        newpasswd).hexdigest()
            user[0].persist()
            SendMail(req,to=req.form.get('emailrecovery')).sendRecoveryPassword(newpasswd = newpasswd)
    else:
        pageData = {'file' : 'recoveryPassword',
                    "subdomain": subdomain}
    return Page(req).render(pageData)

def screenshot(req,static=None, subdomain=None):
    pageData = {'file' : 'screenshots',
            "subdomain": subdomain}
    return Page(req).render(pageData)


def mioip(req,static=None, subdomain=None):
    if req.form.get('name') \
                and req.form.get('email'):
        SendMail(req=req).sendIP(form=req.form)
        redirectUrl=addSlash(subdomain.template)
        return Page(req).redirect(redirectUrl)

    else:
        pageData = {'file' : 'mioip',
                "subdomain": subdomain}
        return Page(req).render(pageData)


def getnews(req):
    captchamd5=""
    captcha = req.form.get('captcha')
    string = req.form.get('string')
    titolo = req.form.get('Title')
    abstract = req.form.get('Abstract')
    body = req.form.get('Body')
    source_url = req.form.get('source_url')
    source_url_alt_text = req.form.get('source_url_alt_text')
    source_user = req.form.get('source_user')
    #if req.form.get('languageId'):
        #languageId = req.form.get('languageId')
        #if languageId != "None":
            #news.id_language = languageId
        #else:
            #new.id_language = 1
    if captcha:
        captchamd5 = hashlib.md5(captcha).hexdigest()
    if captchamd5 == string:
        if titolo != "" and abstract != "" and body != "":
            news = News(req=req)
            news.title = titolo
            news.body = body
            news.abstract = abstract
            news.permalink = permalinkaTitle(titolo)
            news.source_url = source_url
            news.source_url_alt_text = source_url_alt_text
            news.insert_date = datetime.datetime.now()
            news.active = False
            new.id_language = 1
            news.persist()
            pageData = {'file' : 'getnews',
                    #'string':hashlib.md5(string).hexdigest(),
                    'sent' : "True"}
            return Page(req).render(pageData)
            #redirectUrl='/'
            #return Page(req).redirect(redirectUrl)
    if not captcha:
        string = createcaptcha()
        pageData = {'file' : 'getnews',
                    'string':hashlib.md5(string).hexdigest(),
                    'sent' : "False"}
    return Page(req).render(pageData)


def sviluppo_(req,static=None, subdomain=None):
    """ questa è la pagina di gestione delle informazioni relative
    agli strumenti usati nello sviluppo come il trac ( di cui si prelevano i
    feeds """
    feedTrac = Environment.feedTrac
    if not feedTrac or time.localtime(time.time()).tm_hour > Environment.orario:
        feedTrac = getfeedFromSite(name="trac", items=10)
        Environment.feedTrac = feedTrac
        Environment.orario = time.localtime(time.time()).tm_hour
    else:
        feedTrac = Environment.feedTrac
    pageData = {'file' : 'sviluppo',
            "subdomain": subdomain,
            "feedTrac" :feedTrac}
    return Page(req).render(pageData)

def checkcodeincr(req, code):
    """ Action relativa alla verifica del codiceENCR di
    verifica registrazione
    """
    cr = ConfirmRegistration().select(code=code)
    if cr:
        cr[0].verified = True
        cr[0].persist()
        user = User().getRecord(id=cr[0].id_user)
        user.active= True
        user.id_role = 4 # Utente
        user.last_modified = datetime.datetime.now()
        user.persist()
        SendMail(req=req, to=user.email).sendRegMail()
        pageData = {'file' : 'registerConfirmed'}
        return Page(req).render(pageData)
    else:
        redirectUrl= "/"
        return Page(req).redirect(redirectUrl)

def _sa_to_dict(obj):
    for item in obj.__dict__.items():
        if item[0][0] is '_':
            continue
        if isinstance(item[1], str):
            yield [item[0], item[1].decode()]
        elif isinstance(item[1], datetime.datetime):
            yield [item[0], item[1].__str__()]
        else:
            yield item

def jsonn(obj):
    if isinstance(obj, list):
        return json.dumps(map(dict, map(_sa_to_dict, obj)))
    else:
        return json.dumps(dict(_sa_to_dict(obj)))

def check(req,static=None, subdomain=None):
    print req.form.to_dict()
    sc = SetConf().select(batchSize=None)
    return Response(jsonn(sc))
