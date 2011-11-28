# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

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
import gettext
import datetime,time
from sqlalchemy import *
from sqlalchemy.orm import *
import locale
from jinja2 import Template
import simplejson as json

from promogest import Environment
from promogest.lib import webutils
from promogest.dao.User import User
from promogest.modules.Multilingua.dao.Language import Language
from promogest.dao.Setconf import SetConf
from promogest.lib.webutils import *
from promogest.ui import utils
from promogest.lib.session import Session

COOKIENAME = SetConf().select(key="cookie_name")[0].value

class Page(object):

    def __init__(self, req):
        self.req = req
        self.path = req.environ['PATH_INFO'].split('/')
        self.host = req.environ['HTTP_HOST']
        self.auth = Session(req).control()
        self.nameuser = getUsernameFromId(req)
        self.us= None
        self.vetrina = None
        #self.language= Language().select()
        jinja_env.globals['req'] = req
        jinja_env.globals['environment'] = Environment
        jinja_env.globals['utils'] = utils
        self.role = getRoleFromId(req)
        #self.role = "Admin"


    def template_loaded(self,template, req=None):
        _= self.setlang()
        template.filters.insert(0, Translator(_))

    def getLang(self, req):
        """
        Funzione che comanda la lingua
        """
        #if not self.auth:
            #self.auth = Session(req).control()
        #if not self.nameuser:
            #self.nameuser = getUsernameFromId(req)
        #if self.auth and self.nameuser:
            #if not self.us:
                #self.us = User(req=self.req).select(username=str(self.nameuser),batchSize=None)[0]
            #lang = str(self.us.lingua_breve)
            #return lang
        #else:
            #try:
                #lang = req.cookies['ngsresinelangflagged']
            #except:
                #if "HTTP_ACCEPT_LANGUAGE" in req.environ:
                    #lang=self.req.environ['HTTP_ACCEPT_LANGUAGE'][0:2]
                #else:
        lang = "it"
        return lang

    def itemStaticMenu(self):
        #self.itemsStaticMenu = []
        lingua= self.getLang(self.req)
        l = []
        for a in self.language:
            if a.denominazione_breve==lingua or a.denominazione_breve =="all":
                l.append(a.id)
            else:
                pass
        itemsStaticMenu = StaticMenu(req=self.req).select(id_language=l,batchSize=None)
        return itemsStaticMenu


    def setlang(self):
        languages = self.getLang(self.req)
        try:
            lang = gettext.translation('messages', Environment.configPath+'lang',languages=[languages] )
        except:
            lang = gettext.translation('messages', Environment.configPath+'lang',languages=["it"] )
        _ = lang.ugettext
        lang.install()
        return _

    def tpl(self, req):
        loader = TemplateLoader([Environment.templates_dir],callback=self.template_loaded)
        self.tmpl = loader.load(includeFile(self.req,'index') +'.html')

    def createCookie(self, resp, cookiename, cookieval):
        resp.set_cookie(cookiename, value=cookieval, path='/', domain=None)
        return resp

    def deleteCookie(self, resp, cookiename):
        resp.delete_cookie(cookiename, path='/', domain=None)
        return resp

    def bodyTags(self, pageData):
        if pageData["bodyTags"]:
            for dao in pageData["bodyTags"]:
                for attr in dir(pageData[dao]):
                    if attr[0] !="_" and type(getattr(pageData[dao],attr)) == type(u"ciao"):
                        template = Template(getattr(pageData[dao],attr))
                        boh = template.render(pageData=pageData)
                        try:
                            setattr(pageData[dao], attr, boh)
                        except:
                            pass
        return pageData


    def render(self, pageData, cookiename=None, cookieval=None, cookiedel=None, langflagged = None):
        #self.itemsStaticMenu = self.itemStaticMenu()
        if "subdomain" not in pageData:
            pageData["subdomain"] = Environment.SUB.lower()
        if "bodyTags" in pageData.keys():
            pageData = self.bodyTags(pageData)
        try:
            pageData["project_name"] = SetConf().select(key="name")[0].value
            pageData["head_title"] = SetConf().select(key="head_title")[0].value
        except:
            print ""
        if "args" not in pageData:
            pageData["args"] = self.req.args.to_dict()
        if "forms" not in pageData:
            pageData["forms"] = self.req.form.to_dict()
            pageData["formsjs"] = json.dumps(self.req.form.to_dict())
        pageData['auth'] = self.auth
        pageData["USER"] = getUserFromId(self.req)
        pageData['file'] = includeFile(pageData['file'])
        #pageData['itemsStaticMenu'] = self.itemsStaticMenu
        pageData['nameuser'] = self.nameuser
        pageData['now'] = datetime.datetime.now()
        pageData['role'] = self.role
        #pageData['language'] = self.language
        if "dao" in pageData:
            resp = render_template(pageData["file"],pageData=pageData,dao = pageData["dao"])
        else:
            resp = render_template(pageData["file"],pageData=pageData)

        idcookiename = COOKIENAME
        idcookienamelang = COOKIENAME+'langflagged'
        if idcookienamelang not in self.req.cookies:
            if langflagged:
                idcookievallang = langflagged
            else:
                idcookievallang = self.getLang(self.req)
            resp = self.createCookie(resp, idcookienamelang, idcookievallang)
        if idcookiename not in self.req.cookies:
            idcookieval = hashlib.sha1(repr(time.time())).hexdigest()
            resp = self.createCookie(resp, idcookiename, idcookieval)
        if cookiename and cookieval:
            resp = self.createCookie(resp, cookiename, cookieval)
        if cookiedel:
            resp = self.deleteCookie(resp, cookiedel)
        return resp

    def redirect(self, url=None, cookiename=None, cookieval=None,
                    cookienamelang=None, cookievallang=None, cookiedel=None):
#        self.itemsStaticMenu = self.itemStaticMenu()
        subdomain = '/' + self.path[1] + '/'
        if not url:
            if not self.path[1]:
                resp = RedirectResponse("/")
            else:
                resp = RedirectResponse(subdomain)
        else:
            #if not self.path[1]:
                #print "UUUUUUUUUUUUUUUUUUUUUUUURL"
            resp = RedirectResponse(url)
            #else:
                #resp = RedirectResponse(subdomain+url)
        #idcookiename = self.req.environ["SERVER_NAME"] + 'id'
        idcookiename =  Environment.COOKIENAME
        if idcookiename not in self.req.cookies:
            idcookieval = hashlib.sha1(repr(time.time())).hexdigest()
            resp = self.createCookie(resp, idcookiename, idcookieval)
        if cookiename and cookieval:
            resp = self.createCookie(resp, cookiename, cookieval)
        if cookienamelang and cookievallang:
            resp = self.createCookie(resp, cookienamelang, cookievallang)
        if cookiedel:
            resp = self.deleteCookie(resp, cookiedel)

        return resp

    def pluginSearch(self):
        pass
