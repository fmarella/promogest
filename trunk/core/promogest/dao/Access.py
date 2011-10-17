#-*- coding: utf-8 -*-
#
# Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from User import User

userTable = Table('utente',params['metadata'], autoload=True, schema=params['mainSchema'])

try:
    access=Table('access', params['metadata'],schema = params['schema'],autoload=True)
except:

    if params["tipo_db"] == "sqlite":
        utenteFK = 'utente.id'
    else:
        utenteFK = params['mainSchema']+'.utente.id'

    access = Table('access', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('id_user',Integer,ForeignKey(utenteFK,onupdate="CASCADE",ondelete="CASCADE")),
            Column('login', Date, nullable=True),
            Column('logout', Date, nullable=True),
            schema=params['schema'])
    access.create(checkfirst=True)

class Access(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(k,v):
        dic= {  'keys' : access.c.key.contains(v),
                'value':access.c.value == v}
        return  dic[k]


std_mapper = mapper(Access, access, properties={
                            'utente':relation(User)
                            })
