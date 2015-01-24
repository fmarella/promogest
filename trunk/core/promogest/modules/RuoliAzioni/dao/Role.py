# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from promogest.dao.Dao import Dao, Base

class Role(Base, Dao):
    """
    Role class provides to make a Users dao which include more used
    database functions
    """
    try:
        __table__ = Table('role',params['metadata'],schema = mainSchema,autoload=True,autoload_with=engine)
    except:
        __table__ = Table('role', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('name', String(50), nullable=False),
            Column('descrizione', String(250), nullable=False),
            Column('id_listino', Integer),
            Column('active', Boolean, default=0),
            schema=params["mainSchema"]
            )

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k =="idRole":
            dic= {k : Role.__table__.c.id == v}
        elif k == "name":
            dic= { k : Role.__table__.c.name.ilike("%"+v+"%")}
        return  dic[k]
