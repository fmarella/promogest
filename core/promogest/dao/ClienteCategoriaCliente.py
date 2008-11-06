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
from promogest.dao.CategoriaCliente import CategoriaCliente

class ClienteCategoriaCliente(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {'idCliente' : cliente_categoria_cliente.c.id_cliente ==v}
        return  dic[k]

cliente_categoria_cliente=Table('cliente_categoria_cliente',
                        params['metadata'],
                        schema = params['schema'],
                        autoload=True)

std_mapper =mapper(ClienteCategoriaCliente, cliente_categoria_cliente,
            properties={
            #'cliente':relation(Cliente, backref='cliente_categoria_cliente'),
            'categoria_cliente':relation(CategoriaCliente, backref='cliente_categoria_cliente'),
            }, order_by=cliente_categoria_cliente.c.id_cliente)