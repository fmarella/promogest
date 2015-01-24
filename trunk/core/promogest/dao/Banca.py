# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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
from promogest.dao.Dao import Dao, Base
from sqlalchemy.schema import *
from sqlalchemy.types import *


def gen_banca():
    banks = Banca().select(offset=None, batchSize=None)
    for b in banks:
        if b.agenzia:
            yield (b, b.id, ("{0} ({1})".format(b.denominazione, b.agenzia)))
        else:
            yield (b, b.id, ("{0}".format(b.denominazione)))

class Banca(Base, Dao):
    try:
        __table__ = Table('banca',
                      params['metadata'],
                      schema=params['schema'],
                      autoload=True)
    except:
        from data.banca import t_banca
        __table__ = t_banca

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= {  k : Banca.__table__.c.denominazione.ilike("%"+v+"%")}
        elif k == 'iban':
            dic = {k: Banca.__table__.c.iban.ilike("%"+v+"%")}
        elif k == 'abi':
            dic = {k: Banca.__table__.c.abi.ilike("%"+v+"%")}
        elif k == 'cab':
            dic = {k: Banca.__table__.c.cab.ilike("%"+v+"%")}
        elif k == 'bic_swift':
            dic = {k: Banca.__table__.c.bic_swift.ilike('%' + v + '%')}
        elif k == 'agenzia':
            dic = {k:Banca.__table__.c.agenzia.ilike("%"+v+"%")}
        return  dic[k]
