# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import Table
from sqlalchemy.orm import mapper
from core.Environment import *
from Dao import Dao

languageTable = Table('language', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('denominazione_breve', String(50), nullable=True),
        Column('denominazione', String(200), nullable=True),
        schema = params['mainSchema']
        )
languageTable.create(checkfirst=True)
s= select([languageTable.c.denominazione]).execute().fetchall()
if (u'Italiano',) not in s or s==[]:
    lang = languageTable.insert()
    lang.execute(denominazione = 'Italiano', denominazione_breve = 'it')
    lang.execute(denominazione = 'Inglese', denominazione_breve = 'en')
    lang.execute(denominazione = 'Tedesco', denominazione_breve = 'de')
    lang.execute(denominazione = 'Francese', denominazione_breve = 'fr')
    lang.execute(denominazione = 'Cinese', denominazione_breve = 'ci')
    lang.execute(denominazione = 'Spagnolo', denominazione_breve = 'es')
    lang.execute(denominazione = 'TUTTE', denominazione_breve = 'all')

class Language(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {}
        return  dic[k]

lang=Table('language', params['metadata'],
    schema = params['mainSchema'],
    autoload=True)

std_mapper = mapper(Language, lang, order_by=lang.c.denominazione)

