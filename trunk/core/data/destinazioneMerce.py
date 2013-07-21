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

class DestinazioneMerceDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.debug = debug

    def create(self):
#        clienteTable = Table('cliente', self.metadata, autoload=True, schema=self.schema)

        if self.schema:
            clienteFK = self.schema+'.cliente.id'
        else:
            clienteFK = 'cliente.id'

        destinazioneMerceTable = Table('destinazione_merce', self.metadata,
                Column('id',Integer,primary_key=True),
                Column('denominazione',String(200),nullable=False),
                Column('indirizzo',String(200),nullable=True),
                Column('localita',String(100),nullable=True),
                Column('cap',String(10),nullable=True),
                Column('provincia',String(50),nullable=True),
                Column('id_cliente',Integer,ForeignKey(clienteFK,onupdate="CASCADE",ondelete="RESTRICT")),
                schema=self.schema
                )
        destinazioneMerceTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
