#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class Pagamento(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {'denominazione' : pagamento.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

pagamento=Table('pagamento',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper = mapper(Pagamento, pagamento, order_by=pagamento.c.id)