# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class GruppoTagliaTaglia(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {'id':gruppotagliataglia.c.id ==v}
        return  dic[k]

gruppotagliataglia=Table('gruppo_taglia_taglia',
           params['metadata'],
           schema = params['schema'],
           autoload=True)

std_mapper = mapper(GruppoTagliaTaglia, gruppotagliataglia, properties={},
        order_by=gruppotagliataglia.c.id_gruppo_taglia)