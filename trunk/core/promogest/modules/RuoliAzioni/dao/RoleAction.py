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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *


from promogest.dao.Dao import Dao, Base
from Role import Role
from Action import Action



class RoleAction(Base, Dao):
    """ RoleAction class database functions  """
    try:
        __table__ = Table('roleaction',
                meta,
                schema = mainSchema,
                autoload=True,
                autoload_with=engine)
    except:
        __table__ = Table('roleaction', params["metadata"],
            Column('id_role', Integer, ForeignKey(fk_prefix_main+'role.id'),primary_key=True),
            Column('id_action', Integer, ForeignKey(fk_prefix_main+'action.id'),primary_key=True),
            schema=params["mainSchema"]
                        )
    role = relationship("Role", backref="roleaction")
    action = relationship("Action", backref="roleaction")

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_role':
            dic = {k: RoleAction.__table__.c.id_role == v}
        elif k == 'id_action':
            dic = {k: RoleAction.__table__.c.id_action == v}
        return  dic[k]



#idAdmin = Role().select(name ="Admin")
#if not idAdmin:
    #print "ATTENZIONE NON e' PRESENTE UN ADMIN"
#else:
    #idadmin = idAdmin[0].id
    #idact = params["session"].query(Action.id).all()
    #idract = params["session"].query(RoleAction.id_action).filter_by(id_role=idadmin).all()
    #if idact != idract:
        #ac = Action().select(batchSize=None)
        #for a in ac:
            #ra = RoleAction().select(id_role=idadmin,id_action=a.id, batchSize=None)
            #if not ra:
                #aa = RoleAction()
                #aa.id_role = idadmin
                #aa.id_action = a.id
                #session.add(aa)
        #params["session"].commit()

##SERVER per eliminare una riga inutile ...ricordati di usare gli id
#aa = RoleAction().select(id_action=5, batchSize=None)
#if aa:
    #for a in aa:
        #a.delete()
#a = Action().getRecord(id=5)
#if a:
    #if a.denominazione_breve =="INSERIMENTO":
        #a.delete()
