#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class Pos(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'denominazione' : pos.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

pos=Table('pos',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(Pos, pos, order_by=pos.c.id)
