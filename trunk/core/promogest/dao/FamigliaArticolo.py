# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class FamigliaArticolo(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= {k : famiglia.c.denominazione.ilike("%"+v+"%")}
        elif k == "idPadre":
            dic= {k : famiglia.c.id_padre == v}
        elif k == "codice":
            dic= {k : famiglia.c.codice == v}
        elif k == "denominazioneBreve":
            dic= {k : famiglia.c.denominazione_breve.ilike("%"+v+"%")}
        return  dic[k]

    def fathers(self):
        ok = params['session'].query(FamigliaArticolo).filter(and_(FamigliaArticolo.id_padre==None)).all()
        return ok

famiglia=Table('famiglia_articolo', params['metadata'], schema = params['schema'], autoload=True)
#std_mapper = mapper(FamigliaArticolo,famiglia,order_by=famiglia.c.id_padre)

std_mapper = mapper(FamigliaArticolo, famiglia, properties={
    'children': relation(FamigliaArticolo, backref=backref('parent', remote_side=[famiglia.c.id]))
},order_by=famiglia.c.id_padre)




