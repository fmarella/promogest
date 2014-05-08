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

import datetime
from sqlalchemy import *
from promogest.Environment import *

t_testata_movimento = Table('testata_movimento', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('numero', Integer, nullable=False),
        Column('parte', Integer, nullable=True, default=1),
        Column('registro_numerazione', String(50), nullable=False),
        Column('operazione', String(100),ForeignKey(fk_prefix_main+"operazione.denominazione",onupdate="CASCADE",ondelete="RESTRICT"), nullable=True ),
        Column('data_movimento',DateTime,ColumnDefault(datetime.datetime.now), nullable=True),
        Column('data_inserimento',DateTime,ColumnDefault(datetime.datetime.now), nullable=True),
        Column('note_interne', Text, nullable=True),
        Column('note_pie_pagina', String(200), nullable=True),
        Column('id_testata_documento', Integer,ForeignKey(fk_prefix+'testata_documento.id',onupdate="CASCADE",ondelete="CASCADE"), nullable=True),
        Column('id_to_magazzino', Integer),
        Column('id_cliente', Integer,ForeignKey(fk_prefix+'cliente.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
        Column('id_fornitore', Integer,ForeignKey(fk_prefix+'fornitore.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
        UniqueConstraint('parte', 'numero', 'data_movimento'),
        CheckConstraint("parte < 4 AND parte >= 1"),
        schema=params["schema"]
        )
t_testata_movimento.create(checkfirst=True)
