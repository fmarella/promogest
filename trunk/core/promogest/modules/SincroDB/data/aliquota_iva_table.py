# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.AliquotaIva import AliquotaIva

def aliquota_iva_table(soup=None, op=None, dao=None, row=None):
    if op =="DELETE":
        d = AliquotaIva().getRecord(id=loads(row.object))
        if d:
            d.delete()
    else:
        record = soup.aliquota_iva.get(loads(row.object))
        if op == "INSERT":
            d = AliquotaIva().getRecord(id=loads(row.object))
            if not d:
                d = AliquotaIva()
                d.id = record.id
        elif op == "UPDATE":
            d = AliquotaIva().getRecord(id=loads(row.object))
        d.id_tipo = record.id_tipo
        d.denominazione_breve = record.denominazione_breve
        d.denominazione= record.denominazione
        d.percentuale= record.percentuale
        d.percentuale_detrazione= record.percentuale_detrazione
        d.descrizione_detrazione = record.descrizione_detrazione
        d.persist()
    return True