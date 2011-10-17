# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao



try:
    subs=Table('subdomain', params['metadata'],schema = params['schema'],autoload=True)
except:
    subs = Table('subdomain', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('description', String(500), nullable=False),
        Column('name', String(50), nullable=False),
        Column('template', String(50), nullable=False),
        Column('active', Boolean, default=False),
        schema = params['schema']
        )
    subs.create(checkfirst=True)


class Subdomain(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'name' : subs.c.name==v}
        return  dic[k]


std_mapper = mapper(Subdomain, subs)
