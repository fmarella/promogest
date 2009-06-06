# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import sqlalchemy
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest import Environment

def tipo_recapito_table(soup=None,soupLocale=None, op=None,dao=None,rowLocale=None, row=None, all=False):

    if op =="DELETE":
        soupLocale.delete(rowLocale)
    elif op == "INSERT":
        soupLocale.tipo_recapito.insert(id = row.id,
                                    denominazione= row.denominazione)
    elif op == "UPDATE":
        for i in rowLocale.c:
            t = str(i).split(".")[1] 
            setattr(rowLocale, t, getattr(row, t))
    sqlalchemy.ext.sqlsoup.Session.commit()
    return True