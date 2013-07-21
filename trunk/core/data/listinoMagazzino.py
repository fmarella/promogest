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

class ListinoMagazzinoDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.debug = debug

    def create(self):
        listinoTable = Table('listino', self.metadata, autoload=True, schema=self.schema)
        magazzinoTable = Table('magazzino', self.metadata, autoload=True, schema=self.schema)

        if self.schema:
            listinoFK = self.schema+'.listino.id'
            magazzinoFK = self.schema+'.magazzino.id'
        else:
            listinoFK = 'listino.id'
            magazzinoFK = 'magazzino.id'

        listinoMagazzinoTable = Table('listino_magazzino', self.metadata,
                Column('id_listino',Integer,ForeignKey(listinoFK,onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
                Column('id_magazzino',Integer,ForeignKey(magazzinoFK,onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
                schema=self.schema
                )
        listinoMagazzinoTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
