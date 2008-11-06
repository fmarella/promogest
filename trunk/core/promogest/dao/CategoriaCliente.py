# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao


class CategoriaCliente(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self, k,v):
        dic= {'denominazione' : categoria_cliente.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

categoria_cliente=Table('categoria_cliente',
                    params['metadata'],
                    schema = params['schema'],
                    autoload=True)

std_mapper = mapper(CategoriaCliente,categoria_cliente, order_by=categoria_cliente.c.id)




