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
from UnitaBase import UnitaBase
from Articolo import Articolo
from Dao import Dao

class Multiplo(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {  'idArticolo' : multiplo.c.id_articolo== v,
                'idUnitaBase' : multiplo.c.id_unita_base == v,
                'denominazione': multiplo.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

    def _unitabase(self):
        if self.uniba:  return self.uniba.denominazione
        else: return ""
    unita_base = property(_unitabase)

    def _articolo(self):
        if self.arti: return self.arti.denominazione
        else: return ""
    articolo = property(_articolo)

multiplo=Table('multiplo',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

std_mapper = mapper(Multiplo, multiplo, properties={
    "uniba":relation(UnitaBase,primaryjoin=multiplo.c.id_unita_base==UnitaBase.id),
    "arti":relation(Articolo,primaryjoin=multiplo.c.id_articolo==Articolo.id)
        }, order_by=multiplo.c.id)
