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

from werkzeug.exceptions import NotFound
from promogest.lib.webutils import *
from promogest.pages.login import login, logout, prelogin
from promogest.lib.page import Page
#from core.pages.home import *
from promogest.pages.mainpage import mainpage
#from core.lib.utils import *
from promogest.pages.siteAdmin import siteAdminn # importa la parte di gestione ...
from promogest.pages.userAction import user
from promogest.pages.roleAction import role
#from promogest.pages.menuItemAction import menuItem
from promogest.pages.companyAction import company
from promogest.pages.preview import previews
from promogest.pages.daoadd import daoadd
from promogest.pages.anagrafiche import anagrafiche
from promogest.pages.magazzini import magazzini
from promogest.pages.parametri import parametri
from promogest.pages.promemoria import promemoria
from promogest.pages.anagraficaArticolo import anagraficaArticolo
from promogest.pages.anagraficaCliente import anagraficaCliente
from promogest.pages.anagraficaFornitore import anagraficaFornitore
from promogest.pages.anagraficaVettore import anagraficaVettore
from promogest.pages.anagraficaAgente import anagraficaAgente
from promogest.pages.anagraficaFornitura import anagraficaFornitura
from promogest.pages.anagraficaCategoriaArticolo import anagraficaCategoriaArticolo
from promogest.pages.anagraficaFamigliaArticolo import anagraficaFamigliaArticolo
from promogest.pages.anagraficaCategoriaCliente import anagraficaCategoriaCliente
from promogest.pages.anagraficaCategoriaFornitore import anagraficaCategoriaFornitore
from promogest.pages.anagraficaCategoriaContatto import anagraficaCategoriaContatto
from promogest.pages.anagraficaImballaggio import anagraficaImballaggio
from promogest.pages.anagraficaMultiplo import anagraficaMultiplo
from promogest.pages.anagraficaPagamento import anagraficaPagamento
from promogest.pages.anagraficaBanca import anagraficaBanca
from promogest.pages.anagraficaAliquotaIva import anagraficaAliquotaIva
from promogest.pages.configuration import *
from promogest.pages.jsonSearch import jsonsearch
from promogest.pages.printDao import printDao
#from core.pages.siteAdmin.subdomainAction import subDomain
from promogest.pages.setconfAction import setConf

""" PARTE RELATIVA AL SITEADMIN """

@expose("/")
def siteAdmi(req, subdomain=""):
    #if hasAction(req,action=[1,2,3,4,5]): # adminrole
    #if Environment.SUB:
        #host_url= "/"+Environment.SUB
        #return Page(req).redirect(host_url)

    if 5==5: # adminrole
        return siteAdminn(req, SUB=Environment.SUB)
    elif hasAction(req,action=[1,2]): #utente
        host_url= "/"+subdomain
        return Page(req).redirect(host_url)
    else:
        print " L'USER NON HA ABBASTANZA DIRITTI DI ACCESSO"
#        Session(req).destroy()
        pageData = {'file' : 'not_found'}
        return Page(req).render(pageData)


#@expose("/siteAdmin/<action>")
#def siteAdminAction(req, subdomain=None, action=None):
#    if hasAction(req,action=[1,2,3,4,5]):
#        if action.upper() =="THEME_SETUP":
#            return theme_setup(req,subdomain=subdomain, action=action)
#        elif action.upper() =="SETUP":
#            return mainSetup(req,subdomain=subdomain, action=action)

#        if "USER" in action.upper():
#            return user(req,subdomain=subdomain, action=action)
#        if "MENUITEM" in action.upper():
#            return menuItem(req,subdomain=subdomain, action=action)
#        if "SETCONF" in action.upper():
#            return setConf(req,subdomain=subdomain, action=action)
#        if "SUBDOMAIN" in action.upper():
#            return subDomain(req,subdomain=subdomain, action=action)
#        if "ROLE" in action.upper():
#            return role(req,subdomain=subdomain, action=action)
#        if "STATICPAGES" in action.upper():
#            return staticPages(req,subdomain=subdomain, action=action)
#        if "COMPANY" in action.upper():
#            return company(req,subdomain=subdomain, action=action)
#        if "FEED" in action.upper():
#            return feed(req,subdomain=subdomain, action=action)
#    else:
#        pageData = {'file' : 'not_found'}
#        return Page(req).render(pageData)

def elencoPagineStatiche(req, static=None, subdomain=None):
    if static == "sla2pdf":
        return sla2pdff(req, static=static, subdomain=subdomain)
    elif static == "company_detail":
        return companyDetail(req)
    elif static == "company_list":
        return companylistCategorized(req)
    elif static == "contacts":
        return contacts(req, static=static, subdomain=subdomain)
    elif static == "userDetail":
        return userdetail(req, static=static, subdomain=subdomain)
    elif static =="main":
        return mainpage(req, subdomain=subdomain)
    elif static =="login":
        return login(req, SUB=subdomain)
    elif static =="prelogin":
        return prelogin(req, SUB=subdomain)
    elif static =="logout":
        return logout(req, SUB=subdomain)
    elif static =="anagrafiche":
        return anagrafiche(req)
    elif static =="magazzini":
        return magazzini(req)
    elif static =="parametri":
        return parametri(req)
    elif static =="promemoria":
        return promemoria(req)
    #elif static.upper() == Environment.SUB.upper():
        #return siteAdminn(req, SUB=Environment.SUB)
#    elif action.upper() =="THEME_SETUP":
#        return theme_setup(req,subdomain=subdomain, action=action)
#    elif action.upper() =="SETUP":
#        return mainSetup(req,subdomain=subdomain, action=action)

#    if "USER" in action.upper():
#        return user(req,subdomain=subdomain, action=action)
#    if "MENUITEM" in action.upper():
#        return menuItem(req,subdomain=subdomain, action=action)
#    if "SETCONF" in action.upper():
#        return setConf(req,subdomain=subdomain, action=action)
#    if "SUBDOMAIN" in action.upper():
#        return subDomain(req,subdomain=subdomain, action=action)
#    if "ROLE" in action.upper():
#        return role(req,subdomain=subdomain, action=action)
#    if "STATICPAGES" in action.upper():
#        return staticPages(req,subdomain=subdomain, action=action)
#    if "COMPANY" in action.upper():
#        return company(req,subdomain=subdomain, action=action)
#    if "FEED" in action.upper():
#        return feed(req,subdomain=subdomain, action=action)
    else:
        pageData = {'file' : 'not_found'}
        return Page(req).render(pageData)


def __sub__(req, sub=None, action=None):
    if sub == "categoria_articolo":
        return anagraficaCategoriaArticolo(req, action=action)
    elif sub == "famiglia_articolo":
        return anagraficaFamigliaArticolo(req, action=action)
    elif sub == "categoria_cliente":
        return anagraficaCategoriaCliente(req, action=action)
    elif sub == "categoria_fornitore":
        return anagraficaCategoriaFornitore(req, action=action)
    elif sub == "categoria_contatto":
        return anagraficaCategoriaContatto(req, action=action)
    elif sub == "imballaggio":
        return anagraficaImballaggio(req, action=action)
    elif sub == "multiplo":
        return anagraficaMultiplo(req, action=action)
    elif sub == "pagamento":
        return anagraficaPagamento(req, action=action)
    elif sub == "banca":
        return anagraficaBanca(req, action=action)
    elif sub == "aliquota_iva":
        return anagraficaAliquotaIva(req, action=action)
    elif sub == "articolo":
        return anagraficaArticolo(req, action=action)
    elif sub == "cliente":
        return anagraficaCliente(req, action=action)
    elif sub == "fornitura":
        return anagraficaFornitura(req, action=action)
    elif sub == "fornitore":
        return anagraficaFornitore(req, action=action)
    elif sub == "vettore":
        return anagraficaVettore(req, action=action)
    elif sub == "agente":
        return anagraficaAgente(req, action=action)


def __autocomplete__(req, action=None, what_json_search=None):
    return jsonsearch(req, action = action, what_json_search=what_json_search)

def __printt__(req, dao=None, action=None):
    return printDao(req, dao=dao)

@expose('/preview')
def __preview(req):
    return previews(req)

@expose('/daoadd')
def __daoadd(req):
    dao= req.form.get("dao")
    action = "new"
    return __sub__(req, sub=dao, action=action)

@expose('/delete')
def __delete(req):
    dao= req.form.get("dao")
    action = "delete"
    return __sub__(req, sub=dao, action=action)

@expose('/printt')
def __printt(req):
    dao= req.args.get("dao")
    action = "printt"
    return __printt__(req, dao=dao, action=action)


@expose('/autocomplete/<what_json_search>')
def __autocomplete(req, what_json_search=None):
    action = "autocomplete"
    return __autocomplete__(req, action=action, what_json_search=what_json_search)

@expose('/edit')
def __edit(req):
    dao= req.form.get("dao")
    action = "edit"
    return __sub__(req, sub=dao, action=action)


#Qui gestiamo le pagine statiche di primo livello
@expose("/<first>")
def statics(req, first=None):
    return elencoPagineStatiche(req, static=first)

#qui gestiamo le operazioni di secondo livello sulle anagrafiche
@expose('/anagrafiche/<second>/<terzo>')
def ___anagrafiche_sub(req, second=None, terzo=None):
    return __sub__(req, sub=second, action=terzo)

@expose('/parametri/<second>/<terzo>')
def ___parametri_sub(req, second=None, terzo=None):
    return __sub__(req, sub=second, action=terzo)
