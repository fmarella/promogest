# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.CategoriaCliente import CategoriaCliente

def categoria_cliente_table(soup=None, op=None, dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.categoria_cliente.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = CategoriaCliente().getRecord(id=row.id)
        else:
            d = CategoriaCliente().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = CategoriaCliente()
            d.id = record.id
        else:
            d = CategoriaCliente().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = CategoriaCliente().getRecord(id=row.id)
        else:
            d = CategoriaCliente().getRecord(id=loads(row.object))
    d.descrizione = record.descrizione
    d.denominazione= record.denominazione
    d.active= record.active
    d.persist()
    return True