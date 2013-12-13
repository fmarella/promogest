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

t_contatto = Table('contatto', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('tipo_contatto', String(50),primary_key=True),
            Column('nome',String(200), nullable=True),
            Column('cognome',String(200), nullable=True),
            Column('ruolo',String(200), nullable=True),
            Column('descrizione',String(300), nullable=True),
            Column('note',Text, nullable=True),
            UniqueConstraint('id'),
            CheckConstraint("(tipo_contatto = 'cliente') OR (tipo_contatto = 'fornitore') OR (tipo_contatto = 'magazzino') OR (tipo_contatto = 'azienda') OR (tipo_contatto = 'generico')"),
            schema=params["schema"]
            )
t_contatto.create(checkfirst=True)
