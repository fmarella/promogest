# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.TipoRecapito import TipoRecapito


def tipo_recapito_table(soup=None, op=None,dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.tipo_recapito.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = TipoRecapito().getRecord(id=row.id)
        else:
            d = TipoRecapito().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = TipoRecapito()
            d.id = record.id
        else:
            d = TipoRecapito().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = TipoRecapito().getRecord(id=row.id)
        else:
            d = TipoRecapito().getRecord(id=loads(row.object))
    d.denominazione = record.denominazione
    d.persist()
    return True