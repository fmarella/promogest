# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import Table
from sqlalchemy.orm import mapper
from promogest.Environment import params
from Dao import Dao

class Banca(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= {  k : banca.c.denominazione.ilike("%"+v+"%")}
        elif k == 'iban':
            dic = {k: banca.c.iban.ilike("%"+v+"%")}
        elif k == 'agenzia':
            dic = {k:banca.c.agenzia.ilike("%"+v+"%")}
        return  dic[k]

banca=Table('banca',params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Banca,banca, order_by=banca.c.id)