# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

try:
    menu=Table('menu', params['metadata'],schema = params['schema'],autoload=True)
except:
    menu = Table('menu', params['metadata'],
            Column('id', Integer, primary_key=True),
            Column('desciption', String(500), nullable=True),
            Column('name', String(50), nullable=False),
            Column('css', String(80) ),
            Column('active', Boolean, default=False),
            schema = params['schema'])
    menu.create(checkfirst=True)

class Menu(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'name' : menu.c.name==v}
        return  dic[k]

std_mapper = mapper(Menu, menu)
