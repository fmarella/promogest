# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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

from promogest.dao.Dao import Dao, Base
from promogest.dao.CategoriaCliente import CategoriaCliente

class ListinoCategoriaCliente(Base, Dao):
    try:
        __table__ = Table('listino_categoria_cliente',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
    except:
        from data.listinoCategoriaCliente import t_listino_categoria_cliente
        __table__ = t_listino_categoria_cliente

    __mapper_args__ = {
        'order_by' : "id_listino"
    }

    catecli = relationship(CategoriaCliente, backref="listino_categoria_cliente")

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    @property
    def categoria_cliente(self):
        if self.catecli: return self.catecli.denominazione
        else: return ""

    def filter_values(self,k,v):
        dic= {  'idListino' : ListinoCategoriaCliente.__table__.c.id_listino == v}
        return  dic[k]
