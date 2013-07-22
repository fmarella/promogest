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

t_aliquota_iva = Table('aliquota_iva', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('id_tipo',
                Integer,
                    ForeignKey(fk_prefix_main + "tipo_aliquota_iva.id",
                    onupdate="CASCADE",
                    ondelete="RESTRICT"),
                nullable=False),
        Column('denominazione_breve', String(10), nullable=False, unique=True),
        Column('denominazione', String(300), nullable=False,unique=True),
        Column('percentuale', Numeric(8,4), nullable=False),
        Column('percentuale_detrazione', Numeric(8,4), nullable=True),
        Column('descrizione_detrazione', String(100), nullable=True),
        schema=params["schema"]
        )
t_aliquota_iva.create(checkfirst=True)
