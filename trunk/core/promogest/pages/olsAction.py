#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni  <francesco@promotux.it>
#
import os
import datetime
import Image
from sqlalchemy import *
from sqlalchemy.orm import *
from core.dao.OlsLine import OlsLine
from core.lib.utils import *
from core import Environment
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
from core.lib.unipath.path import *


def ols(req, subdomain=None, action =None):

    def getolss(req, static=None, subdomain=""):
        ols =  Environment.params["session"].query(OlsLine).filter_by(active=True).order_by(func.random()).all()[0]
        if ols:
            ols.clicks =int(ols.clicks or 0)+1
            ols.persist()
        else:
            ols=OlsLine()
        pageData = {'file' : 'getols',
                    "subdomain": addSlash(subdomain),
                    "ols": ols}
        return Page(req).render(pageData)

    def spot_attivi(req, static=None, subdomain=""):
        olss = OlsLine().select(batchSize=None, active=True)
        pageData = {'file' : 'spot_attivi',
                    "subdomain": addSlash(subdomain),
                    "olss" :olss}
        return Page(req).render(pageData)

    def olsList(req, subdomain=None, action=None):
        item = 0
        searchword = str(req.form.get('search'))
        defaultOffset = 0
        defaultOffsetIndex = 0
        olss = OlsLine(req=req).select(batchSize=None)
        pageData = {'file' : 'olsAction',
                    "subdomain": addSlash(subdomain),
                    'item': item,
                    'pag' : defaultOffsetIndex,
                    'olss' : olss}
        return Page(req).render(pageData)

    def olsAdd(req, subdomain="", action=None):
        """Aggiunge una pagina a contenuto statico"""
        idrr = Session(req).getUserId()
        userEnvDir = prepareUserEnv(req)
        olss = OlsLine().select(batchSize=None)
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            ols = OlsLine(req=req)
            pageData = {'file' : 'olsAction',
                        "subdomain": addSlash(subdomain),
                        'ols' : ols,}
            return Page(req).render(pageData)
        elif req.args.get("edit"):
            ols = OlsLine(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file' : 'olsAction',
                        "subdomain": addSlash(subdomain),
                        'ols' : ols,}
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                        and req.form.get('olsSpot'):
            ols = OlsLine(req=req)
        elif req.args.get('update')\
                        and req.form.get('olsSpot'):
            ols = OlsLine(req=req).getRecord(id =req.args.get("update"))
        if ols:
            ols.spot = req.form.get('olsSpot')
            ols.codice = req.form.get('olsCodice')
            ols.ordine = req.form.get('olsOrdine')
            dr = datetime.date(int(req.form.get('olsDataExpire').split("-")[2]),
                                int(req.form.get('olsDataExpire').split("-")[1]),
                                int(req.form.get('olsDataExpire').split("-")[0]))
            de = datetime.date(int(req.form.get('olsDataExpire').split("-")[2]),
                                int(req.form.get('olsDataExpire').split("-")[1]),
                                int(req.form.get('olsDataExpire').split("-")[0]))
            ols.data_registrazione = dr
            ols.data_expire = de
            ols.id_user = idrr
            ols.persist()
            redirectUrl=addSlash(subdomain)+'/siteAdmin/olsList'
            return Page(req).redirect(redirectUrl)

    def olsDel(req, subdomain=None, action=None):
        """
        Cancella una news
        """
        olsId = req.args.get('olsId')
        ols = OlsLine(req=req).getRecord(id=olsId)
        ols.delete()
        redirectUrl=addSlash(subdomain)+'/siteAdmin/olsList'
        return Page(req).redirect(redirectUrl)

    def olsActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        olsId = req.args.get('id')
        ols = OlsLine(req=req).getRecord(id=olsId)
        if ols.active==False:
            ols.active = True
        else:
            ols.active = False
        ols.persist()
        redirectUrl=addSlash(subdomain)+'/siteAdmin/olsList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="OLSLIST": # sezione ols
        return olsList(req,subdomain=subdomain, action=action)
    elif action.upper() == "OLSDEL":
        return olsDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "OLSADD":
        return olsAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "OLSACTIVE":
        return olsActive(req,subdomain=subdomain,action=action)
