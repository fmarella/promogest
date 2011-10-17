# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from CategoriaCliente import CategoriaCliente

class ListinoCategoriaCliente(Dao):

    def __init__(self, req=None):
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




