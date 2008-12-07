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
from TipoAliquotaIva import TipoAliquotaIva

class AliquotaIva(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        if k=='denominazione':
            dic= { k: aliquota_iva.c.denominazione.ilike("%"+v+"%")}
        elif k == "percentuale":
            dic= { k: aliquota_iva.c.percentuale == v}
        return  dic[k]

aliquota_iva = Table('aliquota_iva',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(AliquotaIva,aliquota_iva, properties={
        'tipo_aliquota_iva':relation(TipoAliquotaIva, backref='aliquota_iva')
            }, order_by=aliquota_iva.c.id)


