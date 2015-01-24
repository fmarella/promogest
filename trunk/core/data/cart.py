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
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>."

from sqlalchemy import *
from promogest.Environment import *

params["session"].close()
t_cart = Table('cart', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('id_articolo',Integer, ForeignKey(fk_prefix+'articolo.id')),
        Column('quantita', Integer, nullable=True),
        Column('id_utente', Integer, ForeignKey(fk_prefix_main+'utente.id')),
        Column('data_inserimento',DateTime, nullable=True),
        Column('data_conferma',DateTime, nullable=True),
        Column('sessionid',String(50), nullable=True),
        Column('id_pagamento', Integer, ForeignKey(fk_prefix+'pagamento.id')),
        Column('id_cliente', Integer),
        schema=params["schema"]
        )
t_cart.create(checkfirst=True)
