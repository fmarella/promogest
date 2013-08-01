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


t_articolo_kit = Table('articolo_kit', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('id_articolo_wrapper', Integer,
            ForeignKey(fk_prefix+'articolo.id', onupdate="CASCADE", ondelete="CASCADE")),
        Column('id_articolo_filler', Integer,
            ForeignKey(fk_prefix+'articolo.id', onupdate="CASCADE", ondelete="CASCADE"),
            nullable=True),
        Column('quantita', Numeric(16, 4), nullable=False),
        Column('data_inserimento', DateTime, nullable=False),
        Column('data_esclusione', DateTime, nullable=True),
        Column('attivo', Boolean, default=True), #potrebbe non servire ma lasciamolo
        Column('note', Text, nullable=True),
        schema=params["schema"],
        useexisting=True)
t_articolo_kit.create(checkfirst=True)
