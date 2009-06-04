# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.CategoriaArticolo import CategoriaArticolo

def categoria_articolo_table(soup=None, op=None, dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.categoria_articolo.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = CategoriaArticolo().getRecord(id=row.id)
        else:
            d = CategoriaArticolo().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = CategoriaArticolo()
            d.id = record.id
        else:
            d = CategoriaArticolo().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = CategoriaArticolo().getRecord(id=row.id)
        else:
            d = CategoriaArticolo().getRecord(id=loads(row.object))
    d.denominazione_breve = record.denominazione_breve
    d.denominazione= record.denominazione
    d.persist()
    return True