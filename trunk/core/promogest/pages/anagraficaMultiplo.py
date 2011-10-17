#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from decimal import *
from promogest.lib.page import Page
from promogest.dao.Multiplo import Multiplo
from promogest.dao.UnitaBase import UnitaBase

def anagraficaMultiplo(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req, action=None):
        denominazione = None
        denominazione_breve = None
        if req.form.to_dict():
            denominazione = req.form.get("denominazione")
            denominazione_breve = req.form.get("denominazione_breve")
        daos = Multiplo(req=req).select(batchSize=None, denominazione=denominazione,
                                    denominazioneBreve=denominazione_breve)
        chiavi = {"denominazione" : denominazione,
                    "denominazione_breve":denominazione_breve}
        pageData = {'file' : "anagraficaSemplice",
                    "_dao_":"multiplo",
                    "name": "Multiplo",
                    "tree":"treeMultiplo",
                    "fkey":"fk_multiplo",
                    "chiavi":chiavi,
                    "action":action,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __add__(req, action=None):
        """ TODO: Gestione dei campi obbligatori e delle chiavi duplicate"""
        id = req.form.get("id")
        if action == "add":
            dao = Multiplo()
        else:
            dao = Multiplo().getRecord(id=id)
        dao.denominazione = req.form.get("denominazione")
        dao.denominazione_breve = req.form.get("denominazione_breve")
        dao.id_unita_base = int(req.form.get("id_unita_base"))
        dao.moltiplicatore = float(req.form.get("moltiplicatore"))
        if req.form.get("denominazione") \
                and req.form.get("denominazione_breve") \
                and req.form.get("moltiplicatore"):
            dao.persist()
        redirectUrl='/parametri/multiplo/list'
        return Page(req).redirect(redirectUrl)

    def __del__(req, action=None):
        """  """
        id = req.form.get("idr")
        dao = Multiplo().getRecord(id=id)
        if dao:
            dao.delete()
        daos = Multiplo(req=req).select(batchSize=None)
        pageData = {'file' : "/tree/treeMultiplo",
                    "_dao_":"multiplo",
                    "name": "Multiplo",
                    "tree":"treeMultiplo",
                    "action":action,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __edit__(req, action=None):
        id = req.form.get("idr")
        dao = Multiplo().getRecord(id=id)
        unitabase = UnitaBase().select(batchSize=None)
        pageData = {'file' : "/addedit/ae_multiplo",
                    "unitabase":unitabase,
                    "_dao_":"multiplo",
                    "name": "Multiplo",
                    "tree":"treeMultiplo",
                    "action":action,
                    "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        unitabase = UnitaBase().select(batchSize=None)
        pageData = {'file' : "/addedit/ae_multiplo",
                    "_dao_":"multiplo",
                    "name": "Multiplo",
                    "tree":"treeMultiplo",
                    "action":action,
                    "unitabase":unitabase}
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
