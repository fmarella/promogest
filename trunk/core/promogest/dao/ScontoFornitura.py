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

class ScontoFornitura(Dao):
    """  """
    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def filter_values(self,k,v):
        dic= {'idFornitura' : sconto_fornitura.c.id_fornitura ==v}
        return  dic[k]

sconto_fornitura=Table('sconto_fornitura',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper = mapper(ScontoFornitura, sconto_fornitura, order_by=sconto_fornitura.c.id)




