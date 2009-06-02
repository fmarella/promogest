# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Listino import Listino

def listino_table(soup=None, op=None, dao=None, row=None):
    if op=="DELETE":
        listi = Listino().getRecord(id=loads(row.object))
        if listi:
            listi.delete()
    else:
        record = soup.listino.get(loads(row.object))
        if op == "INSERT":
            listi = Listino().getRecord(id=loads(row.object))
            if not listi:
                listi = Listino()
                listi.id = record.id
        elif op == "UPDATE":
            listi = Listino().getRecord(id=loads(row.object))
        listi.denominazione = record.denominazione
        listi.descrizione = record.descrizione
        listi.data_listino= record.data_listino
        listi.listino_attuale = record.listino_attuale
        listi.visible= record.visible
        listi.persist()
    return True