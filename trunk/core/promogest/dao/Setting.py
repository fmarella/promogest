#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class Setting(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def filter_values(self,k,v):
        dic= {  'keys' : setting.c.key.ilike("%"+v+"%"),
        'description':setting.c.description.ilike("%"+v+"%"),
                'value':setting.c.value == v}
        return  dic[k]

setting=Table('setting',
        params['metadata'],
        schema = params['schema'],
        autoload=True)
std_mapper = mapper(Setting, setting, order_by=setting.c.key)


