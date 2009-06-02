# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.ListinoArticolo import ListinoArticolo

def listino_articolo_table(soup=None, op=None, dao=None, row=None):
    if op =="DELETE":
        d = ListinoArticolo().getRecord(id=loads(row.object))
        if d:
            d.delete()
    else:
        record = soup.listino_articolo.get(loads(row.object))
        if op == "INSERT":
            d = ListinoArticolo().getRecord(id=loads(row.object))
            if not d:
                d = Listino()
                d.id_articolo = record.id_articolo
                d.id_articolo = record.id_articolo
                d.data_listino_articolo = record.data_listino_articolo
        elif op == "UPDATE":
            d = ListinoArticolo().getRecord(id=loads(row.object))
        d.prezzo_dettaglio = record.prezzo_dettaglio
        d.prezzo_ingrosso = record.prezzo_ingrosso
        d.ultimo_costo= record.ultimo_costo
        d.listino_attuale = record.listino_attuale
        d.persist()
    return True