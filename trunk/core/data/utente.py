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
import datetime
from sqlalchemy import *
from promogest.Environment import *

t_utente = Table('utente', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('username', String(50), nullable=False),
        Column('password', String(50), nullable=False),
        Column('email', String(70), nullable=True),
        Column('registration_date', DateTime,ColumnDefault(datetime.datetime.now)),
        Column('last_modified', DateTime),
        Column('photo_src', String(150), nullable=True),
        Column('id_role', Integer, ForeignKey(fk_prefix_main+'role.id',onupdate="CASCADE",ondelete="RESTRICT")),
        Column('active', Boolean, default=False),
        Column('schemaa_azienda', String(100), ForeignKey(fk_prefix_main+'azienda.schemaa'), nullable=True),
        Column('tipo_user', String(50), nullable=True),
        Column('id_language', Integer,ForeignKey(fk_prefix_main+'language.id')),
        Column('email_confirmed', Boolean, default=False),
        Column('privacy', Boolean, default=False),
        Column('mailing_list', Boolean, default=False),
        schema=params["mainSchema"],
        )
t_utente.create(checkfirst=True)

s= select([t_utente.c.username]).execute().fetchall()
if (u'admin',) not in s or s==[]:
    user = t_utente.insert()
    username ='admin'
    password = 'admin'
    passwd =md5.new(username+password).hexdigest()
    user.execute(username='admin', password=passwd, email='tes@tes.it', id_role = 1,tipo_user="GTK", active=True)
