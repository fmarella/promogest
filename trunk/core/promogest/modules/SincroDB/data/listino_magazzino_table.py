# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.ListinoMagazzino import ListinoMagazzino

def listino_magazzino_table(soup=None, op=None, dao=None, row=None,all=False):
    d = None
    if soup and not all:
        record = soup.listino_magazzino.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = ListinoMagazzino().getRecord(id=[row.id_listino,row.id_magazzino])
        else:
            d = ListinoMagazzino().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = ListinoMagazzino()
            d.id_listino = record.id_listino
            d.id_magazzino = record.id_magazzino
        else:
            d = ListinoArticolo().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = ListinoArticolo().getRecord(id=[row.id_listino,row.id_magazzino])
            #if d:
                #d = d[0]
        else:
            d = ListinoArticolo().getRecord(id=loads(row.object))
    d.persist()
    return True