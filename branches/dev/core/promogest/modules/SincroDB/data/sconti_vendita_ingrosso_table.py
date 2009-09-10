# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso

def sconti_vendita_ingrosso_table(soup=None, op=None, dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.sconti_vendita_ingrosso.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = ScontoVenditaIngrosso().getRecord(id=row.id)
        else:
            d = ScontoVenditaIngrosso().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = ScontoVenditaIngrosso()
            d.id = record.id
        else:
            d = ScontoVenditaIngrosso().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = ScontoVenditaIngrosso().getRecord(id=row.id)
        else:
            d = ScontoVenditaIngrosso().getRecord(id=loads(row.object))
        if not d:
            d = ScontoVenditaIngrosso()
            d.id = record.id
    d.id_listino = record.id_listino
    d.id_articolo = record.id_articolo
    d.data_listino_articolo = record.data_listino_articolo

    d.persist()
    return True