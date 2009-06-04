# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.TipoAliquotaIva import TipoAliquotaIva


def tipo_aliquota_iva_table(soup=None, op=None,dao=None, row=None):
    d = None
    if soup and not all:
        record = soup.tipo_aliquota_iva.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = TipoAliquotaIva().getRecord(id=row.id)
        else:
            d = TipoAliquotaIva().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = TipoAliquotaIva()
            d.id = record.id
        else:
            d = TipoAliquotaIva().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = TipoAliquotaIva().getRecord(id=row.id)
        else:
            d = TipoAliquotaIva().getRecord(id=loads(row.object))
    d.denominazione= record.denominazione
    d.persist()
    return True