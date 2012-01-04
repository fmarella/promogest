#-*- coding: utf-8 -*-
#
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

import hashlib
import datetime

from sqlalchemy.orm import *
from promogest.dao.User import User
from promogest.dao.Access import Access
from promogest.lib.webutils import *

from promogest.lib.session import Session
from promogest.lib.page import Page


def prelogin(req=None, SUB=""):
    pageData = {'file': 'index',
                'subdomain': addSlash(SUB)}
    return Page(req).render(pageData)


def login(req=None, SUB = ""):
    """
    Gestione procedura di login
    """
    username = req.form.getlist('username')
    passwordd = req.form.getlist('password')
    act = findAct(req)
    company = req.form.get('company')
    workingYear = req.form.get('year')
    Environment.workingYear = int(workingYear)
    Environment.azienda = company
    Environment.meta.clear()
#    Environment.meta.reflect(schema=company )
    Environment.params["metadata"].clear()
    Environment.params["metadata"].reflect(schema="promogest2" )
    Environment.params["metadata"].reflect(schema=company )
#    from promogest import Environment
    if not username or not req.cookies:
        return Page(req).redirect(req.host_url)
        #return index()
    rows = User().select(username=str(username[0]),
                    password=hashlib.md5(username[0]+passwordd[0]).hexdigest())
    if len(rows) == 1:
        if rows[0].active == 1:
            id_user = rows[0].id
            Session(req).start(id_user)
            datelogin = datetime.datetime.today()
            access = Access(req=req)
            access.id_user = id_user
            access.login = datelogin
            access.persist()
            host_url= "/main"
            return Page(req).redirect(host_url)
    else:
        error = """<br/><br/><center><h2>User e/o password errati.<br/>
                    L' utente non e' presente in archivio.<h2></center>
                """
        pageData = {'file': 'error',
                    'error': error}
        return Page(req).render(pageData)


def logout(req, SUB =""):
    """
    Gestione procedura di logout
    """
    Session(req).destroy()
    host_url= req.host_url
    return Page(req).redirect(host_url)
