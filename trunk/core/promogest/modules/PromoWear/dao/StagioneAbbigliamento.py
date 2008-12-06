# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class StagioneAbbigliamento(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def filter_values(self,k,v):
        dic= {'id':stagioneabbigliamento.c.id ==v}
        return  dic[k]

stagioneabbigliamento=Table('stagione_abbigliamento',
    params['metadata'],
    schema = params['mainSchema'],
    autoload=True)

std_mapper = mapper(StagioneAbbigliamento, stagioneabbigliamento, properties={},
                order_by=stagioneabbigliamento.c.id)