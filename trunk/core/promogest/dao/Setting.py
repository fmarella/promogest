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

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=='keys':
            dic= {  k : setting.c.key.ilike("%"+v+"%")}
        elif k == 'description':
            dic = {k:setting.c.description.ilike("%"+v+"%")}
        elif k == 'value':
            dic = {k:setting.c.value == v}
        return  dic[k]

setting=Table('setting',params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Setting, setting, order_by=setting.c.key)


