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

class StoccaggioDb(object):

    def __init__(self, schema = None, mainSchema=None,metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.debug = debug

    def create(self):
        azTable = Table('articolo', self.metadata, autoload=True, schema=self.schema)
        ffTable = Table('magazzino', self.metadata, autoload=True, schema=self.schema)

        if self.schema:
            articoloFK = self.schema+'.articolo.id'
            magazzinoFK = self.schema+'.magazzino.id'
        else:
            articoloFK = 'articolo.id'
            magazzinoFK = 'magazzino.id'

        stoccaggioTable = Table('stoccaggio', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('scorta_minima', Integer, nullable=True),
                Column('livello_riordino', Integer, nullable=True),
                Column('data_fine_scorte', DateTime,nullable=True),
                Column('data_prossimo_ordine', DateTime, nullable=True),
                Column('id_articolo', Integer,ForeignKey(articoloFK,onupdate="CASCADE",ondelete="CASCADE"), nullable=True),
                Column('id_magazzino', Integer, ForeignKey(magazzinoFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=False),
                schema=self.schema
                )
        stoccaggioTable.create(checkfirst=True)

    def alter(self, req=None, arg=None):
        pass
