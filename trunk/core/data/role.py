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
from promogest.Environment import *


t_role = Table('role', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('name', String(50), nullable=False),
        Column('descrizione', String(250), nullable=False),
        Column('id_listino', Integer),
        Column('active', Boolean, default=0),
        schema=params["mainSchema"]
        )
t_role.create(checkfirst=True)

s= select([t_role.c.name]).execute().fetchall()
if (u'Admin',) not in s or s ==[]:
    ruoli = t_role.insert()
    ruoli.execute(name = "Admin", descrizione = "Gestore del promogest", active = True)
    ruoli.execute(name = "Magazzino", descrizione = "Gestione magazzino", active = True)
    ruoli.execute(name = "Venditore", descrizione = "Addetto alla vendita", active = True)
    ruoli.execute(name = "Fatturazione", descrizione = "Fatturazione", active = True)
    ruoli.execute(name = "Cliente", descrizione = "Cliente", active = True)
