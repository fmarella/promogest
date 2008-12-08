# -*- coding: utf-8 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import params, host, database
from Dao import Dao
from Role import Role
from Language import Language

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
        elif k == 'role':
            dic = {k:user.c.id_role == v}
        elif k == 'active':
            dic = {k:user.c.active == v}
        return  dic[k]

    def _ruolo(self):
        if self.role: return self.role.name
        else: return ""
    ruolo = property(_ruolo)

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
        if self.username == "admin" and host=="db.promotux.it" and database == "promogest_demo":
            print "TENTATIVO DI MODIFICA ADMIN L'EVENTO VERRA' REGISTRATO E SEGNALATO "
            return False
        else:
            params["session"].add(self)
            params["session"].commit()
            return True


user=Table('utente', params['metadata'],
    schema = params['mainSchema'],
    autoload=True)

std_mapper = mapper(User, user, properties={
    "role":relation(Role,primaryjoin=
            user.c.id_role==Role.id),
    'lang':relation(Language, primaryjoin=
            user.c.id_language==Language.id)
        }, order_by=user.c.username)
