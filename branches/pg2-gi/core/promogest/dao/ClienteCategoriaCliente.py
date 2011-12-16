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
from CategoriaCliente import CategoriaCliente

class ClienteCategoriaCliente(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k =='idCliente':
            dic= {k : cliente_categoria_cliente.c.id_cliente ==v}
        elif k =='idCategoriaList':
            dic= {k : cliente_categoria_cliente.c.id_categoria_cliente.in_(v)}
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