# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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
from Dao import Dao
from promogest.dao.AliquotaIva import AliquotaIva
from migrate import *


class Pagamento(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "denominazione":
            dic= {k : pagamento.c.denominazione.ilike("%"+v+"%")}
        elif k == "tipo":
            dic= {k : pagamento.c.tipo == v} # cassa o banca
        return  dic[k]

    @property
    def aliquota_iva(self):
        dao = AliquotaIva().getRecord(self.id_aliquota_iva)
        if dao:
            return dao.denominazione_breve
        else:
            return ''
    #aliquota_iva = property(_aliquota_iva)

    @property
    def perc_aliquota_iva(self):
        dao = AliquotaIva().getRecord(self.id_aliquota_iva)
        if dao:
            return dao.percentuale
        else:
            return 0

pagamento = Table('pagamento',
                  params['metadata'],
                  schema = params['schema'],
                  autoload=True)

if 'tipo' not in [c.name for c in pagamento.columns]:
    col = Column('tipo', String, default='banca')
    col.create(pagamento, populate_default=True)

if 'spese' not in [c.name for c in pagamento.columns]:
    col = Column('spese', Numeric(16, 4), nullable=True)
    col.create(pagamento, populate_default=True)

if 'id_aliquota_iva' not in [c.name for c in pagamento.columns]:
    col = Column('id_aliquota_iva', Integer, nullable=True)
    col.create(pagamento, populate_default=True)

std_mapper = mapper(Pagamento, pagamento, order_by=pagamento.c.id)