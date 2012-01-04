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

from sqlalchemy.orm import *
from promogest.dao.Dao import Dao
from promogest.lib.page import Page
from promogest import Environment
from promogest.lib.webutils import *
#from core.dao.StaticPages import StaticPages
from promogest.dao.MenuItem import MenuItem
from promogest.dao.Menu import Menu

def menuItem(req, subdomain=None, action=None):

    def menuItemList(req, subdomain=None, action=None):
        """
        menuItem e' per la pagina relativa a siteAdmin
        """
        menus = MenuItem(req=req).select(batchSize=None, orderBy="id_menu")
        pageData = {'file' : 'menuItemAction',
                    'menus':menus}
        return Page(req).render(pageData)

    def menuItemAdd(req, subdomain=None, action=None):
        """
        Aggiunta voci di menù
        """
        staticPages = StaticPages(req=req).select(batchSize=None)
        if req.args.get('new') =="":
            menuitem = MenuItem()
            menus = Menu().select(batchSize=None)
            pageData = {'file' : 'menuItemAction',
                        "staticPages":staticPages,
                        'menuitem' : menuitem,
                        "menus":menus}
            return Page(req).render(pageData)
        if req.args.get('newmenu') =="":
            m = Menu().select(name=req.form.get("newMenuname"))
            if req.form.get("addmenubutton"):
                m = Menu().select(name=req.form.get("newMenuname"))
                if m:
                    m = m[0]
                else:
                    m = Menu()
                m.name = req.form.get("newMenuname")
                m.desciption = req.form.get("newMenudescrizione")
                m.active = True
                m.persist()
            elif req.form.get("delmenubutton"):
                if m:
                    m[0].delete()
            elif req.form.get("actfalsebutton"):
                if m:
                    m[0].active = False
                    m.persist()
            elif req.form.get("acttruebutton"):
                if m:
                    m[0].active = True
                    m[0].persist()
            redirectUrl='/siteAdmin/menuItemAdd?new'
            return Page(req).redirect(redirectUrl)
        elif req.args.get("edit"):
            menu = MenuItem(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file' : 'menuItemAction',
                        'menu':menu,
                        "staticPages":staticPages}
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                and req.form.get('newItem'):
            menu = MenuItem(req=req)
        elif req.args.get('update')\
                and req.form.get('newItem') :
            menu = MenuItem(req=req).getRecord(id =req.args.get("update"))
        if menu:
            menu.item = req.form.get('newItem')
            menu.active = req.form.get('activeitem') or False
            menu.url = req.form.get('url') or ""
            menu.position = req.form.get('position') or None
            menu.target = req.form.get('target')
            menu.number = req.form.get('number')
            menu.id_menu = req.form.get('menuId')
            menu.id_page = req.form.get('pageId')
            menu.id_padre = req.form.get('fatherpageId') or None
            menu.id_language = req.form.get('languageId') or 1
            menu.persist()

            redirectUrl = '/siteAdmin/menuItemList'
            return Page(req).redirect(redirectUrl)

    def menuItemDel(req, subdomain=None, action=None):
        """
        Cancella una news
        """
        menuId = req.args.get('menuId')
        menu = MenuItem(req=req).getRecord(id=menuId)
        menu.delete()
        redirectUrl='/siteAdmin/menuItemList'
        return Page(req).redirect(redirectUrl)

    def menuItemActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato della news
        Attivo o disattivo
        """
        menuId = req.args.get('id')
        menu = MenuItem(req=req).getRecord(id=menuId)
        if menu.active:
            menu.active = False
        else:
            menu.active = True
        menu.persist()
        redirectUrl='/siteAdmin/menuItemList'
        return Page(req).redirect(redirectUrl)

    if action.upper() =="MENUITEMLIST":
        return menuItemList(req,subdomain=subdomain, action=action)
    elif action.upper() == "MENUITEMDEL":
        return menuItemDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "MENUITEMUPDATE":
        return menuItemUpdate(req,subdomain=subdomain,action=action)
    elif action.upper() == "MENUITEMADD":
        return menuItemAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "MENUITEMACTIVE":
        return menuItemActive(req,subdomain=subdomain,action=action)
    elif action.upper() == "MENUITEMEDIT":
        return menuItemEdit(req,subdomain=subdomain,action=action)
