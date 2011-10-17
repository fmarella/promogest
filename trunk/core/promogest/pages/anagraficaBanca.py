#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from promogest.lib.page import Page
from promogest.dao.Banca import Banca

def anagraficaBanca(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req, action=None):
        denominazione = None
        agenzia = None
        iban = None
        if req.form.to_dict():
            denominazione = req.form.get("denominazione")
            agenzia = req.form.get("agenzia")
            iban = req.form.get("iban")
        chiavi = {"denominazione" : denominazione,
                    "agenzia":agenzia,
                    "iban":iban}
        daos = Banca(req=req).select(batchSize=None,
                                        denominazione=denominazione,
                                        agenzia=agenzia,
                                        iban=iban)
        pageData = {'file' : "anagraficaSemplice",
                    "dao":"Banca",
                    "_dao_":"banca",
                    "name": "Banca",
                    "tree":"treeBanca",
                    "fkey":"fk_banca",
                    "action":action,
                    "chiavi":chiavi,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __add__(req, action=None):
        id = req.form.get("id")
        denominazione = req.form.get("denominazione")
        if action == "add":
            dao = Banca()
        else:
            dao = Banca().getRecord(id=id)
        dao.denominazione = req.form.get("denominazione")
        dao.agenzia = req.form.get("agenzia")
        dao.iban = req.form.get("iban")
        if denominazione:
            dao.persist()
        redirectUrl='/parametri/banca/list'
        return Page(req).redirect(redirectUrl)

    def __del__(req, action=None):
        id = req.form.get("idr")
        dao = Banca().getRecord(id=id)
        if dao:
            dao.delete()
        daos = Banca(req=req).select(batchSize=None)
        pageData = {'file' : "/tree/treeBanca",
                    "action":action,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __edit__(req, action=None):
        id = req.form.get("idr")
        dao = Banca().getRecord(id=id)
        pageData = {'file' : "/addedit/ae_banca",
                    "action":action,
            "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        pageData = {'file' : "/addedit/ae_banca",
                    "_dao_":"banca",
                    "name": "Banca",
                    "tree":"treeBanca",
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
