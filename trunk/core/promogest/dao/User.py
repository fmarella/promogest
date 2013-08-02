# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import *

try:
    t_utente = Table('utente', params['metadata'],schema = params['mainSchema'],autoload=True)
except:
    from data.azienda import t_azienda
    from data.language import t_language
    from data.role import t_role
    from data.utente import t_utente

from promogest.dao.Dao import Dao
#from promogest.dao.Regioni import Regioni
#from promogest.dao.Province import Province
from migrate import *
from promogest.modules.RuoliAzioni.dao.Role import Role
from promogest.dao.DaoUtils import get_columns


class User(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'username':
            dic = {k:t_utente.c.username == v}
        elif k == 'password':
            dic = {k:t_utente.c.password == v}
        elif k == 'usern':
            dic = {k:t_utente.c.username.ilike("%"+v+"%")}
        elif k == 'email':
            dic = {k:t_utente.c.email.ilike("%"+v+"%")}
        elif k == 'active':
            dic = {k:t_utente.c.active == v}
        elif k == 'tipoUser':
            dic = {k:t_utente.c.tipo_user == v}
        elif k == 'idRole':
            dic = {k:t_utente.c.id_role == v}
        return  dic[k]


    def delete(self):
        if self.username == "admin":
            print "TENTATIVO DI CANCELLAZIONE ADMIN L'EVENTO VERRA' REGISTRATO "
            return False
        else:
            params['session'].delete(self)
            params["session"].commit()
            return True

    @property
    def ruolo(self):
        try:
            if self.role: return self.role.name
            else: return ""
        except:
            nome = Role().select(idRole=self.id_role)
            if nome:
                return nome[0].name or ""
            else:
                return ""


std_mapper = mapper(User, t_utente,
    properties={
        'email':deferred(t_utente.c.email),
        'registration_date':deferred(t_utente.c.registration_date),
        'last_modified':deferred(t_utente.c.last_modified),
        'photo_src':deferred(t_utente.c.photo_src),
        #'id_language':deferred(user.c.id_language),
        'schemaa_azienda':deferred(t_utente.c.schemaa_azienda),

}, order_by=t_utente.c.username)
