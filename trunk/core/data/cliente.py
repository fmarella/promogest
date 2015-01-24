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
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.


from sqlalchemy import *
from promogest.Environment import *

try:
    t_cliente = Table('cliente',
                        params['metadata'],
                        schema=params['schema'],
                        autoload=True)
except:
    t_cliente = Table('cliente', params["metadata"],
            Column('id',Integer,ForeignKey(fk_prefix+'persona_giuridica.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_pagamento',Integer,ForeignKey(fk_prefix+'pagamento.id',onupdate="CASCADE",ondelete="RESTRICT")),
            Column('id_magazzino',Integer,ForeignKey(fk_prefix+'magazzino.id',onupdate="CASCADE",ondelete="RESTRICT")),
            Column('id_listino',Integer,ForeignKey(fk_prefix+'listino.id',onupdate="CASCADE",ondelete="RESTRICT")),
            Column('id_banca',Integer,ForeignKey(fk_prefix+'banca.id',onupdate="CASCADE",ondelete="RESTRICT")),
            Column('pagante', Boolean, default=False),
            Column('id_aliquota_iva', Integer, nullable=True),
            Column('tipo', String(2), default="PG"),
            extend_existing=True,
            schema=params["schema"]
            )
    t_cliente.create(checkfirst=True)
