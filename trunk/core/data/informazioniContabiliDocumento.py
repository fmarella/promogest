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


t_informazioni_contabili_documento = Table('informazioni_contabili_documento', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('documento_saldato', Boolean, default=False),
        Column('id_documento',Integer,ForeignKey(fk_prefix+'testata_documento.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False, ),
        Column('id_primo_riferimento',Integer,ForeignKey(fk_prefix+'testata_documento.id',onupdate="CASCADE",ondelete="RESTRICT")),
        Column('id_secondo_riferimento',Integer,ForeignKey(fk_prefix+'testata_documento.id',onupdate="CASCADE",ondelete="RESTRICT")),
        Column('totale_pagato', Numeric(16,4), nullable=False, default=0),
        Column('totale_sospeso', Numeric(16,4), nullable=False, default=0),
        schema=params["schema"]
        )
t_informazioni_contabili_documento.create(checkfirst=True)
