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


def stato_articolo_table(soup=None, op=None,dao=None, row=None):
    d = None
    if soup and not all:
        record = soup.stato_articolo.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = StatoArticolo().getRecord(id=row.id)
        else:
            d = StatoArticolo().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = StatoArticolo()
            d.id = record.id
        else:
            d = StatoArticolo().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = StatoArticolo().getRecord(id=row.id)
        else:
            d = StatoArticolo().getRecord(id=loads(row.object))
    d.denominazione= record.denominazione
    d.persist()
    return True