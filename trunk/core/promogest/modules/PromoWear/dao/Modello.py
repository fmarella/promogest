# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


class Modello(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k=="id":
            dic= {k: modello.c.id ==v}
        elif k =="denominazione":
            dic= {k: modello.c.denominazione == v}
        return  dic[k]

modello=Table('modello',
           params['metadata'],
           schema = params['schema'],
           autoload=True)

std_mapper = mapper(Modello, modello, properties={},
        order_by=modello.c.denominazione)
