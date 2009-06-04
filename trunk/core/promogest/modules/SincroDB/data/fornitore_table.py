# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Fornitore import Fornitore


def fornitore_table(soup=None, op=None,dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.fornitore.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = Fornitore().getRecord(id=row.id)
        else:
            d = Fornitore().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = Fornitore()
            d.id = record.id
        else:
            d = Fornitore().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = Fornitore().getRecord(id=row.id)
        else:
            d = Fornitore().getRecord(id=loads(row.object))
    d.id_categoria_fornitore = record.id_categoria_fornitore
    d.id_pagamento = record.id_pagamento
    d.id_magazzino = record.id_magazzino

    d.persist()
    return True