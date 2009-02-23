# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class CarattereStampa(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':caratteristampa.c.id ==v}
        return  dic[k]

caratteristampa=Table('caratteri_stampa', params['metadata'],schema = params['schema'],
                                                                        autoload=True)

std_mapper = mapper(CarattereStampa, caratteristampa, properties={},
                    order_by=caratteristampa.c.id)