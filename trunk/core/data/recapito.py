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

class RecapitoDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.mainSchema= mainSchema
        self.debug = debug

    def create(self):
        cccTable = Table('contatto', self.metadata, autoload=True, schema=self.schema)
        trTable = Table('tipo_recapito', self.metadata, autoload=True, schema=self.mainSchema)
        if self.mainSchema:
            tiporecapitoFK = self.mainSchema+'.tipo_recapito.denominazione'
        else:
            tiporecapitoFK = 'tipo_recapito.denominazione'
        if self.schema:
            contattoFK = self.schema+'.contatto.id'
        else:
            contattoFK = 'contatto.id'

        recapitoTable = Table('recapito', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('recapito', String(450), nullable=False),
                Column('tipo_recapito',String(100),ForeignKey(tiporecapitoFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=False),
                Column('id_contatto',Integer ,ForeignKey(contattoFK,onupdate="CASCADE",ondelete="CASCADE"),nullable=False),
                #ForeignKeyConstraint(['id_contatto'],[self.schema+'.contatto.id'],onupdate="CASCADE", ondelete="CASCADE"),
                schema=self.schema
                )
        recapitoTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
