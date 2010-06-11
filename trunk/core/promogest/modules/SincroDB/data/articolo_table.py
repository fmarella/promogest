# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Articolo import Articolo

def articolo_table(soup=None, op=None, dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.articolo.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = Articolo().getRecord(id=row.id)
        else:
            d = Articolo().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = Articolo()
            d.id = record.id
        else:
            d = Articolo().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = Articolo().getRecord(id=row.id)
        else:
            d = Articolo().getRecord(id=loads(row.object))
        if not d:
            d = Articolo()
            d.id = record.id

    d.codice = record.codice
    d.denominazione = record.denominazione
    d.id_aliquota_iva = record.id_aliquota_iva
    d.id_famiglia_articolo = record.id_famiglia_articolo
    d.id_categoria_articolo = record.id_categoria_articolo
    d.id_immagine = record.id_immagine
    d.id_unita_base = record.id_unita_base
    d.id_stato_articolo = record.id_stato_articolo
    d.produttore = record.produttore
    d.unita_dimensioni = record.unita_dimensioni
    d.lunghezza = record.lunghezza
    d.larghezza = record.larghezza
    d.altezza = record.altezza
    d.unita_volume = record.unita_volume
    d.volume = record.volume
    d.unita_peso = record.unita_peso
    d.peso_lordo = record.peso_lordo
    d.id_imballaggio = record.id_imballaggio
    d.peso_imballaggio = record.peso_imballaggio
    d.stampa_etichetta = record.stampa_etichetta
    d.codice_etichetta = record.codice_etichetta
    d.descrizione_etichetta = record.descrizione_etichetta
    d.stampa_listino = record.stampa_listino
    d.descrizione_listino = record.descrizione_listino
    d.aggiornamento_listino_auto = record.aggiornamento_listino_auto
    d.timestamp_variazione = record.timestamp_variazione
    d.note = record.note
    d.contenuto = record.contenuto
    d.cancellato = record.cancellato
    d.sospeso = record.sospeso
    d.quantita_minima = record.quantita_minima
    a = d.persist()
    if not a:
        g = Articolo().select(codice=record.codice)
        if g :
            g=g[0]
            g.codice = g.codice+"BIS"
            b = g.persist()
            if not b:
                print "PROPRIO NON SO COSA FARE HO ANCHE  CAMBIATO IL CODICE"
            articolo_table(soup=soup, op=op, dao=dao, row=row, all=all)
    return True