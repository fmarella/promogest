# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.RigaMovimento import RigaMovimento, t_riga_movimento
from Dao import Dao

try:
    numerolottotemp = Table('numero_lotto_temp',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    numerolottotemp = Table('numero_lotto_temp', params['metadata'],
            Column('id', Integer, primary_key=True),
            Column('id_riga_movimento_vendita_temp', Integer,
                ForeignKey(fk_prefix + 'riga_movimento.id'), nullable=False),
            Column('lotto_temp', String(50), nullable=False),
            Column('data_lotto_temp', DateTime, nullable=True),
            schema=params["schema"])
    numerolottotemp.create(checkfirst=True)

class NumeroLottoTemp(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "lottoTemp":
            dic = {k: numerolottotemp.c.lotto_temp==v}
        elif k == "idRigaMovimentoVenditaTemp":
            dic = {k: numerolottotemp.c.id_riga_movimento_vendita_temp==v}
        return dic[k]

std_mapper = mapper(NumeroLottoTemp, numerolottotemp,
    properties={
        "rigamovventemp": relation(RigaMovimento,
            primaryjoin=(numerolottotemp.c.id_riga_movimento_vendita_temp==t_riga_movimento.c.id),
            backref="NLT"),
    },
    order_by=numerolottotemp.c.id)
