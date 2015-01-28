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

t_testata_scontrino = Table('testata_scontrino', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('data_inserimento',DateTime,ColumnDefault(datetime.datetime.now),nullable=False),
            Column('totale_scontrino',Numeric(16,4),nullable=False),
            Column('totale_contanti',Numeric(16,4),nullable=False),
            Column('totale_assegni',Numeric(16,4),nullable=False),
            Column('totale_carta_credito',Numeric(16,4),nullable=False),
            Column('id_magazzino',Integer,ForeignKey(fk_prefix + "magazzino.id", onupdate="CASCADE", ondelete="RESTRICT")),
            Column('id_pos',Integer,ForeignKey(fk_prefix +"pos.id", onupdate="CASCADE", ondelete="RESTRICT")),
            Column('id_ccardtype',Integer,ForeignKey(fk_prefix +"credit_card_type.id", onupdate="CASCADE", ondelete="RESTRICT")),
            Column('id_user',Integer),
            Column('id_testata_movimento',Integer,ForeignKey(fk_prefix + "testata_movimento.id", onupdate="CASCADE", ondelete="RESTRICT")),
            schema=params['schema'],
                    extend_existing=True,
            )
t_testata_scontrino.create(checkfirst=True)
