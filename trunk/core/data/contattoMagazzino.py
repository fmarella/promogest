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


try:
    t_contatto_magazzino = Table('contatto_magazzino', params["metadata"],
                            schema = params['schema'],
                            autoload=True)
except:
    t_contatto_magazzino = Table('contatto_magazzino', params["metadata"],
            Column('id',Integer,primary_key=True),
            Column('tipo_contatto',String(50),primary_key=True),
            Column('id_magazzino',Integer,ForeignKey(fk_prefix+'magazzino.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False),
            ForeignKeyConstraint(['id', 'tipo_contatto'],[fk_prefix+'contatto.id', fk_prefix+'contatto.tipo_contatto'],onupdate="CASCADE", ondelete="CASCADE"),
            CheckConstraint("tipo_contatto = 'magazzino'"),
            schema=params["schema"],
            extend_existing=True
            )
    t_contatto_magazzino.create(checkfirst=True)
