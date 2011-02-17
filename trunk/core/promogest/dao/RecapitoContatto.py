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
from Dao import Dao

class RecapitoContatto(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        if k =="id":
            dic= {k:recapito.c.id_contatto==v}
        elif k =="idContatto":
            dic = {k:recapito.c.id_contatto==v}
        elif k =="tipoRecapito":
            dic = {k:recapito.c.tipo_recapito==v}
        return  dic[k]

recapito=Table('recapito',
        params['metadata'],
        autoload=True,
        schema = params['schema'])

std_mapper = mapper(RecapitoContatto, recapito,properties={
    'tipo_reca':relation(TipoRecapito, backref='recapito')
    }, order_by=recapito.c.id)
