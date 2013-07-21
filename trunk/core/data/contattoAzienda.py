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

class ContattoAziendaDb(object):

    def __init__(self, schema = None, mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.mainSchema = mainSchema
        self.debug = debug

    def create(self):
        coTable = Table('contatto', self.metadata, autoload=True, schema=self.schema)
        azTable = Table('azienda', self.metadata, autoload=True, schema=self.mainSchema)
        if self.mainSchema:
            aziendaFK = self.mainSchema+'.azienda.schemaa'
            contattoFKid = self.schema+'.contatto.id'
            contattoFKtipo_contatto = self.schema+'.contatto.tipo_contatto'

        else:
            aziendaFK = 'azienda.schemaa'
            contattoFKid = 'contatto.id'
            contattoFKtipo_contatto = 'contatto.tipo_contatto'

        contattoAziendaTable = Table('contatto_azienda', self.metadata,
                Column('id',Integer,primary_key=True),
                Column('tipo_contatto',String(50),primary_key=True),
                Column('schema_azienda',String(100),ForeignKey(aziendaFK,onupdate="CASCADE",ondelete="RESTRICT"),nullable=False),
                ForeignKeyConstraint(['id', 'tipo_contatto'],[contattoFKid, contattoFKtipo_contatto],onupdate="CASCADE", ondelete="CASCADE"),
                CheckConstraint("tipo_contatto = 'azienda'"),
                schema=self.schema
                )
        contattoAziendaTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
