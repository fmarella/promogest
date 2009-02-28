# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import params, host, database, conf
from Dao import Dao
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

    #def _ruolo(self):
        #if self.role: return self.role.name
        #else: return ""
    #ruolo = property(_ruolo)

    def _language(self):
        if self.lang: return self.lang.denominazione
        else: return ""
    lingua = property(_language)

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
    if hasattr(conf, "RuoliAzioni") and getattr(conf.RuoliAzioni,'mod_enable')=="yes":

        @property
        def ruolo(self):
            if self.useroles: return self.useroles.rol.name
            else: return ""




user=Table('utente', params['metadata'],
    schema = params['mainSchema'],
    autoload=True)

std_mapper = mapper(User, user, properties={
    #'lang':relation(Language, primaryjoin=
            #user.c.id_language==Language.id)
        }, order_by=user.c.username)
if hasattr(conf, "RuoliAzioni") and getattr(conf.RuoliAzioni,'mod_enable')=="yes":
    from promogest.modules.RuoliAzioni.dao.UserRole import UserRole
    std_mapper.add_property("useroles",relation(UserRole,primaryjoin=(user.c.id==UserRole.id_user),backref="users",uselist=False))

