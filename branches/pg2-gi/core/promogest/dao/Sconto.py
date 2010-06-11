#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class Sconto(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        dic= {}
        return  dic[k]

sconto=Table('sconto',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
std_mapper = mapper(Sconto, sconto, order_by=sconto.c.id)