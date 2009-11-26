# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


class Colore(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        dic= {'id': colore.c.id ==v,
            "denominazione": colore.c.denominazione==v}
        return  dic[k]

colore=Table('colore',
           params['metadata'],
           schema = params['schema'],
           autoload=True)

std_mapper = mapper(Colore, colore, properties={},
        order_by=colore.c.denominazione)
