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
from promogest.dao.CategoriaArticolo import CategoriaArticolo

def anagraficaCategoriaArticolo(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req, action=None):
        denominazione = None
        denominazione_breve = None
        if req.form.to_dict():
            denominazione = req.form.get("denominazione")
            denominazione_breve = req.form.get("denominazione_breve")
        chiavi = {"denominazione" : denominazione,
                        "denominazione_breve" : denominazione_breve}
        daos = CategoriaArticolo(req=req).select(batchSize=None,
                                            denominazione=denominazione,
                                    denominazioneBreve=denominazione_breve)
        pageData = {'file' : "anagraficaSemplice",
                    "dao":"CategoriaArticolo",
                    "_dao_":"categoria_articolo",
                    "name": "Categorie Articolo",
                    "tree":"treeCategoriaArticolo",
                    "fkey":"fk_categoriaarticolo",
                    "action":action,
                    "chiavi":chiavi,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __add__(req, action=None):
        id = req.form.get("id")
        denominazione = req.form.get("denominazione")
        denominazione_breve = req.form.get("denominazione_breve")
        if action =="add":
            dao = CategoriaArticolo()
        else:
            dao = CategoriaArticolo().getRecord(id=id)
        dao.denominazione = denominazione
        dao.denominazione_breve = denominazione_breve
        if denominazione:
            dao.persist()
        redirectUrl='/parametri/categoria_articolo/list'
        return Page(req).redirect(redirectUrl)

    def __del__(req, action=None):
        id = req.form.get("idr")
        dao = CategoriaArticolo().getRecord(id=id)
        if dao:
            dao.delete()
        daos = CategoriaArticolo(req=req).select(batchSize=None)
        pageData = {'file' : "/tree/treeCategoriaArticolo",
                    "action":action,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __edit__(req, action=None):
        id = req.form.get("idr")
        dao = CategoriaArticolo().getRecord(id=id)
        pageData = {'file' : "/addedit/ae_categoriaarticolo",
                    "action":action,
            "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        pageData = {'file' : "/addedit/ae_categoriaarticolo",
                    "_dao_":"categoria_articolo",
                    "name": "Categoria Articolo",
                    "tree":"treeCategoriaArticolo",
                    "fkey":"fk_categoriaarticolo",
                    "action":action}
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
