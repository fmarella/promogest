# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class Taglia(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':colore.c.id ==v}
        return  dic[k]

taglia=Table('taglia',
           params['metadata'],
           schema = params['schema'],
           autoload=True)

std_mapper = mapper(Taglia, taglia, properties={},
        order_by=taglia.c.denominazione)
