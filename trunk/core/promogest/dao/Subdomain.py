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
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao



try:
    subs=Table('subdomain', params['metadata'],schema = params['schema'],autoload=True)
except:
    subs = Table('subdomain', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('description', String(500), nullable=False),
        Column('name', String(50), nullable=False),
        Column('template', String(50), nullable=False),
        Column('active', Boolean, default=False),
        schema = params['schema']
        )
    subs.create(checkfirst=True)


class Subdomain(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'name' : subs.c.name==v}
        return  dic[k]


std_mapper = mapper(Subdomain, subs)
