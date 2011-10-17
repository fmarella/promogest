#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from decimal import *
from promogest.lib.page import Page
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.TipoAliquotaIva import TipoAliquotaIva

def anagraficaAliquotaIva(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req, action=None):
        denominazione = None
        if req.form.to_dict():
            denominazione = req.form.get("denominazione")
        daos = AliquotaIva(req=req).select(batchSize=None, denominazione=denominazione)
        chiavi = {"denominazione" : denominazione}
        pageData = {'file' : "anagraficaSemplice",
                    "_dao_":"aliquota_iva",
                    "name": "Aliquota Iva",
                    "tree":"treeAliquotaIva",
                    "fkey":"fk_aliquotaiva",
                    "chiavi":chiavi,
                    "action":action,
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
        redirectUrl='/parametri/aliquota_iva/list'
        return Page(req).redirect(redirectUrl)

    def __del__(req, action=None):
        """ TODO: Gestione delle chiavi non cancellabili """
        id = req.form.get("idr")
        dao = AliquotaIva().getRecord(id=id)
        if dao:
            dao.delete()
        daos = AliquotaIva(req=req).select(batchSize=None)
        pageData = {'file' : "/tree/treeAliquotaIva",
                    "_dao_":"aliquota_iva",
                    "name": "Aliquota Iva",
                    "tree":"treeAliquotaIva",
                    "fkey":"fk_aliquotaiva",
                    "action":action,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __edit__(req, action=None):
        id = req.form.get("idr")
        dao = AliquotaIva().getRecord(id=id)
        tipoAliquota = TipoAliquotaIva().select(batchSize=None)
        pageData = {'file' : "/addedit/ae_aliquotaiva",
                    "tipoAliquota":tipoAliquota,
                    "_dao_":"aliquota_iva",
                    "name": "Aliquota Iva",
                    "tree":"treeAliquotaIva",
                    "action":action,
                    "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        tipoAliquota = TipoAliquotaIva().select(batchSize=None)
        pageData = {'file' : "/addedit/ae_aliquotaiva",
                    "_dao_":"aliquota_iva",
                    "name": "Aliquota Iva",
                    "tree":"treeAliquotaIva",
                    "action":action,
                    "tipoAliquota":tipoAliquota}
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
