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

def language_table(soup=None,soupLocale=None, op=None,dao=None,rowLocale=None, row=None, all=False):
    if op =="DELETE":
        soupLocale.delete(rowLocale)
    elif op == "INSERT":
        soupLocale.language.insert(id=row.id,
                            denominazione=row.denominazione,
                            denominazione_breve = row.denominazione_breve)
    elif op == "UPDATE":
        for i in rowLocale.c:
            t = str(i).split(".")[1] #mi serve solo il nome tabella
            setattr(rowLocale, t, getattr(row, t))
    sqlalchemy.ext.sqlsoup.Session.commit()
    return True