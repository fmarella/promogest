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
from Magazzino import Magazzino



class ListinoMagazzino(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _magazzino(self):
        if self.magazzin:
            mag = self.magazzin.denominazione
            return mag
        else:
            return ""
    magazzino = property(_magazzino)

    def filter_values(self,k,v):
        dic= {  'idListino' : listino_magazzino.c.id_listino ==v,
                'idMagazzino' : listino_magazzino.c.id_magazzino ==v}
        return  dic[k]

listino_magazzino = Table('listino_magazzino',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
std_mapper = mapper(ListinoMagazzino, listino_magazzino, properties={
        #"listino" : relation(Listino, backref="listino_magazzino"),
        "magazzin": relation(Magazzino, backref="listino_magazzino")
            }, order_by=listino_magazzino.c.id_listino)



