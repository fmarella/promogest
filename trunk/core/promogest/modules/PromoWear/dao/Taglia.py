# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


class Taglia(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=="id":
            dic= {k: taglia.c.id ==v}
        elif k == "denominazioneBreve":
            dic = {k:taglia.c.denominazione_breve == v }
        return  dic[k]


    #@property
    #def numero_ordine(self):
        #if self.GTTTAG:
            #print "LISTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", self.GTTTAG
            #return 1
        #else: return 1

taglia=Table('taglia', params['metadata'],schema = params['schema'],autoload=True)


std_mapper = mapper(Taglia, taglia,order_by=taglia.c.denominazione)
