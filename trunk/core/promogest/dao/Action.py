# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class Action(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {  'denominazione' : action.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

action=Table('action',
            params['metadata'],
            schema = params['mainSchema'],
            autoload=True)

std_mapper = mapper(Action, action, order_by=action.c.id)