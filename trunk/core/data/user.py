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



import sys
import md5
from sqlalchemy import *

class UserDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.mainSchema=mainSchema
        self.debug = debug


    def create(self):
        roleTable = Table('role',self.metadata, autoload=True, schema=self.mainSchema)
        languageTable = Table('language', self.metadata, autoload=True, schema=self.mainSchema)
        if self.mainSchema:
            aziendaFK = self.mainSchema+'.azienda.schemaa'
        else:
            aziendaFK = 'azienda.schemaa'

        userTable = Table('utente', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('username', String(50), nullable=False),
                Column('password', String(50), nullable=False),
                Column('email', String(70), nullable=True),
                Column('registration_date', DateTime,PassiveDefault(func.now())),
                Column('last_modified', DateTime, onupdate=func.current_timestamp()),
                Column('photo_src', String(150), nullable=True),
                Column('id_role', Integer, ForeignKey(self.mainSchema+'.role.id',onupdate="CASCADE",ondelete="RESTRICT")),
                Column('active', Boolean, default=False),
                Column('schemaa_azienda', String(100), ForeignKey(aziendaFK), nullable=True),
                Column('tipo_user', String(50), nullable=True),
                Column('id_language', Integer,ForeignKey(self.mainSchema+'.language.id')),
                schema=self.mainSchema
                )
        userTable.create(checkfirst=True)
        s= select([userTable.c.username]).execute().fetchall()
        if (u'admin',) not in s or s==[]:
            user = userTable.insert()
            username ='admin'
            password = 'admin'
            passwd =md5.new(username+password).hexdigest()
            user.execute(username='admin', password=passwd, email='tes@tes.it', id_role = 1,tipo_user="pyGTK", active=True)
            #username1 = 'vendita'
            #password1 = 'vendita'
            #passwd1 =md5.new(username1+password1).hexdigest()
            #user.execute(username='vendita', password=passwd1, email='tes@tes.it', id_role = 2,tipo_user="pyGTK", active=True)
            #username2 = "magazzino"
            #password2 = "magazzino"
            #passwd2 = md5.new(username2+password2).hexdigest()
            #user.execute(username='magazzino', password=passwd2, email='tes@tes.it', id_role = 3,tipo_user="pyGTK", active=True)
            #username3 = "adminweb"
            #password3 = "adminweb"
            #passwd3 = md5.new(username3+password3).hexdigest()
            #user.execute(username='adminweb', password=passwd3, email='tes@tes.it', id_role = 1,tipo_user="web", active=True)
