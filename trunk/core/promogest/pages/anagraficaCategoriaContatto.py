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


from promogest.lib.page import Page
from promogest.modules.Contatti.dao.CategoriaContatto import CategoriaContatto

def anagraficaCategoriaContatto(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req, action=None):
        denominazione =None
        if req.form.to_dict():
            denominazione = req.form.get("denominazione")
        chiavi = {"denominazione" : denominazione}
        daos = CategoriaContatto(req=req).select(batchSize=None, denominazione=denominazione)
        pageData = {'file' : "anagraficaSemplice",
                    "dao":"CategoriaContatto",
                    "_dao_":"categoria_contatto",
                    "name": "Categorie Contatto",
                    "tree":"treeCategoriaContatto",
                    "fkey":"fk_categoriacontatto",
                    "action":action,
                    "chiavi":chiavi,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __add__(req, action=None):
        id = req.form.get("id")
        denominazione = req.form.get("denominazione")
        if action == "add":
            dao = CategoriaContatto()
        else:
            dao = CategoriaContatto().getRecord(id=id)
        dao.denominazione = denominazione
        if denominazione:
            dao.persist()
        redirectUrl='/parametri/categoria_contatto/list'
        return Page(req).redirect(redirectUrl)

    def __del__(req, action=None):
        id = req.form.get("idr")
        dao = CategoriaContatto().getRecord(id=id)
        if dao:
            dao.delete()
        daos = CategoriaContatto(req=req).select(batchSize=None)
        pageData = {'file' : "/tree/treeCategoriaContatto",
                    "action":action,
                    "daos":daos}
        return Page(req).render(pageData)

    def __edit__(req, action=None):
        id = req.form.get("idr")
        dao = CategoriaContatto().getRecord(id=id)
        pageData = {'file' : "/addedit/ae_categoriacontatto",
                    "action":action,
            "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        pageData = {'file' : "/addedit/ae_categoriacontatto",
                    "_dao_":"categoria_contatto",
                    "name": "Categoria Contatto",
                    "tree":"treeCategoriaContatto",
                    "action":action,
        }
        return Page(req).render(pageData)

    if action=="list":
        return _list_(req, action=action)
    elif action=="add" or action=="fromedit":
        return __add__(req, action=action)
    elif action=="delete":
        return __del__(req, action=action)
    elif action=="edit":
        return __edit__(req, action=action)
    elif action=="new":
        return __new__(req, action=action)
