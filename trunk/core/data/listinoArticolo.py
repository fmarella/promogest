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
#from sqlalchemy.dialects import mysql

t_listino_articolo = Table('listino_articolo', params["metadata"],
        Column('id_listino', Integer,ForeignKey(fk_prefix+"listino.id"),primary_key=True),
        Column('id_articolo', Integer, ForeignKey(fk_prefix+"articolo.id"),primary_key=True),
        Column('prezzo_dettaglio', Numeric(16,4)),
        Column('prezzo_ingrosso', Numeric(16,4)),
        Column('ultimo_costo', Numeric(16,4), nullable=True),
        Column('data_listino_articolo', DateTime,ColumnDefault(datetime.datetime.now),nullable=False,primary_key=True),
        Column('listino_attuale', Boolean, nullable=False),
        #ForeignKeyConstraint(['id_listino', 'id_articolo'],[fk_prefix+'.listino.id', fk_prefix+'.articolo.id'],onupdate="CASCADE", ondelete="CASCADE"),
        CheckConstraint("prezzo_dettaglio is not NULL OR prezzo_ingrosso is not NULL"),
        schema=params["schema"],
        mysql_engine='InnoDB'

        )
t_listino_articolo.create(checkfirst=True)
