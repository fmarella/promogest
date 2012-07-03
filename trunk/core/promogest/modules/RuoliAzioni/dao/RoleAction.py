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
from Action import Action

try:
    roleaction=Table('roleaction',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)
except:
    if tipodb == "sqlite":
        roleTable = Table('role',params["metadata"], autoload=True, schema=params["mainSchema"])
        actionTable = Table('action',params["metadata"], autoload=True, schema=params["mainSchema"])
        roleaction = Table('roleaction', params["metadata"],
            Column('id_role', Integer, ForeignKey('role.id'),primary_key=True),
            Column('id_action', Integer, ForeignKey('action.id'),primary_key=True),
            useexisting=True)
        roleaction.create(checkfirst=True)

class RoleAction(Dao):
    """ RoleAction class database functions  """
    def __init__(self, req=None):
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

idAdmin = Role().select(name ="Admin")
if not idAdmin:
    print "ATTENZIONE NON e' PRESENTE UN ADMIN"
else:
    idadmin = idAdmin[0].id
    idact = params["session"].query(Action.id).all()
    idract = params["session"].query(RoleAction.id_action).filter_by(id_role=idadmin).all()
    if idact != idract:
        ac = Action().select(batchSize=None)
        for a in ac:
            ra = RoleAction().select(id_role=idadmin,id_action=a.id, batchSize=None)
            if not ra:
                aa = RoleAction()
                aa.id_role = idadmin
                aa.id_action = a.id
                session.add(aa)
        params["session"].commit()
