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

class ContattoFornitoreDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.debug = debug

    def create(self):
        coTable = Table('contatto', self.metadata, autoload=True, schema=self.schema)
        azTable = Table('fornitore', self.metadata, autoload=True, schema=self.schema)

        if self.schema:
            contattoFKid =self.schema+'.contatto.id'
            fornitoreFK =self.schema+'.fornitore.id'
            contattoFKtipocontatto = self.schema+'.contatto.tipo_contatto'
        else:
            contattoFKid ='contatto.id'
            fornitoreFK = 'fornitore.id'
            contattoFKtipocontatto = 'contatto.tipo_contatto'



        contattoFornitoreTable = Table('contatto_fornitore', self.metadata,
                Column('id',Integer,primary_key=True),#ForeignKey(self.schema+'.contatto.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                Column('tipo_contatto',String(50),primary_key=True),#ForeignKey(self.schema+'.contatto.tipo_contatto',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True,default="fornitore"),
                Column('id_fornitore',Integer,ForeignKey(fornitoreFK,onupdate="CASCADE",ondelete="RESTRICT"),nullable=False),
                ForeignKeyConstraint(['id', 'tipo_contatto'],[contattoFKid, contattoFKtipocontatto],onupdate="CASCADE", ondelete="CASCADE"),
                CheckConstraint("tipo_contatto = 'fornitore'"),
                schema=self.schema
                )
        contattoFornitoreTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
