# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
# Licenza: GNU GPLv2

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import params
from promogest.dao.Dao import Dao
from Role import Role
from Action import Action

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


