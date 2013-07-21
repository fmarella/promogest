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
from sqlalchemy.orm import *
from promogest.

class AccessDb(object):
    """
    create and drop single and all  tables
    """
    def __init__(self, schema = None, mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.mainSchema = mainSchema
        self.debug = debug


    def create(self):
        userTable = Table('utente',self.metadata, autoload=True, schema=self.mainSchema)

        if self.mainSchema:
            utenteFK = self.mainSchema+'.utente.id'
        else:
            utenteFK = 'utente.id'

        accessTable = Table('access', self.metadata,
                Column('id',Integer,primary_key=True),
                Column('id_user',Integer,ForeignKey(utenteFK,onupdate="CASCADE",ondelete="CASCADE")),
                Column('login', Date, nullable=True),
                Column('logout', Date, nullable=True),
                schema=self.schema
                )
        accessTable.create(checkfirst=True)
