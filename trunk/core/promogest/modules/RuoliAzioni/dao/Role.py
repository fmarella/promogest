# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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


try:
    role=Table('role',params['metadata'],schema = params['mainSchema'],autoload=True)
except:
    if tipodb == "sqlite":
        role = Table('role', params['metadata'],
            Column('id', Integer, primary_key=True),
            Column('name', String(50), nullable=False),
            Column('descrizione', String(250), nullable=False),
            Column('id_listino', Integer),
            Column('active', Boolean, default=False),
            useexisting=True)
        role.create(checkfirst=True)
        s= select([role.c.name]).execute().fetchall()
        if (u'Admin',) not in s or s ==[]:
            ruoli = role.insert()
            ruoli.execute(name = "Admin", descrizione = "Gestore del promogest", active = True)
            ruoli.execute(name = "Magazzino", descrizione = "Gestione magazzino", active = True)
            ruoli.execute(name = "Venditore", descrizione = "Addetto alla vendita", active = True)
            ruoli.execute(name = "Fatturazione", descrizione = "Fatturazione", active = True)


class Role(Dao):
    """
    Role class provides to make a Users dao which include more used
    database functions
    """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k =="idRole":
            dic= {k : role.c.id == v}
        elif k == "name":
            dic= { k : role.c.name.ilike("%"+v+"%")}
        return  dic[k]
std_mapper = mapper(Role, role, order_by=role.c.id)
