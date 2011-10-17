# -*- coding: utf-8 -*-

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

class Imballaggio(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'denominazione' : imballaggio.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

imballaggio=Table('imballaggio',params['metadata'],schema = params['schema'],
                                                                autoload=True)

std_mapper = mapper(Imballaggio,imballaggio)
