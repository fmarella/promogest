# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
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
from promogest.lib.migrate import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.User import User, user

#userTable = Table('utente', params['metadata'], autoload=True, schema=params['mainSchema'])
pagamentoTable = Table('pagamento',params['metadata'], autoload=True, schema=params['schema'])
articleTable = Table('articolo',params['metadata'], autoload=True, schema=params['schema'])
#clienteTable = Table('cliente',params['metadata'], autoload=True, schema=params['schema'])


try:
    cart=Table('cart', params['metadata'],schema = params['schema'],autoload=True)

    if 'id_cliente' not in [c.name for c in cart.columns]:
        col = Column('id_cliente', Integer, nullable=True)
        col.create(cart)


except:
    if params["tipo_db"] == "sqlite":
        utenteFK = 'utente.id'
        pagamentoFK = 'pagamento.id'
        articleFK = 'articolo.id'
    else:
        utenteFK = params['mainSchema']+'.utente.id'
        pagamentoFK = params["schema"] +'.pagamento.id'
        articleFK = params["schema"] +'.articolo.id'

    cart = Table('cart', params['metadata'],
            Column('id', Integer, primary_key=True),
            Column('id_articolo',Integer, ForeignKey(self.schema+'.articolo.id')),
            Column('quantita', Integer, nullable=True),
            Column('id_utente', Integer, ForeignKey(self.mainSchema+'.utente.id')),
            Column('data_inserimento',DateTime, nullable=True),
            Column('data_conferma',DateTime, nullable=True),
            Column('sessionid',String(50), nullable=True),
            Column('id_pagamento', Integer, ForeignKey(self.schema+'.pagamento.id')),
            Column('id_cliente', Integer),
            schema=self.schema
            )
    cart.create(checkfirst=True)

class Cart(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)


    def filter_values(self, k,v):
        if k == "idArticolo":
            dic= { k : cart.c.id_articolo==v}
        elif k == "sessionid":
            dic= { k : cart.c.sessionid == v}
        elif k == "idUser":
            dic= { k : cart.c.id_user == v}
        elif k == "idCliente":
            dic= { k : cart.c.id_cliente == v}
        return  dic[k]


std_mapper = mapper(Cart, cart, properties={
            'user' : relation(User,primaryjoin=
                    cart.c.id_utente==user.c.id,
                    foreign_keys=[user.c.id], backref="cart"),
                }, order_by=cart.c.id)
