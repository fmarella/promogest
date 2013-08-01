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


t_inventario = Table('inventario', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('anno',Integer,nullable=False),
        Column('id_magazzino',Integer,ForeignKey(fk_prefix+'magazzino.id',onupdate="CASCADE",ondelete="CASCADE"),nullable=False),
        Column('id_articolo',Integer,ForeignKey(fk_prefix+'articolo.id',onupdate="CASCADE",ondelete="CASCADE"),nullable=False),
        Column('quantita',Numeric(16,4),nullable=True),
        Column('valore_unitario',Numeric(16,4),nullable=True),
        Column('data_aggiornamento',DateTime,nullable=True),
        schema=params["schema"]
        )
t_inventario.create(checkfirst=True)
