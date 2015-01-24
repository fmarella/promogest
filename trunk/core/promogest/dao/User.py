# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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

import hashlib
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest import Environment
from promogest.dao.Dao import Dao, Base
from promogest.modules.RuoliAzioni.dao.Role import Role

class User(Base, Dao):
    """ User class provides to make a Users dao which include more used"""
    try:
        __table__ = Table('utente', meta,schema=mainSchema, autoload=True, autoload_with=engine)
    except:
        from data.utente import t_utente
        __table__ = t_utente


    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'username':
            dic = {k: User.__table__.c.username == v}
        elif k == 'password':
            dic = {k: User.__table__.c.password == v}
        elif k == 'usern':
            dic = {k: User.__table__.c.username.ilike("%"+v+"%")}
        elif k == 'email':
            dic = {k: User.__table__.c.email.ilike("%"+v+"%")}
        elif k == 'emailEM':
            dic = {k: User.__table__.c.email == v}
        elif k == 'active':
            dic = {k: User.__table__.c.active == v}
        elif k == 'tipoUser':
            dic = {k: User.__table__.c.tipo_user == v}
        elif k == 'idRole':
            dic = {k: User.__table__.c.id_role == v}
        elif k == 'schemaAzienda':
            dic = {k: User.__table__.c.schemaa_azienda == v}
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

#try:
    #User.__table__.c.schemaa_azienda
#except:
    #conn = engine.connect()
    #ctx = MigrationContext.configure(conn)
    #op = Operations(ctx)
    #op.add_column('utente', Column('schemaa_azienda', String(100), ForeignKey(fk_prefix_main+'azienda.schemaa'), nullable=True), schema=mainSchema)
    #delete_pickle()
    #restart_program()

#s= select([User.__table__.c.username]).execute().fetchall()
#for nome in schemi_presenti:
    #if str("admin_"+str(nome)) not in str(s) and "__" not in nome and nome != "public" and nome!="promogest2" and nome !="information_schema":
        #from promogest.dao.Azienda import Azienda
        #aa = Azienda().getRecord(id=str(nome))
        #if aa:
            #user = User()
            #username ='admin_'+str(nome)
            #password = 'admin'
            #user.username = username
            #user.password =hashlib.md5(username+password).hexdigest()
            #user.email = 'tes@tes.it'
            #user.schemaa_azienda = str(nome)
            #user.id_role=1
            #user.tipo_user="WEB"
            #user.active = True
            #user.persist()
