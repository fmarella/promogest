#-*- coding: utf-8 -*-
#
# Promogest

# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from CategoriaCliente import CategoriaCliente

class ListinoCategoriaCliente(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _categoriaCliente(self):
        if self.catecli: return self.catecli.denominazione
        else: return ""
    categoria_cliente = property(_categoriaCliente)

    def filter_values(self,k,v):
        dic= {  'idListino' : listino_categoria_cliente.c.id_listino == v}
        return  dic[k]

listino_categoria_cliente=Table('listino_categoria_cliente',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper = mapper(ListinoCategoriaCliente, listino_categoria_cliente, properties={
        #"listino" : relation(Listino, backref="listino_categoria_cliente"),
        #"catecli":relation(CategoriaCliente,primaryjoin=
                        #(listino_categoria_cliente.c.id_categoria_cliente==CategoriaCliente.id)),
        "catecli" : relation(CategoriaCliente, backref="listino_categoria_cliente")
        },
        order_by=listino_categoria_cliente.c.id_listino)




