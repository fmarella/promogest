# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class RecapitoSpedizione(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':recapitospedizione.c.id ==v}
        return  dic[k]

recapitospedizione=Table('recapito_spedizione',
                            params['metadata'],
                            schema = params['schema'],
                            autoload=True)

std_mapper = mapper(RecapitoSpedizione, recapitospedizione, properties={},
                                    order_by=recapitospedizione.c.id)
