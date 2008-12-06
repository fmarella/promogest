#-*- coding: utf-8 -*-

"""
 Promogest - promoCMS
 Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
 license: GPL see LICENSE file
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from TipoRecapito import TipoRecapito
#from promogest.dao.Contatto import Contatto
from Dao import Dao

class RecapitoContatto(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def filter_values(self, k,v):
        dic= {'id':recapito.c.id_contatto==v,
            'idContatto':recapito.c.id_contatto==v}
        return  dic[k]

recapito=Table('recapito',
        params['metadata'],
        autoload=True,
        schema = params['schema'])

std_mapper = mapper(RecapitoContatto, recapito,properties={
    'tipo_reca':relation(TipoRecapito, backref='recapito')
    }, order_by=recapito.c.id)



