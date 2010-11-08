#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from migrate import *


class Pagamento(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "denominazione":
            dic= {k : pagamento.c.denominazione.ilike("%"+v+"%")}
        elif k == "tipo":
            dic= {k : pagamento.c.tipo == v} # cassa o banca
        return  dic[k]

pagamento=Table('pagamento',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

if "tipo" not in [c.name for c in pagamento.columns]:
    col = Column('tipo', String, default='banca')
    col.create(pagamento, populate_default=True)

std_mapper = mapper(Pagamento, pagamento, order_by=pagamento.c.id)
