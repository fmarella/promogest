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

online_userTable  = Table('online_user', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('sessionid',String(100),unique=True),
        Column('insert_date', DateTime),
        schema = params['schema'])
user_onlineTable.create(checkfirst=True)

class OnlineUser(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione':newscategory.c.denominazione == v,
                }
        return  dic[k]

onlineuser=Table('online_user', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(OnlineUser, onlineuser)
#filler()
