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
from Articolo import Articolo
from Multiplo import Multiplo
from Listino import Listino

class Riga(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=='descrizione':
            dic= {  k : riga.c.descrizione.ilike("%"+v+"%")}
        elif k=="id_articolo":
            dic={k:riga.c.id_articolo==v}
        return  dic[k]

riga=Table('riga',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

std_mapper = mapper(Riga, riga, properties={}, order_by=riga.c.id)


