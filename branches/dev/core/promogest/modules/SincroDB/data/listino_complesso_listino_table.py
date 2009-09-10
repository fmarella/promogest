# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.ListinoComplessoListino import ListinoComplessoListino

def listino_complesso_listino_table(soup=None, op=None, dao=None, row=None,all=False):
    d = None
    if soup and not all:
        record = soup.listino_complesso_listino.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = ListinoComplessoListino().getRecord(id=row.id_listino_complesso)
        else:
            d = ListinoComplessoListino().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = ListinoComplessoListino()
            d.id_listino_complesso = record.id_listino_complesso
        else:
            d = ListinoComplessoListino().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = ListinoComplessoListino().getRecord(id=row.id_listino_complesso)
            #if d:
                #d = d[0]
        else:
            d = ListinoComplessoListino().getRecord(id=loads(row.object))
    d.id_listino = record.id_listino
    d.persist()
    return True