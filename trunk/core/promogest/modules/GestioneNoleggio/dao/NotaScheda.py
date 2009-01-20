# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class NotaScheda(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':notascheda.c.id ==v}
        return  dic[k]

notascheda=Table('nota_scheda', params['metadata'], schema = params['schema'],
                                                                    autoload=True)

std_mapper = mapper(NotaScheda, notascheda, properties={},
                                order_by=notascheda.c.id)
