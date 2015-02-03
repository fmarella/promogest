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

t_tipo_recapito = Table('tipo_recapito', params["metadata"],
        Column('denominazione',String(100),primary_key=True),
        schema=params["mainSchema"],
        extend_existing=True
        )
t_tipo_recapito.create(checkfirst=True)


s= select([t_tipo_recapito.c.denominazione]).execute().fetchall()
if (u'Telefono',) not in s or s==[]:
    tipo = t_tipo_recapito.insert()
    tipo.execute(denominazione='Telefono')
    tipo.execute(denominazione='Cellulare')
    tipo.execute(denominazione='Indirizzo')
    tipo.execute(denominazione= "Citta'")
    tipo.execute(denominazione='CAP')
    tipo.execute(denominazione='Nazione')
    tipo.execute(denominazione='Info')
    tipo.execute(denominazione='Fax')
    tipo.execute(denominazione='Email')
    tipo.execute(denominazione='MSN')
    tipo.execute(denominazione='Provincia')
    tipo.execute(denominazione='Sito')
    tipo.execute(denominazione='Skype')
