# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Listino import Listino

def listino_table(soup=None, op=None, dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.listino.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = Listino().getRecord(id=[row.denominazione,row.data_listino])
        else:
            d = Listino().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = Listino()
            d.id = record.id
        else:
            d = Listino().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = Listino().select(id=row.id)
            if d:
                d = d[0]
        else:
            d = Listino().getRecord(id=loads(row.object))
    d.denominazione = record.denominazione
    d.descrizione = record.descrizione
    d.data_listino= record.data_listino
    d.listino_attuale = record.listino_attuale
    d.visible= record.visible
    d.persist()
    return True