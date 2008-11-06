#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class StatoArticolo(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {}
        return  dic[k]

stato_articolo=Table('stato_articolo',
                        params['metadata'],
                        schema = params['mainSchema'],
                        autoload=True)
std_mapper = mapper(StatoArticolo, stato_articolo, order_by=stato_articolo.c.id)



