# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from sqlalchemy.orm import mapper, relation,
try:
    from sqlalchemy.orm import relationship
except:
    print "AGGIORNARE SQLALCHEMY"
from promogest.Environment import *
from Dao import Dao
from Regioni import Regioni
from Province import Province
#if hasattr(conf, "RuoliAzioni") and getattr(conf.RuoliAzioni,'mod_enable')=="yes":
    #from promogest.modules.RuoliAzioni.dao.Role import Role
#from Language import Language

class User(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None):
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
        if hasattr(conf, "RuoliAzioni") and getattr(conf.RuoliAzioni,'mod_enable')=="yes":
            if k == 'idRole':
                dic = {k:and_(user.c.id==UserRole.id_user,UserRole.id_role == v)}
        return  dic[k]
    #if hasattr(conf, "RuoliAzioni") and getattr(conf.RuoliAzioni,'mod_enable')=="yes":
        #def _ruolo(self):
            #if self.role: return self.role.name
            #else: return ""
        #ruolo = property(_ruolo)

    #def _language(self):
        #if self.lang: return self.lang.denominazione
        #else: return ""
    #lingua = property(_language)

    def delete(self):
        if self.username == "admin":
            print "TENTATIVO DI CANCELLAZIONE ADMIN L'EVENTO VERRA' REGISTRATO "
            return False
        else:
            params['session'].delete(self)
            params["session"].commit()
            return True

    def persist(self):
        if self.username == "admin" and database == "promogest_demo":
            print "TENTATIVO DI MODIFICA ADMIN L'EVENTO VERRA' REGISTRATO E SEGNALATO "
            return False
        else:
            params["session"].add(self)
            params["session"].commit()
            return True

    if hasattr(conf, "RuoliAzioni") \
        and hasattr(conf.RuoliAzioni,"mod_enable") \
        and getattr(conf.RuoliAzioni,'mod_enable')=="yes":
        try:
            @property
            def ruolo(self):
                if self.role: return self.role.name
                else: return ""
        except:
            print " RUOLIAZIONI ANCORA PROBLEMI"

    if hasattr(conf, "MultiLingua") and getattr(conf.MultiLingua,'mod_enable')=="yes":
        @property
        def lingua(self):
            if self.userlang: return self.userlang.lan.denominazione
            else: return ""


user=Table('utente', params['metadata'],schema = params['mainSchema'],autoload=True)
std_mapper = mapper(User, user, order_by=user.c.username)

if hasattr(conf, "RuoliAzioni") \
        and hasattr(conf.RuoliAzioni,"mod_enable") \
        and getattr(conf.RuoliAzioni,'mod_enable')=="yes":
    try:
        from promogest.modules.RuoliAzioni.dao.Role import Role
        if tipodb =="sqlite":
            std_mapper.add_property("role",relationship(Role,primaryjoin=(user.c.id_role==Role.id),foreign_keys=[Role.id],backref="users",uselist=False))
        else:
            std_mapper.add_property("role",relationship(Role,primaryjoin=(user.c.id_role==Role.id),backref="users",uselist=False))
    except:
        print "ATTENZIONE!! RUOLI AZIONI NON È INSTALLATO CORRETTAMENTE"
if hasattr(conf, "MultiLingua") and getattr(conf.MultiLingua,'mod_enable')=="yes":
    from promogest.modules.MultiLingua.dao.UserLanguage import UserLanguage
    std_mapper.add_property("userlang",relation(UserLanguage,primaryjoin=(user.c.id==UserLanguage.id_user),backref="users",uselist=False))
