# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class CategoriaFornitore(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'denominazione' : categoria_fornitore.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

categoria_fornitore=Table('categoria_fornitore',
                        params['metadata'],
                        schema = params['schema'],
                        autoload=True)

std_mapper = mapper(CategoriaFornitore,categoria_fornitore)