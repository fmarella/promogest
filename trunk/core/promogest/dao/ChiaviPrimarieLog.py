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
#from CategoriaCliente import CategoriaCliente

class ChiaviPrimarieLog(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'idAppLog' : chiaviprimarielog.c.id_application_log2 ==v}
        return  dic[k]

chiaviprimarielog=Table('chiavi_primarie_log',
                        params['metadata'],
                        schema = params['mainSchema'],
                        autoload=True)

std_mapper =mapper(ChiaviPrimarieLog, chiaviprimarielog,
            properties={
            #'cliente':relation(Cliente, backref='cliente_categoria_cliente'),
            #'categoria_cliente':relation(CategoriaCliente, backref='cliente_categoria_cliente'),
            }, order_by=chiaviprimarielog.c.id)
