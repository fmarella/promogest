#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
 """

from sqlalchemy import Table
from sqlalchemy.orm import mapper, join,relation
from promogest.Environment import params
#from Listino import Listino
from Dao import Dao

class ListinoComplessoListino(Dao):
    """  """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idListinoComplesso':
            dic= {k : listinocomplessolistino.c.id_listino_complesso ==v}
        elif k == 'idListino':
            dic = {k:listinocomplessolistino.c.id_listino==v}
        return  dic[k]

    def _listino(self):
        if self.listino: return self.listino.denominazione
        else: return ""
    listino_denominazione= property(_listino)

sconto=Table('sconto', params['metadata'],schema = params['schema'],autoload=True)

listinocomplessolistino=Table('listino_complesso_listino',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(ListinoComplessoListino,listinocomplessolistino, properties={
                                            },
                    order_by=listinocomplessolistino.c.id_listino_complesso)
