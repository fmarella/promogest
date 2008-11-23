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
from Sconto import Sconto

class ScontoVenditaDettaglio(Dao):
    """  """
    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        if k == 'idListino':
            dic= {k : sconti_vendita_dettaglio.c.id_listino ==v}
        elif k == 'idArticolo':
            dic = {k:sconti_vendita_dettaglio.c.id_articolo ==v}
        elif k == 'dataListinoArticolo':
            dic = {k:sconti_vendita_dettaglio.c.data_listino_articolo==v}
        return  dic[k]
        
sconto=Table('sconto', params['metadata'],schema = params['schema'],autoload=True)

sconti_vendita_dettaglio=Table('sconti_vendita_dettaglio',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

j = join(sconto, sconti_vendita_dettaglio)

std_mapper = mapper(ScontoVenditaDettaglio,j, properties={
                    "id" : [sconto.c.id, sconti_vendita_dettaglio.c.id]},
                    order_by=sconti_vendita_dettaglio.c.id)
