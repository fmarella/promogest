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

class TestataMovimentoDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.mainSchema= mainSchema
        self.debug = debug

    def create(self):
        #import pdb
        #pdb.set_trace()
        opTable = Table('operazione',self.metadata, autoload=True, schema=self.mainSchema)
        tdTable = Table('testata_documento',self.metadata, autoload=True, schema=self.schema)
        clTable = Table('cliente',self.metadata, autoload=True, schema=self.schema)
        foTable = Table('fornitore',self.metadata, autoload=True, schema=self.schema)
        if self.schema:
            testatadocumentoFK = self.schema+'.testata_documento.id'
            clienteFK = self.schema+'.cliente.id'
            fornitoreFK = self.schema+'.fornitore.id'
        else:
            testatadocumentoFK = 'testata_documento.id'
            clienteFK = 'cliente.id'
            fornitoreFK = 'fornitore.id'
        if self.mainSchema:
            operazioneFK = self.mainSchema+'.operazione.denominazione'
        else:
            operazioneFK = "operazione.denominazione"

        testataMovimentoTable = Table('testata_movimento', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('numero', Integer, nullable=False),
                Column('parte', Integer, nullable=True, default=1),
                Column('registro_numerazione', String(50), nullable=False),
                Column('operazione', String(100),ForeignKey(operazioneFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True ),
                Column('data_movimento',DateTime,PassiveDefault(func.now()), nullable=True),
                Column('data_inserimento',DateTime,PassiveDefault(func.now()), nullable=True),
                Column('note_interne', Text, nullable=True),
                Column('note_pie_pagina', String(200), nullable=True),
                #chiavi esterne
                Column('id_testata_documento', Integer,ForeignKey(testatadocumentoFK,onupdate="CASCADE",ondelete="CASCADE"), nullable=True),
                Column('id_cliente', Integer,ForeignKey(clienteFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
                Column('id_fornitore', Integer,ForeignKey(fornitoreFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
                UniqueConstraint('parte', 'numero', 'data_movimento'),
                CheckConstraint("parte < 4 AND parte >= 1"),
                schema=self.schema
                )
        testataMovimentoTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
