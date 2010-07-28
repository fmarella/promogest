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

class CategoriaArticolo(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= {k : categoria_articolo.c.denominazione.ilike("%"+v+"%")}
        elif k == "denominazioneBreve":
            dic= {k : categoria_articolo.c.denominazione_breve.ilike("%"+v+"%")}
        elif k == "denominazioneBreveEM":
            dic= {k : categoria_articolo.c.denominazione_breve == v}
        return  dic[k]

categoria_articolo=Table('categoria_articolo',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(CategoriaArticolo, categoria_articolo, order_by=categoria_articolo.c.id)



