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
from core.Environment import *
from Dao import Dao
from User import User
from Modulo import Modulo

userTable = Table('utente', params['metadata'], autoload=True, schema=params['mainSchema'])
modulo=Table('modulo', params['metadata'],schema = params['schema'],autoload=True)

try:
    usermodulo=Table('user_modulo', params['metadata'],schema = params['schema'],autoload=True)
except:
    if params["tipo_db"] == "sqlite":
        utenteFK ='utente.id'
        moduloFK ='modulo.id'
    else:
        utenteFK =params['mainSchema']+'.utente.id'
        moduloFK =params['schema']+'.modulo.id'

    usermodulo  = Table('user_modulo', params["metadata"],
            Column('id',Integer,primary_key=True),
            Column('activation_date', DateTime, nullable=True),
            Column('id_modulo',Integer,ForeignKey(moduloFK)),
            Column('active', Boolean, default=0),
            Column('id_user', Integer,ForeignKey(utenteFK)),
            schema = params['schema'])
    usermodulo.create(checkfirst=True)

class UserModule(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)


    def filter_values(self, k,v):
        if k == "installation_code":
            dic= { k : userm.c.installation_code ==v}
        elif k =="active":
            dic = { k :usermodulo.c.active ==v}
        elif k =="idUser":
            dic = { k :usermodulo.c.id_user ==v}
        elif k =="idModule":
            dic = { k :usermodulo.c.id_modulo ==v}
        return  dic[k]


std_mapper = mapper(UserModule, usermodulo, properties={
            'user' : relation(User, backref="usermodulo"),
            'modulo' : relation(Modulo, backref="usermodulo"),
                }, order_by=usermodulo.c.id)
