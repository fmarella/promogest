#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from core.lib.page import Page
from core.lib.utils import addSlash
from core.dao.Inventario import Inventario
from core.dao.Articolo import Articolo
import datetime

def inventarioo(req, static= None,subdomain=None):
    """inventario"""
    pageData = {'file' : "inventario",
                "check":False}
    return Page(req).render(pageData)

def inventarioo_check(req, static= None,subdomain=None):
    """inventario_store"""
    art = None
    inve = None
    c_barre = req.form.get('cb')
    codice = req.form.get('codice')
    print "CODICE A BARRE SPARATO + LUNGHEZZA", c_barre, len(c_barre)
    if c_barre:
        art = Articolo().select(codiceABarreEM = c_barre)
        if not art and len(c_barre) < 13:
            art = Articolo().select(codiceABarreEM = "0"+c_barre)
        if art:
            art = art[0]
            inve = Inventario().select(idArticolo = art.id)
            if inve:
                inve = inve[0]
    elif codice:
        art = Articolo().select(codiceEM = codice)
        if art:
            art = art[0]
            inve = Inventario().select(idArticolo = art.id)
            if inve:
                inve = inve[0]
    pageData = {'file' : "inventario",
                "art": art,
                "inve":inve,
                "check":True}
    return Page(req).render(pageData)

def inventarioo_store(req, static= None,subdomain=None):
    """inventario_check"""
    qa = req.form.get('quantita')
    id_inv = req.form.get("id_inv")
    print "QUANTITA e ID ARTICOLO", qa, id_inv
    if qa and id_inv:
        inv = Inventario().getRecord(id=int(id_inv))
        inv.quantita = float(qa)
        inv.data_aggiornamento = datetime.datetime.now()
        inv.persist()
    elif id_inv:
        inv = Inventario().getRecord(id=int(id_inv))
        inv.data_aggiornamento = datetime.datetime.now()
        inv.persist()
    inventariati = Inventario().count(inventariato = True)
    print "NUMERO ARTICOLI INVENTARIATI", inventariati
    pageData = {'file' : "inventario",
                "inventariati":inventariati}
    return Page(req).render(pageData)
