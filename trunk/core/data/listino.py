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

class ListinoDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session = session
        self.schema = schema
        self.debug = debug


    def create(self):

        if self.schema:
            colId = Column('id', Integer,Sequence('listino_id_seq',schema=self.schema),nullable=False,unique=True)
        else:
            colId = Column('id', Integer,nullable=False)

        listinoTable = Table('listino', self.metadata,
                colId,
                Column('denominazione', String(200), nullable=False, primary_key=True),
                Column('descrizione', String(300), nullable=False),
                Column('data_listino', DateTime,default=func.now(), nullable=False, primary_key=True),
                Column('listino_attuale', Boolean, nullable=True),
                Column('visible', Boolean, default=0),
                schema=self.schema)
        try:
            #msg = "DROP SEQUENCE %s.listino_id_seq" %self.schema
            #DDL(msg).execute_at('before-create', listinoTable)
            msg = "CREATE SEQUENCE %s.listino_id_seq" %self.schema
            DDL(msg).execute_at('before-create', listinoTable)
        except:
            print "la relazione listino_id_seq esiste già"
        listinoTable.create(checkfirst=True)

    def alter(self, req=None, arg=None):
        pass
#Column('id', Integer,Sequence('listino_id_seq',schema=self.schema),nullable=False, unique=True),
