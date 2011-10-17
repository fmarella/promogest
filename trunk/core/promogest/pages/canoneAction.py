#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
#

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from core.lib.utils import *
from core import Environment
from core.pages import *
from core.lib.session import Session
from core.lib.page import Page
#from core.dao.Canone import Canone
from core.dao.User import User

def canone(req,subdomain=None, action=None):

    def canoneDetail(req):
        canoneId = req.args.get('id')
        canone = Canone(req=req).getRecord(id=canoneId)
        if not canone:
            pageData = {'file' : 'not_found'}
            return Page(req).render(pageData)
        pageData = {'file' : 'canone_detail',
                    'canone' : canone,
                    'canoneId':canoneId}
        return Page(req).render(pageData)

    def canoneList(req, subdomain=None, action=None):
        batch = 50
        count = Canone().count(searchkey=req.form.get('searchkey'))
        args = pagination(req,batch,count)
        args["page_list"] = "siteAdmin/canoneList"
        canonelist = Canone().select(searchkey=req.form.get('searchkey'),
                                    batchSize=batch,
                                    offset=args["offset"])

        pageData = {'file' : 'canoneAction',
                    "args":args,
                    'canone' : canonelist}
        return Page(req).render(pageData)

    def canoneAdd(req, subdomain=None, action=None):
        """Aggiunge una pagina a contenuto statico"""
        cadenza = Environment.cadenza
        clienti = User().select(idRole=3, batchSize = None)
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            canone = Canone(req=req)

            pageData = {'file' : 'canoneAction',
                        "cadenza": cadenza,
                        "clienti": clienti,
                        'canone' : canone}
            return Page(req).render(pageData)
        elif req.args.get("edit"):
            canone = Canone(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file' : 'canoneAction',
                        "cadenza": cadenza,
                        "clienti": clienti,
                        'canone' : canone}
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                        and req.form.get('denomination'):
            canone = Canone(req=req)
        elif req.args.get('update')\
                        and req.form.get('denomination'):
            canone = Canone(req=req).getRecord(id =req.args.get("update"))
        if canone:
            canone.denomination = req.form.get('denomination')
            if req.form.get('start_date'):
                canone.start_date= datetime.date(int(req.form.get('start_date').split("-")[2]),
                            int(req.form.get('start_date').split("-")[1]),
                            int(req.form.get('start_date').split("-")[0]))
            if req.form.get('stop_date'):
                canone.stop_date= datetime.date(int(req.form.get('stop_date').split("-")[2]),
                            int(req.form.get('stop_date').split("-")[1]),
                            int(req.form.get('stop_date').split("-")[0]))
            canone.valore = req.form.get('valore')
            canone.id_user = req.form.get('clienteId')
            canone.cadenza = req.form.get('cadenza')
            canone.active = False
            canone.persist()
            redirectUrl='/siteAdmin/canoneList'
            return Page(req).redirect(redirectUrl)

    def canoneDel(req, subdomain=None, action=None):
        """
        Cancella un canone
        """
        canoneId = req.args.get('canoneId')
        canone = Canone(req=req).getRecord(id=canoneId)
        canone.delete()
        redirectUrl='/siteAdmin/canoneList'
        return Page(req).redirect(redirectUrl)

    def canoneActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato dei canoni
        Attivo o disattivo
        """
        canoneId = req.args.get('id')
        canone = Canone(req=req).getRecord(id=canoneId)
        if canone.active==False:
            canone.active = True
        else:
            canone.active = False
        canone.persist()
        redirectUrl='/siteAdmin/canoneList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="CANONELIST": # sezione News
        return canoneList(req,subdomain=subdomain, action=action)
    elif action.upper() == "CANONEDEL":
        return canoneDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "CANONEEDIT":
        return canoneEdit(req,subdomain=subdomain,action=action)
    elif action.upper() == "CANONEADD":
        return canoneAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "CANONEACTIVE":
        return canoneActive(req,subdomain=subdomain,action=action)
