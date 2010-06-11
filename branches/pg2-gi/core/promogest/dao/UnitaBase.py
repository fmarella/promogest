# -*- coding: utf-8 -*-

# Promogest
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class UnitaBase(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)
        self.addMC()
    def filter_values(self,k,v):
        dic= {'denominazione' : unitabase.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

    def addMC(self):
        mc = self.select(denominazione ="Metri Cubi")
        if not mc:
            self.denominazione_breve = "mc"
            self.denominazione = "Metri Cubi"
            self.persist()

unitabase=Table('unita_base',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)

std_mapper = mapper(UnitaBase,unitabase)



