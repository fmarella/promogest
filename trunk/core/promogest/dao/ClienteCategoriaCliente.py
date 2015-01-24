# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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
from promogest.dao.Dao import Dao, Base
from promogest.dao.CategoriaCliente import CategoriaCliente

class ClienteCategoriaCliente(Base, Dao):
    try:
        __table__ = Table('cliente_categoria_cliente',
                        params['metadata'],
                        schema = params['schema'],
                        autoload=True)
    except:
        from data.clienteCategoriaCliente import t_cliente_categoria_cliente
        __table__ = t_cliente_categoria_cliente

    __mapper_args__ = {
        'order_by' : "id_cliente"
    }

    categoria_cliente = relationship("CategoriaCliente", backref="cliente_categoria_cliente")

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k =='idCliente':
            dic= {k : ClienteCategoriaCliente.__table__.c.id_cliente ==v}
        elif k =='idCategoriaList':
            dic= {k : ClienteCategoriaCliente.__table__.c.id_categoria_cliente.in_(v)}
        return  dic[k]
