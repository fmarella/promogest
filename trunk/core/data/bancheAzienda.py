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


t_banche_azienda = Table('banche_azienda',
        params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('id_banca', Integer),
        Column('id_azienda', String(100)),
        Column('id_persona_giuridica', Integer),
        Column('numero_conto', String(30)),
        Column('data_riporto', Date()),
        Column('valore_riporto', Numeric(16, 4)),
        Column('codice_sia', String(15)),
        Column('banca_predefinita', Boolean),
        UniqueConstraint('id_banca', 'numero_conto'),
        schema=params['schema'],
        useexisting=True)
t_banche_azienda.create(checkfirst=True)
