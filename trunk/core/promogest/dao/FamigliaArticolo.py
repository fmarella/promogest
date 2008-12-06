# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class FamigliaArticolo(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def filter_values(self,k,v):
        dic= {'denominazione' : famiglia.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

def get_node_depth(id):
    ret_index = 0
    dao = FamigliaArticolo().getRecord(id=id)
    while dao.id_padre is not None:
        dao = FamigliaArticolo().getRecord(id=dao.id_padre)
        ret_index +=1
    else:
        return ret_index

famiglia=Table('famiglia_articolo', params['metadata'], schema = params['schema'], autoload=True)
std_mapper = mapper(FamigliaArticolo,famiglia)



