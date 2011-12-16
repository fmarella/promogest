# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from promogest.Environment import params
from Dao import Dao
from migrate import *
from sqlalchemy.schema import Column
from sqlalchemy.types import String

class Banca(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= {  k : banca.c.denominazione.ilike("%"+v+"%")}
        elif k == 'iban':
            dic = {k: banca.c.iban.ilike("%"+v+"%")}
        elif k == 'abi':
            dic = {k: banca.c.abi.ilike("%"+v+"%")}
        elif k == 'cab':
            dic = {k: banca.c.cab.ilike("%"+v+"%")}
        elif k == 'bic_swift':
            dic = {k: banca.c.bic_swift.ilike('%' + v + '%')}
        elif k == 'agenzia':
            dic = {k:banca.c.agenzia.ilike("%"+v+"%")}
        return  dic[k]

banca=Table('banca',params['metadata'],schema = params['schema'],autoload=True)

if 'bic_swift' not in [c.name for c in banca.columns]:
    col = Column('bic_swift', String)
    col.create(banca, populate_default=True)

std_mapper = mapper(Banca,banca, order_by=banca.c.id)