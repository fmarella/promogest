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

def tipo_aliquota_iva_table(soup=None, op=None,rec=None, dao=None, row=None):
    if op =="DELETE":
        d = TipoAliquotaIva().getRecord(id=loads(row.object))
        if d:
            d.delete()
    else:
        if soup:
            record = soup.tipo_aliquota_iva.get(loads(row.object))
        else:
            record = rec 
        if op == "INSERT" and row:
            d = TipoAliquotaIva().getRecord(id=loads(row.object))
            if not d:
                d = TipoAliquotaIva()
                d.id = record.id
        elif op == "INSERT" and rec:
            reclocale= Environment.params['session'].query(TipoAliquotaIva).all()
            for r in reclocale:
                r.delete()
            d = TipoAliquotaIva()
            d.id = record.id
        elif op == "UPDATE":
            d = TipoAliquotaIva().getRecord(id=loads(row.object))
        d.denominazione = record.denominazione
        d.persist()
    return True