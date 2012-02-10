# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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
from Dao import Dao
from User import User

userTable = Table('utente', meta, autoload=True, schema=mainSchema)

try:
    access = Table('access', meta, schema=mainSchema, autoload=True)
except:

    if tipodb == "sqlite":
        utenteFK = 'utente.id'
    else:
        utenteFK = mainSchema + '.utente.id'

    access = Table('access', meta,
            Column('id', Integer, primary_key=True),
            Column('id_user', Integer, ForeignKey(utenteFK,
                onupdate="CASCADE",
                ondelete="CASCADE")),
            Column('login', Date, nullable=True),
            Column('logout', Date, nullable=True),
            schema=schema_azienda)
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
