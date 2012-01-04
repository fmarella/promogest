# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import params
from promogest.dao.Dao import Dao
from Language import Language
from promogest.dao.User import User

class UserLanguage(Dao):
    """ RoleAction class database functions  """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idLanguage':
            dic = {k:userlanguage.c.id_language == v}
        elif k == 'idUser':
            dic = {k:userlanguage.c.id_user == v}
        return  dic[k]

userlanguage=Table('userlanguage',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)
std_mapper = mapper(UserLanguage, userlanguage, properties={
            'lan':relation(Language, backref='userlanguage'),
            #'use':relation(User, backref='userrole'),
                }, order_by=userlanguage.c.id_language)



