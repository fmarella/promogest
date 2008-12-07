# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class CategoriaContatto(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'denominazione' : categoria_contatto.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

categoria_contatto=Table('categoria_contatto',
                    params['metadata'],
                    schema = params['schema'],
                    autoload=True)

std_mapper = mapper(CategoriaContatto,categoria_contatto, order_by=categoria_contatto.c.id)

