# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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
#from promogest.lib.migrate import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.User import User, t_utente
try:
    t_cart=Table('cart', params['metadata'], schema=params['schema'], autoload=True)
except:
    from data.cart import t_cart

class Cart(Dao):

    def __init__(self, req=None, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "idArticolo":
            dic = {k: t_cart.c.id_articolo == v}
        elif k == "sessionid":
            dic = {k: t_cart.c.sessionid == v}
        elif k == "idUser":
            dic = {k: t_cart.c.id_user == v}
        elif k == "idCliente":
            dic = {k: t_cart.c.id_cliente == v}
        return  dic[k]


std_mapper = mapper(Cart, t_cart, properties={
            #'user': relation(User,
                    #primaryjoin=t_cart.c.id_utente == t_utente.c.id,
                    #foreign_keys=[t_utente.c.id], backref="cart"),
                }, order_by=t_cart.c.id)
