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
from Listino import Listino
from ListinoArticolo import ListinoArticolo
from Dao import Dao

class ListinoComplessoArticoloPrevalente(Dao):
    """  """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idListinoComplesso':
            dic= {k : listinocomplessoarticoloprevalente.c.id_listino_complesso ==v}
        elif k == 'idListino':
            dic = {k:listinocomplessoarticoloprevalente.c.id_listino==v}
        elif k == 'idArticolo':
            dic = {k:listinocomplessoarticoloprevalente.c.id_articolo ==v}
        elif k == 'dataListinoArticolo':
            dic = {k:listinocomplessoarticoloprevalente.c.data_listino_articolo==v}
        return  dic[k]


listinocomplessoarticoloprevalente=Table('listino_complesso_articolo_prevalente',
                                        params['metadata'],
                                        schema = params['schema'],
                                        autoload=True)

std_mapper = mapper(ListinoComplessoArticoloPrevalente,listinocomplessoarticoloprevalente, properties={
                                            },
                    order_by=listinocomplessoarticoloprevalente.c.id_listino_complesso)
