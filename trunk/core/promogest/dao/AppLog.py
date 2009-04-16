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

appLogTable = Table('app_log', params['metadata'], autoload=True, schema=params['mainSchema'])
std_mapper = mapper(AppLog, appLogTable, properties={},order_by=appLogTable.c.id)
