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

t_cliente_categoria_cliente = Table('cliente_categoria_cliente', params["metadata"],
        Column('id_cliente',Integer,ForeignKey(fk_prefix+'cliente.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
        Column('id_categoria_cliente',Integer,ForeignKey(fk_prefix+'categoria_cliente.id',onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
        schema=params["schema"],
        extend_existing=True
        )
t_cliente_categoria_cliente.create(checkfirst=True)
