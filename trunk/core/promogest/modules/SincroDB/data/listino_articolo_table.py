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

def listino_articolo_table(soup=None, op=None, dao=None,rowLocale=None, row=None,all=False):
    d = None
    if soup and not all:
        record = soup.listino_articolo.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = ListinoArticolo().getRecord(id=[row.id_articolo,row.id_listino,row.data_listino_articolo])
        else:
            d = ListinoArticolo().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = ListinoArticolo()
            d.id_listino = record.id_listino
            d.id_articolo = record.id_articolo
            d.data_listino_articolo = record.data_listino_articolo
        else:
            d = ListinoArticolo().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            #d = ListinoArticolo().getRecord(id=[row.id_articolo,row.id_listino,row.data_listino_articolo])
            d = Environment.params["session"].query(ListinoArticolo).get((row.id_articolo,row.id_listino,row.data_listino_articolo))
        else:
            d = ListinoArticolo().getRecord(id=loads(row.object))
        if not d:
            d = ListinoArticolo()
            d.id_listino = record.id_listino
            d.id_articolo = record.id_articolo
            d.data_listino_articolo = record.data_listino_articolo
    d.prezzo_dettaglio = record.prezzo_dettaglio
    d.prezzo_ingrosso = record.prezzo_ingrosso
    d.ultimo_costo= record.ultimo_costo
    d.listino_attuale = record.listino_attuale
    a = d.persist()
    if not a:
        #g = ListinoArticolo().select(codice=record.codice)
        #if g :
            #g=g[0]
            #g.codice = g.codice+"BIS"
            #b = g.persist()
            #if not b:
        print "PROPRIO NON SO COSA FARE HO ANCHE  CAMBIATO IL CODICE"
        #listino_articolo_table(soup=soup, op=op, dao=dao, row=row, all=all)
    return True
