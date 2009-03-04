# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import gtk
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params
import datetime
from ChiaviPrimarieLog import ChiaviPrimarieLog
from Dao import Dao



class AppLog(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)
    #def store(self, dao=None,action=None,status=True,value=None ):
        #self.dao = dao
        #self.action = action
        #self.status = status
        #self.value = value
        ##print self.dao, dir(self.dao), self.dao.__repr__, self.dao.__class__.__name__,self.dao.__module__
        #self.saveToAppLog(dao=self.dao, action=self.action,status=self.status,
                            #value=self.value)


appLogTable = Table('app_log', params['metadata'], autoload=True, schema=params['mainSchema'])
std_mapper = mapper(AppLog, appLogTable, properties={
                "pk":relation(ChiaviPrimarieLog,primaryjoin=
                    ChiaviPrimarieLog.id_application_log2==appLogTable.c.id,
                    cascade="all, delete",
                    backref="app_log")},
                    order_by=appLogTable.c.id)
