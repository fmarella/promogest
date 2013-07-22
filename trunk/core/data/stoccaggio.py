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


t_stoccaggio = Table('stoccaggio', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('scorta_minima', Integer, nullable=True),
        Column('livello_riordino', Integer, nullable=True),
        Column('data_fine_scorte', DateTime,nullable=True),
        Column('data_prossimo_ordine', DateTime, nullable=True),
        Column('id_articolo', Integer,ForeignKey(fk_prefix+'articolo.id',onupdate="CASCADE",ondelete="CASCADE"), nullable=True),
        Column('id_magazzino', Integer, ForeignKey(fk_prefix+'magazzino.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=False),
        schema=params["schema"]
        )
t_stoccaggio.create(checkfirst=True)
