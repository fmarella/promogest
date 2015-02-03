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

t_magazzino = Table('magazzino', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('denominazione',String(100),nullable=False, unique=True),
        Column('indirizzo',String(200),nullable=True),
        Column('localita',String(200),nullable=True),
        Column('cap',String(20),nullable=True),
        Column('provincia',String(100),nullable=True),
        Column('nazione',String(100),nullable=True),
        Column('pvcode',String(5),nullable=True),
        Column('data_ultima_stampa_giornale',Date,nullable=True),
        schema=params["schema"],
        extend_existing=True
        )
t_magazzino.create(checkfirst=True)
