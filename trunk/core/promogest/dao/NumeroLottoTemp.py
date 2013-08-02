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
from sqlalchemy.orm import *
from promogest.Environment import *

try:
    t_numero_lotto_temp = Table('numero_lotto_temp',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    from data.numerolottotemp import t_numero_lotto_temp

from Dao import Dao
from promogest.dao.RigaMovimento import RigaMovimento, t_riga_movimento




class NumeroLottoTemp(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "lottoTemp":
            dic = {k: t_numero_lotto_temp.c.lotto_temp==v}
        elif k == "idRigaMovimentoVenditaTemp":
            dic = {k: t_numero_lotto_temp.c.id_riga_movimento_vendita_temp==v}
        return dic[k]

std_mapper = mapper(NumeroLottoTemp, t_numero_lotto_temp,
    properties={
        "rigamovventemp": relation(RigaMovimento,
            primaryjoin=(t_numero_lotto_temp.c.id_riga_movimento_vendita_temp==t_riga_movimento.c.id),
            backref="NLT"),
    },
    order_by=t_numero_lotto_temp.c.id)
