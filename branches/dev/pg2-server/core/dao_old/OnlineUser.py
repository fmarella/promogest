#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao

online_userTable  = Table('online_user', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('sessionid',String(100),unique=True),
        Column('insert_date', DateTime),
        schema = params['schema'])
user_onlineTable.create(checkfirst=True)

class OnlineUser(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione':newscategory.c.denominazione == v,
                }
        return  dic[k]

onlineuser=Table('online_user', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(OnlineUser, onlineuser)
#filler()