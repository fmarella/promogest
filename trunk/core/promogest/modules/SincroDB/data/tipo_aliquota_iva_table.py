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
    if op =="DELETE":
        d = TipoAliquotaIva().getRecord(id=loads(row.object))
        if d:
            d.delete()
    else:
        if soup:
            record = soup.tipo_aliquota_iva.get(loads(row.object))
        else:
            record = row
        if op == "INSERT":
            try:
                d = TipoAliquotaIva().getRecord(id=loads(row.object))
            except:
                if not d:
                    d = TipoAliquotaIva()
                    d.id = record.id
        elif op == "UPDATE":
            try:
                d = TipoAliquotaIva().getRecord(id=loads(row.object))
            except:
                d = TipoAliquotaIva().getRecord(id=row.id)
        d.denominazione = record.denominazione
        d.persist()
    return True