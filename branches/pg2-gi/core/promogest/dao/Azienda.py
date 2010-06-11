#-*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import Table
from sqlalchemy.orm import mapper
from promogest.Environment import params
from Dao import Dao

class Azienda(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        dic= {  'denominazione' : azienda.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

azienda=Table('azienda',
        params['metadata'],
        autoload=True,
        schema = params['mainSchema'])

std_mapper = mapper(Azienda, azienda, order_by=azienda.c.schemaa)


