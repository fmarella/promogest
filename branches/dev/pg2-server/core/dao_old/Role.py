# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import params
from Dao import Dao

roleTable = Table('role', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('name', String(50), nullable=False),
        Column('descrizione', String(250), nullable=False),
        Column('id_listino', Integer),
        Column('active', Boolean, default=0),
        schema = params['mainSchema']
        )
roleTable.create(checkfirst=True)

s= select([roleTable.c.name]).execute().fetchall()

if (u'Admin',) not in s or s ==[]:
    ruoli = roleTable.insert()
    ruoli.execute(name = "Admin", descrizione = "Gestore del promoWEB", active = True)
    ruoli.execute(name = "Guest", descrizione = "Guest", active = True)
    ruoli.execute(name = "Publisher", descrizione = "Publisher", active = True)
    ruoli.execute(name = "User", descrizione = "User", active = True)

class Role(Dao):
    """
    Role class provides to make a Users dao which include more used
    database functions
    """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'name' : role.c.name.ilike("%"+v+"%")}
        return  dic[k]

role=Table('role',params['metadata'],schema = params['mainSchema'],autoload=True)
std_mapper = mapper(Role, role, order_by=role.c.id)