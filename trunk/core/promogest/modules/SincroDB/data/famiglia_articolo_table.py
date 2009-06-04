# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.FamigliaArticolo import FamigliaArticolo

def famiglia_articolo_table(soup=None, op=None, dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.famiglia_articolo.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = FamigliaArticolo().getRecord(id=row.id)
        else:
            d = FamigliaArticolo().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = FamigliaArticolo()
            d.id = record.id
        else:
            d = FamigliaArticolo().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = FamigliaArticolo().getRecord(id=row.id)
        else:
            d = FamigliaArticolo().getRecord(id=loads(row.object))
    d.denominazione_breve = record.denominazione_breve
    d.denominazione= record.denominazione
    d.codice = record.codice
    d.visible= record.visible
    d.id_padre = record.id_padre
    d.persist()
    return True