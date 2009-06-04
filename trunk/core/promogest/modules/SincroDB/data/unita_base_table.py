# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.UnitaBase import UnitaBase


def unita_base_table(soup=None, op=None,dao=None, row=None):
    d = None
    if soup and not all:
        record = soup.unita_base.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = UnitaBase().getRecord(id=row.id)
        else:
            d = UnitaBase().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = UnitaBase()
            d.id = record.id
        else:
            d = UnitaBase().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = UnitaBase().getRecord(id=row.id)
        else:
            d = UnitaBase().getRecord(id=loads(row.object))
    d.denominazione = record.denominazione
    d.denominazione_breve = record.denominazione_breve
    d.persist()
    return True