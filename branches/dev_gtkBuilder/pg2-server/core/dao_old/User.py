# -*- coding: utf-8 -*-

"""
 # Promogest - Janas
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""
import hashlib
from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao
from core.dao.Language import Language
from core.dao.Role import Role
#from core.modules.MultiLingua.dao.UserLanguage import UserLanguage

app_table = Table('app_log', params['metadata'],
    Column('id', Integer, primary_key=True),
    Column('id_utente', Integer),
    Column('utentedb', String(100), nullable=False),
    Column('schema_azienda', String(100), nullable=False),
    Column('level', String(1)),
    Column('object', PickleType, nullable=True),
    Column('message', String(1000), nullable=True),
    Column('value', Integer, nullable=True),
    Column('registration_date', DateTime),
    schema=params['mainSchema'])

app_table.create(checkfirst=True)

if params["tipo_db"] == "sqlite":
    role = 'role.id'
    language = 'language.id'
else:
    role = params['mainSchema']+'.role.id'
    language= params['mainSchema']+'.language.id'


roleTable = Table('role',params['metadata'], autoload=True, schema = params['mainSchema'])
languageTable = Table('language', params['metadata'], autoload=True, schema = params['mainSchema'])
userTable = Table('utente', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('username', String(50), nullable=False),
        Column('password', String(50), nullable=False),
        Column('email', String(70), nullable=True),
        Column('registration_date', DateTime,PassiveDefault(func.now())),
        Column('last_modified', DateTime, onupdate=func.current_timestamp()),
        Column('photo_src', String(150), nullable=True),
        Column('id_role', Integer, ForeignKey(role,onupdate="CASCADE",ondelete="RESTRICT")),
        Column('active', Boolean, default=False),
        Column('schemaa_azienda', String(100), nullable=True),
        Column('tipo_user', String(50), nullable=True),
        Column('url', String(200), nullable=True),
        Column('id_language', Integer,ForeignKey(language)),
        schema = params['mainSchema']
        )
userTable.create(checkfirst=True)
s= select([userTable.c.username]).execute().fetchall()
if (u'admin',) not in s or s==[]:
    user = userTable.insert()
    username ='admin'
    password = 'futur0'
    passwd =hashlib.md5(username+password).hexdigest()
    user.execute(username='admin', password=passwd, email='tes@tes.it', id_role = 1,tipo_user="WEB", active=True)
#import di dao esterni

from core.dao.PersonaGiuridica import PersonaGiuridica_



class User(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self,req=None):
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
        if self.username == "admin":
            print "TENTATIVO DI MODIFICA ADMIN L'EVENTO VERRA' REGISTRATO E SEGNALATO "
            return False
        else:
            params["session"].add(self)
            params["session"].commit()
            return True

    @property
    def company(self):
        if self.company: return self.company.ensign
        else: return ""

    if hasattr(conf, "RuoliAzioni") and getattr(conf.RuoliAzioni,'mod_enable')=="yes":
        @property
        def ruolo(self):
            if self.role: return self.role.name
            else: return ""

    if hasattr(conf, "MultiLingua") and getattr(conf.MultiLingua,'mod_enable')=="yes":
        @property
        def lingua(self):
            if self.userlang: return self.userlang.lan.denominazione
            else: return ""

user=Table('utente',params['metadata'],schema = params['mainSchema'],autoload=True)
std_mapper = mapper(User,user, properties={
        "per_giu" :relation(PersonaGiuridica_, backref='cliente_'),
        }, order_by=user.c.username)

#std_mapper = mapper(User, user, order_by=user.c.username)
std_mapper.add_property("role",relation(Role,primaryjoin=(user.c.id_role==Role.id),backref="users",uselist=False))

#if hasattr(conf, "MultiLingua") and getattr(conf.MultiLingua,'mod_enable')=="yes":
std_mapper.add_property("userlang",relation(Language,primaryjoin=(user.c.id_language==Language.id),backref="users",uselist=False))

