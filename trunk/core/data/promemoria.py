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

class PromemoriaDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.debug = debug

    def create(self):

        promemoriaTable = Table('promemoria', self.metadata,
                Column('id',Integer,primary_key=True),
                Column('data_inserimento',DateTime,PassiveDefault(func.now()),nullable=False),
                Column('data_scadenza',DateTime,nullable=False),
                Column('oggetto',String(100),nullable=False),
                Column('incaricato',String(100),nullable=True),
                Column('autore',String(100),nullable=True),
                Column('descrizione',Text,nullable=True),
                Column('annotazione',Text,nullable=True),
                Column('riferimento',String(50),nullable=True),
                Column('giorni_preavviso',Integer,nullable=False, default=0),
                Column('in_scadenza',Boolean,nullable=False, default=False),
                Column('scaduto',Boolean,nullable=False, default=False),
                Column('completato',Boolean,nullable=False, default=False),
                schema=self.schema
                )
        promemoriaTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
