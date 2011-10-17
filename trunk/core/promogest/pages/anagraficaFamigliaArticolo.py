#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from decimal import *
from promogest.lib.page import Page
from promogest.dao.FamigliaArticolo import FamigliaArticolo


def anagraficaFamigliaArticolo(req, action=None):
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
        daos = FamigliaArticolo(req=req).select(batchSize=None,
                                denominazione=denominazione,
                                denominazioneBreve=denominazione_breve)
        pageData = {'file' : "anagraficaSemplice",
                    "_dao_":"famiglia_articolo",
                    "name": "Famiglia Articolo",
                    "tree":"treeFamigliaArticolo",
                    "fkey":"fk_famigliaarticolo",
                    "action":action,
                    "chiavi":chiavi,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __add__(req, action=None):
        """ TODO: Gestione dei campi obbligatori e delle chiavi duplicate"""
        id = req.form.get("id")
        percentuale_detrazione= float(req.form.get("percentuale_detrazione")or 0)
        if action == "add":
            dao = AliquotaIva()
        else:
            dao = AliquotaIva().getRecord(id=id)
        dao.denominazione = req.form.get("denominazione")
        dao.denominazione_breve = req.form.get("denominazione_breve")
        dao.id_tipo = int(req.form.get("id_tipo"))
        dao.percentuale = Decimal(str(req.form.get("percentuale")))
        dao.percentuale_detrazione = percentuale_detrazione
        dao.descrizione_detrazione = req.form.get("descrizione_detrazione")
        if req.form.get("denominazione") \
                and req.form.get("denominazione_breve") \
                and req.form.get("percentuale"):
            dao.persist()
        redirectUrl='/parametri/famiglia_articolo/list'
        return Page(req).redirect(redirectUrl)

    def __del__(req, action=None):
        """ TODO: Gestione delle chiavi non cancellabili """
        id = req.form.get("idr")
        dao = AliquotaIva().getRecord(id=id)
        if dao:
            dao.delete()
        daos = AliquotaIva(req=req).select(batchSize=None)
        pageData = {'file' : "/tree/treeFamigliaArticolo",
                    "_dao_":"famiglia_articolo",
                    "name": "Famiglia Articolo",
                    "tree":"treeFamigliaArticolo",
                    "fkey":"fk_famigliaarticolo",
                    "action":action,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __edit__(req, action=None):
        id = req.form.get("idr")
        dao = FamigliaArticolo().getRecord(id=id)
        famigliapadre = FamigliaArticolo().select(batchSize=None)
        pageData = {'file' : "/addedit/ae_famigliaarticolo",
                    "famigliapadre":famigliapadre,
                    "_dao_":"famiglia_articolo",
                    "name": "Famiglia Articolo",
                    "tree":"treeFamigliaArticolo",
                    "fkey":"fk_famigliaarticolo",
                    "action":action,
                    "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        famigliapadre = FamigliaArticolo().select(batchSize=None)
        pageData = {'file' : "/addedit/ae_famigliaarticolo",
                    "_dao_":"famiglia_articolo",
                    "name": "Famiglia Articolo",
                    "tree":"treeFamigliaArticolo",
                    "fkey":"fk_famigliaarticolo",
                    "action":action,
                    "famigliapadre":famigliapadre}
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
