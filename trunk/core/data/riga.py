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

t_riga = Table('riga', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('valore_unitario_netto', Numeric(16,4), nullable=True),
        Column('valore_unitario_lordo', Numeric(16,4), nullable=True),
        Column('quantita', Numeric(16,4), nullable=True),
        Column('moltiplicatore', Numeric(16,4), nullable=True),
        Column('applicazione_sconti', String(20), nullable=True),
        Column('percentuale_iva', Numeric(8,4), nullable=False, default=0),
        Column('id_iva', Integer),
        Column('posizione', Integer),
        Column('id_riga_padre', Integer),
        Column('descrizione', String(500), nullable=True),
        #chiavi esterne
        Column('id_articolo',Integer,ForeignKey(fk_prefix+'articolo.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
        Column('id_magazzino',Integer,ForeignKey(fk_prefix+'magazzino.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
        Column('id_multiplo',Integer,ForeignKey(fk_prefix+'multiplo.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
        Column('id_listino',Integer,ForeignKey(fk_prefix+'listino.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
        schema=params["schema"]
        )
t_riga.create(checkfirst=True)
