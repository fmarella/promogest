#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Pinna Marco (Dr_astico) <zoccolodignu@gmail.com>
 License: GNU GPLv2
 """
 
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class ScontoVenditaIngrosso(Dao):
    """  """
    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {'idListino' : sconti_vendita_Ingrosso.c.id_listino_articolo ==v}
        return  dic[k]

sconto_fornitura=Table('sconti_vendita_ingrosso',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper = mapper(ScontoVenditaIngrosso, sconti_vendita_Ingrosso, order_by=sconti_vendita_ingrosso.c.id)
