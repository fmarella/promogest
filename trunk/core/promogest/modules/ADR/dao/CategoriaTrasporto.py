# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@gmail.com>

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

try:
    categoriatrasporto = Table('categoria_trasporto', params['metadata'],
                               schema=params['schema'],
                               autoload=True)
except:
    categoriatrasporto = Table(
        'categoria_trasporto',
        params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('denominazione', String(200)),
        Column('quantita_massima_trasportabile', Numeric(16, 4)),
        Column('coefficiente_moltiplicazione_virtuale', Numeric(16, 4)),
        Column('note', Text),
        schema=params['schema'],
        )

    categoriatrasporto.create(checkfirst=True)


class CategoriaTrasporto(Dao):

    def __init__(self, req=None, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        dic = {
            'denominazione': categoriatrasporto.c.denominazione == v,
            'quantita_massima_trasportabile': categoriatrasporto.c.quantita_massima_trasportabile \
                == v,
            'coefficiente_moltiplicazione_virtuale': categoriatrasporto.c.coefficiente_moltiplicazione_virtuale \
                == v,
            'note': categoriatrasporto.c.note == v,
            }
        return dic[k]


std_mapper = mapper(CategoriaTrasporto, categoriatrasporto,
                    order_by=categoriatrasporto.c.denominazione)

_categorie = [
    ('0',    0, 999, ''),
    ('1',   20,  50, ''),
    ('2',  333,   3, ''),
    ('3', 1000,   1, ''),
    ('4', 9999,   0, ''),]

f = CategoriaTrasporto().select(denominazione="0")
if not f:
    for p in _categorie:
        a = CategoriaTrasporto()
        a.denominazione = p[0]
        a.quantita_massima_trasportabile = p[1]
        a.coefficiente_moltiplicazione_virtuale = p[2]
        a.note = p[3]
        session.add(a)
    session.commit()
