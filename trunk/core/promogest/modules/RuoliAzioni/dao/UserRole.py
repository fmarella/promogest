# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from Role import Role
from promogest.dao.User import User

try:
    userrole=Table('userrole',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)
except:
    if tipodb == "sqlite":
        userTable = Table('utente',params["metadata"], autoload=True, schema=params["mainSchema"])
        roleTable = Table('role',params["metadata"], autoload=True, schema=params["mainSchema"])
        userrole = Table('userrole', params["metadata"],
            Column('id_role', Integer, ForeignKey('role.id'),primary_key=True),
            Column('id_user', Integer, ForeignKey('utente.id'),primary_key=True),
            useexisting=True)
        userrole.create(checkfirst=True)
        s= select([userrole.c.id_role]).execute().fetchall()
        if (1,) not in s or s ==[]:
            userruoli = userrole.insert()
            userruoli.execute(id_role = 1, id_user =1)


class UserRole(Dao):
    """ RoleAction class database functions  """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_role':
            dic = {k:userrole.c.id_role == v}
        elif k == 'idUser':
            dic = {k:userrole.c.id_user == v}
        return  dic[k]


std_mapper = mapper(UserRole, userrole, properties={
            'rol':relation(Role, backref='userrole'),
            #'use':relation(User, backref='userrole'),
                }, order_by=userrole.c.id_role)
