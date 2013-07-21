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

class UnitaBaseDb(object):

    def __init__(self, schema = None, mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.mainSchema=mainSchema
        self.debug = debug

    def create(self):
        unita_baseTable = Table('unita_base', self.metadata,
                    Column('id', Integer, primary_key=True),
                    Column('denominazione_breve', String(50), nullable=True, unique=True),
                    Column('denominazione', String(200), nullable=True),
                    schema=self.mainSchema
                    )
        unita_baseTable.create(checkfirst=True)
        s= select([unita_baseTable.c.denominazione_breve]).execute().fetchall()
        if (u'pz',) not in s or s==[]:
            unit = unita_baseTable.insert()
            unit.execute(denominazione_breve='pz', denominazione='pezzi')
            unit.execute(denominazione_breve='m', denominazione='Metri')
            unit.execute(denominazione_breve='l', denominazione='Litri')
            unit.execute(denominazione_breve='kg', denominazione='Chilogrammi')
            unit.execute(denominazione_breve='N', denominazione='Numero')
            unit.execute(denominazione_breve='h', denominazione='Ore')
            unit.execute(denominazione_breve='mq', denominazione='Metri Quadri')


    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
