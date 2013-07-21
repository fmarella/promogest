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

class PagesDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.mainSchema = mainSchema
        self.debug = debug


    def create(self):
        languageTable = Table('language', self.metadata, autoload=True, schema=self.mainSchema)
        userTable = Table('utente', self.metadata, autoload=True, schema=self.mainSchema)
        if self.mainSchema:
            utenteFK =self.mainSchema+'.utente.id'
            languageFK =self.mainSchema+'.language.id'
        else:
            utenteFK ='utente.id'
            languageFK = 'language.id'

        pagesTable= Table('static_page', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('title', String(200), nullable=True),
                Column('body', Text, nullable=True),
                Column('publication_date', Date, nullable=True),
                Column('id_user', Integer,ForeignKey(utenteFK)),
                Column('id_language', Integer,ForeignKey(languageFK)),
                schema=self.schema
                )
        pagesTable.create(checkfirst=True)
