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

class RigaCommessaDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.debug = debug

    def create(self):
        testatacommessaTable = Table('testata_commessa', self.metadata, autoload=True, schema=self.schema)


        if not self.schema:
            testatacommessaFK ='testata_commessa.id'

        else:
            testatacommessaFK = self.schema+'.testata_commessa.id'

        rigacommessa = Table('riga_commessa', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('numero', Integer, nullable=False),
                Column('denominazione', String(300), nullable=False),
                Column('id_testata_commessa', Integer,ForeignKey(testatacommessaFK,onupdate="CASCADE",ondelete="CASCADE")),
    #            Column('numero', Integer, nullable=False),
                Column('data_registrazione', DateTime, nullable=True),
                Column('dao_class', String(100), nullable=True),
                Column('note',Text,nullable=True),
                Column('id_dao', Integer, nullable=True),
                schema=self.schema,
                useexisting=True)
        rigacommessa.create(checkfirst=True)


    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
