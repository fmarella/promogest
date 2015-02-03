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

import datetime
from sqlalchemy import *
from promogest.Environment import *

NEUTRO = 0
ASCALARE = 1
TIPO = (
    (0, 'Neutro'),
    (1, 'A scalare')
)

CHIUSO = 0
APERTO = 1
STATO = (
    (0, "Chiuso"),
    (1, "Aperto")
)

#session.close()
t_storico_documento = Table('storico_documento', params["metadata"],
                            Column('id', Integer, primary_key=True),
                            Column('padre', Integer, ForeignKey(fk_prefix + 'testata_documento.id')),
                            Column('figlio', Integer, ForeignKey(fk_prefix + 'testata_documento.id')),
                            Column('data_creazione', DateTime, nullable=True),
                            Column('ultima_modifica', DateTime, nullable=True),
                            Column('data_chiusura', DateTime, nullable=True),
                            Column('stato', Integer, nullable=True),
                            Column('tipo', Integer, nullable=True, default=NEUTRO),
                            Column('note', Text, nullable=True),
                            schema=params['schema'],
                            extend_existing=True)

t_storico_documento.create(checkfirst=True)
