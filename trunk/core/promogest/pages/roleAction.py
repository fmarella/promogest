#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>



from sqlalchemy import *
from sqlalchemy.orm import *
#from core.pages import *
from promogest.modules.RuoliAzioni.dao.Role import Role
from promogest.modules.RuoliAzioni.dao.RoleAction import RoleAction
from promogest import Environment
from promogest.lib.page import Page
from promogest.lib.webutils import *

from promogest.lib.session import Session
from promogest.lib.page import Page


def role(req, subdomain=None, action=None):

    def roleList(req, subdomain=None, action=None):
        """ Funzione di lista e visualizzazione dei ruoli
        """
        roles = Role(req=req).select(batchSize=None)
        pageData = {'file' : 'roleAction',
                    "subdomain": addSlash(subdomain),
                    'action':"list",
                    'roles' : roles}
        return Page(req).render(pageData)

    def roleAdd(req, subdomain=None, action=None):
        """
        Funzione di aggiunta ruoli
        """
        role = req.form.getlist('addrole')
        if role != []:
            role = Role(req=req)
            role.name = str(req.form.get('addrole'))
            role.descrizione = str(req.form.get('adddescrizione'))
            role.active = True
            role.persist()
            role = ''
            redirectUrl='/siteAdmin/roleList'
            return Page(req).redirect(redirectUrl)
        else:
            pageData = {'file' : 'roleAction'}
            return Page(req).render(pageData)

    def roleActive(req, subdomain=None, action=None):
        """
        Funzione di gestione ruoli attivi e disattivi
        """

        roleId = req.args.get('id')
        role = Role(req=req).getRecord(id=roleId)
        if role.name in ["Admin"]:
            role.active = True
        elif role.active:
            role.active = False
        else:
            role.active = True
        role.persist()
        redirectUrl='/siteAdmin/roleList'
        return Page(req).redirect(redirectUrl)

    def roleDel(req, subdomain=None, action=None):
        """
        Funzione di cancellazione dei ruoli
        """
        roleId = req.args.get('id')
        if roleId:
            role = Role(req=req).getRecord(id=roleId)
            if role.name not in ["Admin", "Cliente", "ClientePRO", "Guest"]:
                role.delete()
                #role.flush(self.req)
            else:
                error ="<br/><br/><center>Il ruolo "+role.name+" non puo' essere cancellato.</center>"
                pageData = {'file' : 'error',
                        "subdomain": addSlash(subdomain),
                            'error' : error}
                return Page(req).render(pageData)
        redirectUrl='/siteAdmin/roleList'
        return Page(req).redirect(redirectUrl)

    def roleMod(req, subdomain=None, action=None):
        """
        funzione di modifica dei ruoli a cui si aggiunge
        anche il passaggio delle azioni consentite
        """
        roleId = req.args.get('id')
        if roleId:
            roleActionsId = RoleAction(arg=req).select(id_role=roleId)
            actions = Action(arg=req).select()
            roleactionsID = []
            #listino = Dao(Listino,req=self.req).select(visible=True)
            for i in roleActionsId:
                roleactionsID.append(i.id_action)
            editRole = Role(req=req).getRecord(id=roleId)
            pageData = {'file' : 'roleAction',
                        "subdomain": addSlash(subdomain),
                        'actions' : actions,
                        #'listino' : [],
                        'editRole' : editRole,
                        'roleactionsID' : roleactionsID}
            return Page(req).render(pageData)
        else:
            return Page(req).redirect('Error')

    def roleUpdate(req, subdomain=None, action=None):
        """
        Funzione di gestione dati dal form di modifica dei ruoli
        """
        roleId = req.form.get('id')
        nome = str(req.form.get('nome'))
        note = str(req.form.get('note'))
        #rolelistino = int(req.form.get('roleListino'))
        role = Role(req=req).getRecord(id=roleId)
        role.name = nome
        role.descrizione = note
        role.id_listino = 1
        role.persist()
        redirectUrl = '/siteAdmin/roleList'
        return Page(req).redirect(redirectUrl)


    def roleActionActive(req, subdomain=None, action=None):
        """
        Funzione di controllo e gestione delle azioni per singolo ruolo
        """
        roleAction = RoleAction(arg=req)
        IdAction = req.args.get('id')
        IdRole = req.args.get('roleId')
        flag = req.args.get('flag')
        if IdRole!='1': # andrax : non è bene che si possano disattivare azioni ad admin
            if flag=='1':
                roleAction.id_role = IdRole
                roleAction.id_action = IdAction
                roleAction.persist()
            else:
                delroleAction =  RoleAction(arg=req).select(id_role=IdRole,id_action=IdAction)[0]
                #if delroleAction.id_role == 1:  <------ controllareeeeeeeeeeeeeee
                delroleAction.delete()
        redirectUrl = '/siteAdmin/roleMod?id='+IdRole
        return Page(req).redirect(redirectUrl)

    if action.upper() =="ROLELIST":
        return roleList(req,subdomain=subdomain, action=action)
    elif action.upper() == "ROLEMOD":
        return roleMod(req,subdomain=subdomain,action=action)
    elif action.upper() == "ROLEDEL":
        return roleDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "ROLEUPDATE":
        return roleUpdate(req,subdomain=subdomain,action=action)
    elif action.upper() == "ROLEADD":
        return roleAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "ROLEACTIVE":
        return roleActive(req,subdomain=subdomain,action=action)
    elif action.upper() == "ROLEACTIONACTIVE":
        return roleActionActive(req,subdomain=subdomain,action=action)
