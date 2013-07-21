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

class ImageDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.debug = debug


    def create(self):
        famiglia_articoloTable = Table('famiglia_articolo',self.metadata, autoload=True, schema=self.schema)
        if self.schema:
            famigliaFK = self.schema+'.famiglia_articolo.id'
        else:
            famigliaFK = 'famiglia_articolo.id'


        imageTable = Table('image', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('filename', String(300), nullable=True),
                Column('id_famiglia',Integer, ForeignKey(famigliaFK,onupdate="CASCADE",ondelete="RESTRICT")),
                schema=self.schema)
        self.metadata.create_all(checkfirst=True)
