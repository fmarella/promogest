#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>
#
from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao.Subdomain import Subdomain
from core.lib.utils import *
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
from core.lib.unipath.path import *

def subDomain(req, subdomain=None, action=None):

    def subdomainList(req, subdomain=None, action=None):
        subss = Subdomain().select(batchSize=None)
        print "SUUUUUUUUUUUUUUUUUUUUUUUUBS2", subss
        pageData = {'file': 'subdomainAction',
                    'subs': subss}
        return Page(req).render(pageData)

    def subdomainAdd(req, subdomain="", action=None):
        """Aggiunge una pagina a contenuto statico"""
        idrr = Session(req).getUserId()
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            subs = Subdomain()
            pageData = {'file': 'subdomainAction',
                        'subs': subs}
            return Page(req).render(pageData)
        elif req.args.get("edit"):
            subs = Subdomain(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file': 'subdomainAction',
                        'subs': subs}
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                        and req.form.get('name'):
            subs = Subdomain()
        elif req.args.get('update')\
                        and req.form.get('name'):
            subs = Subdomain(req=req).getRecord(id =req.args.get("update"))
        if subs:
            subs.name = req.form.get('name').lower()
            subs.description = req.form.get('description')
            subs.template = req.form.get('template')
            subs.persist()
            redirectUrl='/siteAdmin/subdomainList'
            return Page(req).redirect(redirectUrl)

    def subdomainDel(req, subdomain=None, action=None):
        """ Cancella un subdomain
        """
        subdomainId = req.args.get('subdomainId')
        subs = Subdomain(req=req).getRecord(id=subdomainId)
        subs.delete()
        redirectUrl='/siteAdmin/subdomainList'
        return Page(req).redirect(redirectUrl)

    def subdomainActive(req, subdomain=None, action=None):
        """ Funzione che si occupa di gestire lo stato Attivo o disattivo
        """
        subdomainId = req.args.get('id')
        subs = Subdomain(req=req).getRecord(id=subdomainId)
        if subs.active==False:
            subs.active = True
        else:
            subs.active = False
        subs.persist()
        redirectUrl= '/siteAdmin/subdomainList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="SUBDOMAINLIST": # sezione moduli
        return subdomainList(req,subdomain=subdomain, action=action)
    elif action.upper() == "SUBDOMAINDEL":
        return subdomainDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "SUBDOMAINADD":
        return subdomainAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "SUBDOMAINACTIVE":
        return subdomainActive(req,subdomain=subdomain,action=action)
