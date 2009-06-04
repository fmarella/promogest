# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment
from promogest.dao.AliquotaIva import AliquotaIva

def aliquota_iva_table(soup=None, op=None, dao=None, row=None, all=False):
    print "OPPPPPPPPPPPPPPPPPPP", op
    d = None
    if soup and not all:
        record = soup.aliquota_iva.get(loads(row.object))
    else:
        record = row
    if op =="DELETE":
        if all:
            d = AliquotaIva().getRecord(id=row.id)
        else:
            d = AliquotaIva().getRecord(id=loads(row.object))
        if d:
            d.delete()
        return True
    elif op == "INSERT":
        if all:
            d = AliquotaIva()
            d.id = record.id
        else:
            d = AliquotaIva().getRecord(id=loads(row.object))
    elif op == "UPDATE":
        if all:
            d = AliquotaIva().getRecord(id=row.id)
            print "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", d
        else:
            d = AliquotaIva().getRecord(id=loads(row.object))
    d.id_tipo = record.id_tipo
    d.denominazione_breve = record.denominazione_breve
    d.denominazione= record.denominazione
    d.percentuale= record.percentuale
    d.percentuale_detrazione= record.percentuale_detrazione
    d.descrizione_detrazione = record.descrizione_detrazione
    d.persist()
    return True