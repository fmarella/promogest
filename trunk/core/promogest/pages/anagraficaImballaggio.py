#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from promogest.lib.page import Page
from promogest.dao.Imballaggio import Imballaggio

def anagraficaImballaggio(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req, action=None):
        denominazione = None
        if req.form.to_dict():
            denominazione = req.form.get("denominazione")
        daos = Imballaggio(req=req).select(batchSize=None, denominazione=denominazione)
        chiavi = {"denominazione" : denominazione}
        pageData = {'file' : "anagraficaSemplice",
                    "dao":"Imballaggio",
                    "_dao_":"imballaggio",
                    "name": "Imballaggio",
                    "tree":"treeImballaggio",
                    "fkey":"fk_imballaggio",
                    "action":action,
                    "chiavi":chiavi,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __add__(req, action=None):
        id = req.form.get("id")
        denominazione = req.form.get("denominazione")
        if action == "add":
            dao = Imballaggio()
        else:
            dao = Imballaggio().getRecord(id=id)
        dao.denominazione = denominazione
        if denominazione:
            dao.persist()
        redirectUrl='/parametri/imballaggio/list'
        return Page(req).redirect(redirectUrl)

    def __del__(req, action=None):
        id = req.form.get("idr")
        dao = Imballaggio().getRecord(id=id)
        if dao:
            dao.delete()
        daos = Imballaggio(req=req).select(batchSize=None)
        pageData = {'file' : "/tree/treeImballaggio",
                    "action":action,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __edit__(req, action=None):
        id = req.form.get("idr")
        dao = Imballaggio().getRecord(id=id)
        pageData = {'file' : "/addedit/ae_imballaggio",
                    "action":action,
            "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        pageData = {'file' : "/addedit/ae_imballaggio",
                    "_dao_":"imballaggio",
                    "name": "Imballaggio",
                    "tree":"treeImballaggio",
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
