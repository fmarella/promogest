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
        if k == "id":
            dic= {k:recapitospedizione.c.id ==v}
        elif k== "idScheda":
            dic= {k:recapitospedizione.c.id_scheda==v}
        return  dic[k]

recapitospedizione=Table('recapito_spedizione',
                            params['metadata'],
                            schema = params['schema'],
                            autoload=True)

std_mapper = mapper(RecapitoSpedizione, recapitospedizione, order_by=recapitospedizione.c.id)
