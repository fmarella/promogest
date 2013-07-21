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

class FamilyArticleDb(object):
    """famiglia_articolo - Tabella famiglie articolo
    """
    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.debug = debug

    def create(self):

        if self.schema:
            famigliaFK = self.schema+'.famiglia_articolo.id'
        else:
            famigliaFK = 'famiglia_articolo.id'

        famiglia_articoloTable = Table('famiglia_articolo', self.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('codice', String(10), nullable=False, unique=True),
                    Column('denominazione_breve', String(10), nullable=False),
                    Column('denominazione', String(200), nullable=False),
                    Column('visible', Boolean, default=0),
                    Column('id_padre', Integer,ForeignKey(famigliaFK)),
                    schema=self.schema
                    )
        famiglia_articoloTable.create(checkfirst=True)

    def alter(self, req=None, arg=None):
        pass
