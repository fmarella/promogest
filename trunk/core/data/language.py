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


t_language = Table('language', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('denominazione_breve', String(50), nullable=True),
        Column('denominazione', String(200), nullable=True),
        schema=params["mainSchema"]
        )
t_language.create(checkfirst=True)

s= select([t_language.c.denominazione]).execute().fetchall()
if (u'Italiano',) not in s or s==[]:
    lang = t_language.insert()
    lang.execute(denominazione = 'Italiano', denominazione_breve = 'it')
    lang.execute(denominazione = 'Inglese', denominazione_breve = 'en')
    lang.execute(denominazione = 'Tedesco', denominazione_breve = 'de')
    lang.execute(denominazione = 'Francese', denominazione_breve = 'fr')
    lang.execute(denominazione = 'Cinese', denominazione_breve = 'ci')
    lang.execute(denominazione = 'Spagnolo', denominazione_breve = 'es')
    lang.execute(denominazione = 'TUTTE', denominazione_breve = 'all')
