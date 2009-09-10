# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Sconto import Sconto

def sconto_table(soup=None, op=None, dao=None,rowLocale=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.sconto.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = Sconto().getRecord(id=row.id)
        else:
            d = Sconto().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = Sconto()
            d.id = record.id
        else:
            d = Sconto().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = Sconto().getRecord(id=row.id)
        else:
            d = Sconto().getRecord(id=loads(row.object))
        if not d:
            d = Sconto()
            d.id = record.id
    d.valore = record.valore
    d.tipo_sconto= record.tipo_sconto
    d.persist()
    return True