# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
# Licenza: GNU GPLv2

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao
from Role import Role
from Action import Action

roleTable = Table('role',params['metadata'], autoload=True, schema=params['mainSchema'])
actionTable = Table('action',params['metadata'], autoload=True, schema=params['mainSchema'])

if params["tipo_db"] == "sqlite":
    roleFK = 'role.id'
    actionFK = 'action.id'
else:
    roleFK = params['mainSchema']+'.role.id'
    actionFK = params['mainSchema']+'.action.id'

roleactionTable = Table('roleaction', params['metadata'],
        Column('id_role', Integer, ForeignKey(roleFK),primary_key=True),
        Column('id_action', Integer, ForeignKey(actionFK),primary_key=True),
        schema=params['mainSchema']
        )
roleactionTable.create(checkfirst=True)
s= select([roleactionTable.c.id_role]).execute().fetchall()
if (1,) not in s or s ==[]:
    ruolieazioni = roleactionTable.insert()
    for i in range(1,6):
        ruolieazioni.execute(id_role = 1, id_action =i)

class RoleAction(Dao):
    """ RoleAction class database functions  """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_role':
            dic = {k:roleaction.c.id_role == v}
        elif k == 'id_action':
            dic = {k:roleaction.c.id_action == v}
        return  dic[k]

roleaction=Table('roleaction',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)
std_mapper = mapper(RoleAction, roleaction, properties={
            'role':relation(Role, backref='roleaction'),
            'action':relation(Action, backref='roleaction'),
                }, order_by=roleaction.c.id_role)