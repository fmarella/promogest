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

t_riga_prima_nota = Table('riga_prima_nota', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('denominazione', String(400), nullable=False),
        Column('id_testata_prima_nota', Integer,
            ForeignKey(fk_prefix+'testata_prima_nota.id', onupdate="CASCADE", ondelete="CASCADE")),
        Column('id_testata_documento', Integer,
            ForeignKey(fk_prefix+'testata_documento.id', onupdate="CASCADE", ondelete="RESTRICT"),
            nullable=True),
        Column('id_banca', Integer,
            ForeignKey(fk_prefix+"banca.id", onupdate="CASCADE", ondelete="RESTRICT"),
            nullable=True),
        Column('numero', Integer, nullable=False),
        Column('data_registrazione', DateTime, nullable=True),
        Column('tipo', String(25), nullable=False),
        Column('segno', String(25), nullable=False),
        Column('valore', Numeric(16, 4), nullable=False),
        Column('note_primanota', Text, nullable=True),
        schema=params["schema"],
        useexisting=True)

t_riga_prima_nota.create(checkfirst=True)
