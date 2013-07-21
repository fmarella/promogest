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

class MultiploDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.mainSchema = mainSchema
        self.debug = debug


    def create(self):
        unita_baseTable = Table('unita_base', self.metadata, autoload=True, schema=self.mainSchema)
        articleTable = Table('articolo', self.metadata, autoload=True, schema=self.schema)

        if self.schema:
            articoloFK = self.schema+'.articolo.id'
        else:
            articoloFK = 'articolo.id'
        if self.mainSchema:
            unitabaseFK = self.mainSchema+'.unita_base.id'
        else:
            unitabaseFK = 'unita_base.id'

        self.multiploTable = Table('multiplo', self.metadata,
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(50),nullable=False),
                Column('denominazione',String(200),nullable=False),
                Column('id_unita_base',Integer,ForeignKey(unitabaseFK, onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_articolo',Integer,ForeignKey(articoloFK, onupdate="CASCADE", ondelete="RESTRICT")),
                Column('moltiplicatore',Numeric(15,6),nullable=False),
                UniqueConstraint('denominazione', 'denominazione_breve'),
                CheckConstraint("id_unita_base IS NULL AND id_articolo IS NOT NULL  OR  id_unita_base IS NOT NULL  AND id_articolo IS NULL"),
                schema=self.schema
                )
        self.multiploTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
