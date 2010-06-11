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
from promogest.dao.User import User

class UserRole(Dao):
    """ RoleAction class database functions  """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_role':
            dic = {k:userrole.c.id_role == v}
        elif k == 'idUser':
            dic = {k:userrole.c.id_user == v}
        return  dic[k]

userrole=Table('userrole',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)
std_mapper = mapper(UserRole, userrole, properties={
            'rol':relation(Role, backref='userrole'),
            #'use':relation(User, backref='userrole'),
                }, order_by=userrole.c.id_role)



