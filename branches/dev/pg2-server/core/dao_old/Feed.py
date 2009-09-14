# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao

feedTable = Table('feed', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('url', String(500), nullable=False),
        Column('name', String(50), nullable=False),
        Column('active', Boolean, default=False),
        schema = params['schema']
        )
feedTable.create(checkfirst=True)

class Feed(Dao):
    # UserSl() class provides to make a Users dao which include more used
    # database functions

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'name' : feed.c.name==v}
        return  dic[k]


feed=Table('feed', params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(Feed, feed)
