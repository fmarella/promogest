#-*- coding: utf-8 -*-
#
"""
 # Promogest - Janas
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao

class Pagamento(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'denominazione' : pagamento.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

pagamento=Table('pagamento',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper = mapper(Pagamento, pagamento, order_by=pagamento.c.id)