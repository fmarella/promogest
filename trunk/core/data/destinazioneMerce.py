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

t_destinazione_merce = Table('destinazione_merce', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('denominazione',String(200),nullable=False),
        Column('indirizzo',String(200),nullable=True),
        Column('localita',String(100),nullable=True),
        Column('cap',String(10),nullable=True),
        Column('provincia',String(50),nullable=True),
        Column('id_cliente',Integer,ForeignKey(fk_prefix+'cliente.id',onupdate="CASCADE",ondelete="RESTRICT")),
        schema=params["schema"]
        )
t_destinazione_merce.create(checkfirst=True)
