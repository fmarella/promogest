# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>

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
from promogest.dao.Dao import Dao
from promogest.lib.migrate import *


try:
    t_provvigione = Table('provvigione', params['metadata'],
                         schema=params['schema'], autoload=True)
except:

    t_provvigione = Table(
        'provvigione',
        params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('valore_provv',  Numeric(16,4), nullable=True),
        Column('tipo_provv', String(10), nullable=True),
        schema=params['schema'],
        useexisting=True,
        )
    t_provvigione.create(checkfirst=True)


class Provvigione(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'id':
            dic = {k: t_provvigione.c.id==v}
        return dic[k]



std_mapper = mapper(Provvigione, t_provvigione,
                    order_by=t_provvigione.c.id)
