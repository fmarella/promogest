# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
#

import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.lib.webutils import *
from promogest import Environment
#from promogest.pages import *
from promogest.dao.Setconf import SetConf
from promogest.lib.session import Session
from promogest.lib.page import Page
from promogest.lib.unipath.path import *

def setConf(req, subdomain=None, action=None):

    def setconfList(req, subdomain=None, action=None):
        """ Lista le opzioni nella tabella
        """
        batch = 50
        count = SetConf().count(searchkey=req.form.get('searchkey'))
        args = pagination(req,batch,count)
        args["page_list"] = "siteAdmin/setconfList"
        setconflist = SetConf().select(searchkey=req.form.get('searchkey'),
                                    batchSize=batch,
                                    offset=args["offset"],
                                    orderBy="section")

        pageData = {'file' : 'setconfAction',
                    "args":args,
                    'setconf' : setconflist}
        return Page(req).render(pageData)

    def setconfAdd(req, subdomain=None, action=None):
        """Aggiunge o modifica una setconf """
        print "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", req.args.to_dict()
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            setconf = SetConf(req=req)
            pageData = {'file' : 'setconfAction',
                        'setconf' : setconf}
            return Page(req).render(pageData)
        elif req.args.get("edit"):
            setconf = SetConf(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file' : 'setconfAction',
                        'setconf' : setconf}
            return Page(req).render(pageData)
        elif req.args.get('add')== ""\
                        and req.form.get('section') \
                        and req.form.get('key'):
            setconf = SetConf(req=req)
        elif req.args.get('update')\
                        and req.form.get('section') \
                        and req.form.get('key'):
            setconf = SetConf(req=req).getRecord(id =req.args.get("update"))
        if setconf:
            setconf.section = req.form.get('section')
            setconf.key = req.form.get('key')
            setconf.value = req.form.get('value')
            setconf.description = req.form.get('description')
            setconf.active = setconf.active or False
            setconf.date = datetime.datetime.now()
            setconf.persist()
            redirectUrl='/siteAdmin/setconfList'
            return Page(req).redirect(redirectUrl)

    def setconfDel(req, subdomain=None, action=None):
        """
        Cancella una setconf
        """
        setconfId = req.args.get('setconfId')
        setconf = SetConf(req=req).getRecord(id=setconfId)
        setconf.delete()
        redirectUrl='/siteAdmin/setconfList'
        return Page(req).redirect(redirectUrl)

    def setconfActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della setconf
        Attivo o disattivo
        """
        setconfId = req.args.get('id')
        setconf = SetConf(req=req).getRecord(id=setconfId)
        if setconf.active==False:
            setconf.active = True
        else:
            setconf.active = False
        setconf.persist()
        redirectUrl='/siteAdmin/setconfList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="SETCONFLIST": # sezione moduli
        return setconfList(req,subdomain=subdomain, action=action)
    elif action.upper() == "SETCONFDEL":
        return setconfDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "SETCONFADD":
        return setconfAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "SETCONFACTIVE":
        return setconfActive(req,subdomain=subdomain,action=action)
