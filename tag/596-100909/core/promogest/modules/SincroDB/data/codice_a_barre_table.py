# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo

def codice_a_barre_articolo_table(soup=None, op=None, dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.codice_a_barre_articolo.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = CodiceABarreArticolo().getRecord(id=row.id)
        else:
            d = CodiceABarreArticolo().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = CodiceABarreArticolo()
            d.id = record.id
        else:
            d = CodiceABarreArticolo().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = CodiceABarreArticolo().getRecord(id=row.id)
        else:
            d = CodiceABarreArticolo().getRecord(id=loads(row.object))
        if not d:
            d = CodiceABarreArticolo()
            d.id = record.id
    d.codice = record.codice
    d.id_articolo = record.id_articolo
    d.primario = record.primario

    d.persist()
    return True