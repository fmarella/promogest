# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

class RoleActionDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.mainSchema=mainSchema
        self.debug = debug

    def create(self):
        roleTable = Table('role',self.metadata, autoload=True, schema=self.mainSchema)
        actionTable = Table('action',self.metadata, autoload=True, schema=self.mainSchema)

        if self.schema:
            roleFK = self.mainSchema+'.role.id'
            actionFK = self.mainSchema+'.action.id'
        else:
            roleFK = 'role.id'
            actionFK = 'action.id'

        roleactionTable = Table('roleaction', self.metadata,
                Column('id_role', Integer, ForeignKey(roleFK),primary_key=True),
                Column('id_action', Integer, ForeignKey(actionFK),primary_key=True),
                schema=self.mainSchema
                )
        roleactionTable.create(checkfirst=True)
        s= select([roleactionTable.c.id_role]).execute().fetchall()
        if (1,) not in s or s ==[]:
            ruolieazioni = roleactionTable.insert()
            for i in range(1,15):
                ruolieazioni.execute(id_role = 1, id_action =i)


    def data(self):
        roleactionTable = Table('roleaction',self.metadata, autoload=True, schema=self.schema)
        ruolieazioni = roleactionTable.insert()
        for i in range(1,15):
            ruolieazioni.execute(id_role = 1, id_action =i)
