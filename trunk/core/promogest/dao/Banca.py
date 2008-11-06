# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class Banca(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {  'denominazione' : banca.c.denominazione.ilike("%"+v+"%"),
        'iban': banca.c.iban.ilike("%"+v+"%"),
        'agenzia':banca.c.agenzia.ilike("%"+v+"%")
                    }
        return  dic[k]

banca=Table('banca',
        params['metadata'],
        schema = params['schema'],
        autoload=True)
std_mapper = mapper(Banca,banca, order_by=banca.c.id)