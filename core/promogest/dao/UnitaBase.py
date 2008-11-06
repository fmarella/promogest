# -*- coding: utf-8 -*-

# Promogest
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class UnitaBase(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {'denominazione' : unitabase.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

unitabase=Table('unita_base',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)

std_mapper = mapper(UnitaBase,unitabase)



