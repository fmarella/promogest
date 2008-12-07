# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class GenereAbbigliamento(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':genereabbigliamento.c.id ==v}
        return  dic[k]

genereabbigliamento=Table('genere_abbigliamento',
    params['metadata'],
    schema = params['mainSchema'],
    autoload=True)

std_mapper = mapper(GenereAbbigliamento, genereabbigliamento, properties={},
                order_by=genereabbigliamento.c.id)