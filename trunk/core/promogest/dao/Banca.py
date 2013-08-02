# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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


from sqlalchemy import Table
from sqlalchemy.orm import mapper
from promogest.Environment import params, delete_pickle
from Dao import Dao
from promogest.lib.migrate import *
from sqlalchemy.schema import Column
from sqlalchemy.types import String

try:
    t_banca = Table('banca',
                      params['metadata'],
                      schema=params['schema'],
                      autoload=True)
except:
    from data.banca import t_banca


def gen_banca():
    banks = Banca().select(offset=None, batchSize=None)
    for b in banks:
        if b.agenzia:
            yield (b, b.id, ("{0} ({1})".format(b.denominazione, b.agenzia)))
        else:
            yield (b, b.id, ("{0}".format(b.denominazione)))

class Banca(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= {  k : t_banca.c.denominazione.ilike("%"+v+"%")}
        elif k == 'iban':
            dic = {k: t_banca.c.iban.ilike("%"+v+"%")}
        elif k == 'abi':
            dic = {k: t_banca.c.abi.ilike("%"+v+"%")}
        elif k == 'cab':
            dic = {k: t_banca.c.cab.ilike("%"+v+"%")}
        elif k == 'bic_swift':
            dic = {k: t_banca.c.bic_swift.ilike('%' + v + '%')}
        elif k == 'agenzia':
            dic = {k:t_banca.c.agenzia.ilike("%"+v+"%")}
        return  dic[k]



#if 'bic_swift' not in [c.name for c in t_banca.columns]:
    #delete_pickle()
    #col = Column('bic_swift', String(200))
    #col.create(t_banca, populate_default=True)

std_mapper = mapper(Banca, t_banca, order_by=t_banca.c.id)
