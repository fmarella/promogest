# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Magazzino import Magazzino

def magazzino_table(soup=None, op=None,dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.magazzino.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = Magazzino().getRecord(id=row.id)
        else:
            d = Magazzino().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = Magazzino()
            d.id = record.id
        else:
            d = Magazzino().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = Magazzino().getRecord(id=row.id)
        else:
            d = Magazzino().getRecord(id=loads(row.object))
    d.denominazione = record.denominazione
    d.indirizzo = record.indirizzo
    d.localita = record.localita
    d.cap = record.cap
    d.provincia = record.provincia
    d.nazione = record.nazione
    d.data_ultima_stampa_giornale = record.data_ultima_stampa_giornale
    d.pvcode = record.pvcode
    d.persist()
    return True