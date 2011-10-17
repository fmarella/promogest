#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
#

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao.StaticPages import StaticPages
from core.lib.utils import *
from core import Environment
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
from core.lib.unipath.path import *

def staticPages(req, subdomain=None, action=None):

    def staticPagesList(req, subdomain=None, action=None):
        staticPages = StaticPages(req=req).select(batchSize=None)
        pageData = {'file' : 'staticPagesAction',
                    "subdomain": addSlash(subdomain),
                    'staticPages' : staticPages}
        return Page(req).render(pageData)

    def staticPagesAdd(req, subdomain=None, action=None):
        """Aggiunge una pagina a contenuto statico"""
        staticPages = None
        idrr = Session(req).getUserId()
        userEnvDir= prepareUserEnv(req)
        #fileList = os.listdir(userEnvDir)

        if req.args.get('new') =="":
            staticPages = StaticPages(req=req)
            pageData = {'file' : 'staticPagesAction',
                        'staticPages' : staticPages,
                        "subdomain": addSlash(subdomain)}
            return Page(req).render(pageData)
        elif req.args.get("upload"):
            pass
        elif req.args.get("edit"):
            staticPages = StaticPages(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file' : 'staticPagesAction',
                        'staticPages' : staticPages,
                        "subdomain": addSlash(subdomain)}
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                        and req.form.get('pageTitle') \
                        and req.form.get('pageBody'):
                staticPages = StaticPages(req=req)
        elif req.args.get('update')\
                        and req.form.get('pageTitle') \
                        and req.form.get('pageBody'):
                staticPages = StaticPages(req=req).getRecord(id =req.args.get("update"))
        if staticPages:
            staticPages.title = req.form.get('pageTitle')
            staticPages.body = req.form.get('pageBody')
            #staticPages.abstract = req.form.get('newsAbstract')
            staticPages.abstract = ""
            staticPages.permalink = permalinkaTitle(req.form.get('pageTitle'))
            staticPages.publication_date = datetime.datetime.utcnow()
            if req.form.get('languageId'):
                languageId = req.form.get('languageId')
                if languageId != "None":
                    staticPages.id_language = languageId
                else:
                    staticPages.id_language = 1
            staticPages.id_user = idrr
            staticPages.persist()
        redirectUrl=addSlash(subdomain)+'/siteAdmin/staticPagesList'
        return Page(req).redirect(redirectUrl)

    def staticPagesDel(req, subdomain="", action=None):
        """Cancella una pagina a contentuto statico"""
        pageId = req.args.get('pageId')
        staticPages = StaticPages(req=req).getRecord(id=pageId)
        staticPages.delete()
        redirectUrl='/siteAdmin/staticPagesList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="STATICPAGESLIST": # sezione Pagine
        return staticPagesList(req,subdomain=subdomain, action=action)
    elif action.upper() == "STATICPAGESDEL":
        return staticPagesDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "STATICPAGESADD":
        return staticPagesAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "STATICPAGESACTIVE":
        return staticPagesActive(req,subdomain=subdomain,action=action)
    elif action.upper() == "STATICPAGESEDIT":
        return staticPagesEdit(req,subdomain=subdomain,action=action)
