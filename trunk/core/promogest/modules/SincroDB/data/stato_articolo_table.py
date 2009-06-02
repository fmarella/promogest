# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.StatoArticolo import StatoArticolo

def stato_articolo_table(soup=None, op=None,rec=None, dao=None, row=None):
    if op =="DELETE":
        d = StatoArticolo().getRecord(id=loads(row.object))
        if d:
            d.delete()
    else:
        if soup:
            record = soup.stato_articolo.get(loads(row.object))
        else:
            record = rec 
        if op == "INSERT" and row:
            d = StatoArticolo().getRecord(id=loads(row.object))
            if not d:
                d = StatoArticolo()
                d.id = record.id
        elif op == "INSERT" and rec:
            reclocale= Environment.params['session'].query(StatoArticolo).all()
            for r in reclocale:
                r.delete()
            d = StatoArticolo()
            d.id = record.id
        elif op == "UPDATE":
            d = StatoArticolo().getRecord(id=loads(row.object))
        d.denominazione = record.denominazione
        d.persist()
    return True