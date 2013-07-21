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

class TestataScontrinoDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.debug = debug

    def create(self):
        testataMovimentoTable = Table('testata_movimento', self.metadata, autoload=True, schema=self.schema)
        if self.schema:
            testatamovimentoFK = self.schema+'.testata_movimento.id'
        else:
            "testata_movimento.id"
        self.testataScontrinoTable = Table('testata_scontrino', self.metadata,
                Column('id',Integer,primary_key=True),
                Column('data_inserimento',DateTime,PassiveDefault(func.now()),nullable=False),
                Column('totale_scontrino',Numeric(16,4),nullable=False),
                Column('totale_contanti',Numeric(16,4),nullable=False),
                Column('totale_assegni',Numeric(16,4),nullable=False),
                Column('totale_carta_credito',Numeric(16,4),nullable=False),
                #chiavi esterne
                Column('id_testata_movimento',Integer,ForeignKey(testatamovimentoFK, onupdate="CASCADE", ondelete="RESTRICT")),
                schema=self.schema
                )
        self.testataScontrinoTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
