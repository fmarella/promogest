#-*- coding: utf-8 -*-
#
# Promogest
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class TipoAliquotaIva(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= { }
        return  dic[k]

tipo_aliquota_iva=Table('tipo_aliquota_iva',
                            params['metadata'],
                            schema = params['mainSchema'],
                            autoload=True)
std_mapper = mapper(TipoAliquotaIva, tipo_aliquota_iva, order_by=tipo_aliquota_iva.c.id)

