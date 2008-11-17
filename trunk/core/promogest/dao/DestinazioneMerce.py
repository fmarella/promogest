# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class DestinazioneMerce(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        if k=='idCliente':
            dic= {k:destinazione_merce.c.id_cliente==v}
        elif k == 'denominazione':
            dic ={k:destinazione_merce.c.denominazione.ilike("%"+v+"%")}
        elif k== 'indirizzo':
            dic = {k:destinazione_merce.c.indirizzo.ilike("%"+v+"%")}
        elif k=='localita':
            dic = {k:destinazione_merce.c.localita.ilike("%"+v+"%")}
        elif k == 'provincia':
            dic = {k:destinazione_merce.c.provincia.ilike("%"+v+"%")}
        return  dic[k]

destinazione_merce=Table('destinazione_merce',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper = mapper(DestinazioneMerce,destinazione_merce, order_by=destinazione_merce.c.id)
