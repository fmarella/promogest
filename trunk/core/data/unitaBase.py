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

t_unita_base = Table('unita_base', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('denominazione_breve', String(50), nullable=True, unique=True),
            Column('denominazione', String(200), nullable=True),
            schema=params["mainSchema"]
            )
t_unita_base.create(checkfirst=True)

s= select([t_unita_base.c.denominazione_breve]).execute().fetchall()
unit = t_unita_base.insert()
if (u'pz',) not in s or s==[]:
    unit.execute(denominazione_breve='pz', denominazione='pezzi')
if (u'm',) not in s or s==[]:
    unit.execute(denominazione_breve='m', denominazione='Metri')
if (u'l',) not in s or s==[]:
    unit.execute(denominazione_breve='l', denominazione='Litri')
if (u'kg',) not in s or s==[]:
    unit.execute(denominazione_breve='kg', denominazione='Chilogrammi')
if (u'N',) not in s or s==[]:
    unit.execute(denominazione_breve='N', denominazione='Numero')
if (u'h',) not in s or s==[]:
    unit.execute(denominazione_breve='h', denominazione='Ore')
if (u'mq',) not in s or s==[]:
    unit.execute(denominazione_breve='mq', denominazione='Metri Quadri')
if (u'mc',) not in s or s==[]:
    unit.execute(denominazione = "Metri Cubi",denominazione_breve="mc")
if (u'gr',) not in s or s==[]:
    unit.execute(denominazione = "Grammi",denominazione_breve="gr")
if (u'ml',) not in s or s==[]:
    unit.execute(denominazione = "Millilitri",denominazione_breve="ml")
if (u'q',) not in s or s==[]:
    unit.execute(denominazione = "Quintali",denominazione_breve="q")
if (u't',) not in s or s==[]:
    unit.execute(denominazione = "Tonnellate",denominazione_breve="t")
