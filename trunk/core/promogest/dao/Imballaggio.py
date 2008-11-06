# -*- coding: utf-8 -*-

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

class Imballaggio(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {  'denominazione' : imballaggio.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

imballaggio=Table('imballaggio',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

std_mapper = mapper(Imballaggio,imballaggio)