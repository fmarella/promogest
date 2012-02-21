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
from Dao import Dao
from Regioni import Regioni
from Province import Province
from migrate import *
from promogest.modules.RuoliAzioni.dao.Role import Role

user=Table('utente', params['metadata'],schema = params['mainSchema'],autoload=True)

if 'id_role' not in [c.name for c in user.columns]:
    col = Column('id_role', Integer, nullable=True)
    col.create(user)

try:
    from sqlalchemy.orm import relationship
    if tipodb =="sqlite":
        std_mapper.add_property("role",relationship(Role,
            primaryjoin=(user.c.id_role==Role.id),
                        foreign_keys=[Role.id],
                        backref="users",
                        uselist=False,
                        passive_deletes=True))
except:
    pg2log.info("AGGIORNARE SQLALCHEMY RUOLI NON FUNZIONERANNO")
if hasattr(conf, "MultiLingua") and getattr(conf.MultiLingua,'mod_enable')=="yes":
    from promogest.modules.MultiLingua.dao.UserLanguage import UserLanguage
    std_mapper.add_property("userlang",
            relation(UserLanguage,
                    primaryjoin=(user.c.id==UserLanguage.id_user),
                    backref="users",
                    uselist=False)
                    )


class User(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'username':
            dic = {k:user.c.username == v}
        elif k == 'password':
            dic = {k:user.c.password == v}
        elif k == 'usern':
            dic = {k:user.c.username.ilike("%"+v+"%")}
        elif k == 'email':
            dic = {k:user.c.email.ilike("%"+v+"%")}
        elif k == 'active':
            dic = {k:user.c.active == v}
        elif k == 'idRole':
            dic = {k:user.c.id_role == v}
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


    if hasattr(conf, "MultiLingua") and getattr(conf.MultiLingua,
                                                'mod_enable')=="yes":
        @property
        def lingua(self):
            if self.userlang: return self.userlang.lan.denominazione
            else: return ""

std_mapper = mapper(User, user, order_by=user.c.username)
