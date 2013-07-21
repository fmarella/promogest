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
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>."

from sqlalchemy import *

class CartDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.mainSchema = mainSchema
        self.debug = debug

    def create(self):
        pagamentoTable = Table('pagamento',self.metadata, autoload=True, schema=self.schema)
        articleTable = Table('articolo',self.metadata, autoload=True, schema=self.schema)
        userTable = Table('utente',self.metadata, autoload=True, schema=self.mainSchema)

        if self.schema:
            articoloFK = self.schema+'.articolo.id'
            pagamentoFK = self.schema+'.pagamento.id'
        else:
            articoloFK = 'articolo.id'
            pagamentoFK = 'pagamento.id'

        if self.mainSchema:
            utenteFK = self.mainSchema+'.utente.id'
        else:
            utenteFK = 'utente.id'

        cartTable = Table('cart', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('id_articolo',Integer, ForeignKey(articoloFK)),
                Column('quantita', Integer, nullable=True),
                Column('id_utente', Integer, ForeignKey(utenteFK)),
                Column('data_inserimento',DateTime, nullable=True),
                Column('data_conferma',DateTime, nullable=True),
                Column('sessionid',String(50), nullable=True),
                Column('id_pagamento', Integer, ForeignKey(pagamentoFK)),
                schema=self.schema
                )
        cartTable.create(checkfirst=True)
