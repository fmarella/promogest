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

t_testata_commessa = Table('testata_commessa', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('numero', Integer, nullable=False),
        Column('denominazione', String(300), nullable=False),
        Column('note', Text, nullable=True),
        Column('id_cliente', Integer,ForeignKey(fk_prefix +'cliente.id',onupdate="CASCADE",ondelete="CASCADE")),
        Column('id_articolo', Integer,ForeignKey(fk_prefix +'articolo.id')),
        Column('id_stadio_commessa', Integer,ForeignKey(fk_prefix +'stadio_commessa.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=True),
        Column('data_inizio', DateTime, nullable=True),
        Column('data_fine', DateTime, nullable=True),
        schema=params["schema"],
        useexisting=True)
t_testata_commessa.create(checkfirst=True)
