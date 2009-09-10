# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Stoccaggio import Stoccaggio


def stoccaggio_table(soup=None, op=None,dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.stoccaggio.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = Stoccaggio().getRecord(id=row.id)
        else:
            d = Stoccaggio().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = Stoccaggio()
            d.id = record.id
        else:
            d = Stoccaggio().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = Stoccaggio().getRecord(id=row.id)
        else:
            d = Stoccaggio().getRecord(id=loads(row.object))
    d.scorta_minima= record.scorta_minima
    d.livello_riordino = record.livello_riordino
    d.data_fine_scorte =record.data_fine_scorte
    d.data_prossimo_ordine = record.data_prossimo_ordine
    d.id_articolo = record.id_articolo
    d.id_magazzino = record.id_magazzino


    d.persist()
    return True