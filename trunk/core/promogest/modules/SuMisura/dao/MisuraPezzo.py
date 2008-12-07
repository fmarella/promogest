# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2008 by Promotux Informatica - http://www.promotux.it/
# Author: francesco  <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class MisuraPezzo(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'idRiga' : misurapezzo.c.id_riga ==v}
        return  dic[k]

misurapezzo=Table('misura_pezzo',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

std_mapper = mapper(MisuraPezzo, misurapezzo, properties={}, order_by=misurapezzo.c.id)
