# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params

from Dao import Dao

class AppLog(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k =="level":
            dic= {  k : appLogTable.c.level == v}
        elif k =="message":
            dic= {  k : appLogTable.c.message.contains(v)}
        return  dic[k]


appLogTable = Table('app_log', params['metadata'], autoload=True, schema=params['mainSchema'])
std_mapper = mapper(AppLog, appLogTable, properties={},order_by=appLogTable.c.id)
