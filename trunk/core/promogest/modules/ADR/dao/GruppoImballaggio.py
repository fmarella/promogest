# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>

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
    gruppo_imballaggio = Table('gruppo_imballaggio', params['metadata'], schema = params['schema'],autoload=True)

except:
    gruppo_imballaggio = Table('gruppo_imballaggio', params["metadata"],
            Column('id',Integer, primary_key=True),
            Column('denominazione', String(10)),
            schema = params['schema'])

    gruppo_imballaggio.create(checkfirst=True)


class GruppoImballaggio(Dao):

    def __init__(self, req= None, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione': gruppo_imballaggio.c.denominazione == v,
                }
        return  dic[k]

std_mapper = mapper(GruppoImballaggio, gruppo_imballaggio, order_by=gruppo_imballaggio.c.denominazione)

_imballaggi = ["I", "II", "III"]

f = GruppoImballaggio().select(denominazione="I")
if not f:
    for p in _imballaggi:
        a = GruppoImballaggio()
        a.denominazione = p
        session.add(a)
    session.commit()
