#-*- coding: utf-8 -*-
#
# Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao
from User import User


try:
    confirmregistration=Table('confirmregistration', params['metadata'],schema = params['schema'],autoload=True)
except:
    userTable = Table('utente',params['metadata'], autoload=True, schema=params['mainSchema'])

    if params["tipo_db"] == "sqlite":
        utenteFK = 'utente.id'
    else:
        utenteFK = params['mainSchema']+'.utente.id'

    confirmregistration = Table('confirm_registration', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('id_user',Integer,ForeignKey(utenteFK,onupdate="CASCADE",ondelete="CASCADE")),
            Column('code', String(300), nullable=False),
            Column('verified', Boolean, nullable=True),
            schema=params['schema']
            )
    confirmregistration.create(checkfirst=True)

class ConfirmRegistration(Dao):

    def __init__(self):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'code' : confirmregistration.c.code ==v}
        return  dic[k]

std_mapper = mapper(ConfirmRegistration, confirmregistration, properties={
                            'utente':relation(User)
                            })
