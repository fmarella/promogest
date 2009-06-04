# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Language import Language


def language_table(soup=None, op=None,dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.language.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = Language().getRecord(id=row.id)
        else:
            d = Language().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = Language()
            d.id = record.id
        else:
            d = Language().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = Language().getRecord(id=row.id)
        else:
            d = Language().getRecord(id=loads(row.object))
    d.denominazione = record.denominazione
    d.denominazione_breve = record.denominazione_breve
    d.persist()
    return True