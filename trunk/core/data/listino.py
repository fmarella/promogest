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

if tipo_eng == "postgresql":
    colId = Column('id', Integer,Sequence('listino_id_seq',schema=params["schema"]),nullable=False,unique=True)
else:
    colId = Column('id', Integer,nullable=False)

t_listino = Table('listino', params["metadata"],
        #colId,
        Column('id',Integer,nullable=False, autoincrement=True,unique=True),
        Column('denominazione', String(200), nullable=False, primary_key=True),
        Column('descrizione', String(300), nullable=False),
        Column('data_listino', DateTime,ColumnDefault(datetime.datetime.now), nullable=False, primary_key=True),
        Column('listino_attuale', Boolean, nullable=True),
        Column('visible', Boolean, default=0),
        schema=params["schema"],
        extend_existing=True,
        mysql_engine='InnoDB'
        )
if tipo_eng == "postgresql":
    try:
        msg = "CREATE SEQUENCE %s.listino_id_seq" %params["schema"]
        DDL(msg).execute_at('before-create', t_listino)
    except:
        print("la relazione listino_id_seq esiste già")
t_listino.create(checkfirst=True)
