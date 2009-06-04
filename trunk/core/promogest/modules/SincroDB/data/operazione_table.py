# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Operazione import Operazione

def operazione_table(soup=None, op=None,dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.operazione.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = Operazione().getRecord(id=row.denominazione)
        else:
            d = Operazione().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = Operazione()
            d.denominazione = record.denominazione
        else:
            d = Operazione().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = Operazione().getRecord(id=row.denominazione)
        else:
            d = Operazione().getRecord(id=loads(row.object))
    d.segno= record.segno
    d.fonte_valore= record.fonte_valore
    d.tipo_persona_giuridica= record.tipo_persona_giuridica
    d.tipo_operazione= record.operazione
    d.persist()
    return True