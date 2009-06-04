# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.Fornitura import Fornitura


def fornitura_table(soup=None, op=None,dao=None, row=None, all=False):
    d = None
    if soup and not all:
        record = soup.fornitura.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = Fornitura().getRecord(id=row.id)
        else:
            d = Fornitura().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = Fornitura()
            d.id = record.id
        else:
            d = Fornitura().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = Fornitura().getRecord(id=row.id)
        else:
            d = Fornitura().getRecord(id=loads(row.object))

    d.codice_articolo_fornitore = record.codice_articolo_fornitore
    d.prezzo_lordo = record.prezzo_lordo
    d.prezzo_netto = record.prezzo_netto
    d.applicazione_sconti = record.applicazione_sconti
    d.scorta_minima = record.scorta_minima
    d.tempo_arrivo_merce = record.tempo_arrivo_merce
    d.fornitore_preferenziale = record.fornitore_preferenziale
    d.percentuale_iva = record.percentuale_iva
    d.data_fornitura = record.data_fornitura
    d.data_prezzo = record.data_prezzo
    d.id_fornitore = record.id_fornitore
    d.id_articolo = record.id_articolo
    d.id_multiplo = record.id_multiplo
    d.persist()
    return True