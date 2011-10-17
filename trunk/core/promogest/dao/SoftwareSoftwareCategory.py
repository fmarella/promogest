# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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


from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from core.dao.Dao import Dao
#from Software import Software
#from SoftwareCategory import SoftwareCategory
#from core.dao.User import User

softwareTable = Table('software', params['metadata'], autoload=True, schema=params['schema'])
categoriaContattoTable = Table('software_category', params['metadata'], autoload=True, schema=params['schema'])

if tipo_db == "sqlite":
    softwareFK = 'software.id'
    softwarecategoryFK = 'software_category.id'
else:
    softwareFK = params['schema']+'.software.id'
    softwarecategoryFK = params['schema']+'.software_category.id'


sofwaresoftwarecategoryTable = Table('software_software_category', params['metadata'],
        Column('id_software',Integer,ForeignKey(softwareFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
        Column('id_software_category',Integer,ForeignKey(softwarecategoryFK,onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
        schema=params['schema']
        )
sofwaresoftwarecategoryTable.create(checkfirst=True)

class SoftwareCategorySoftware(Dao):
    """ RoleAction class database functions  """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_software':
            dic = {k:softwareswcat.c.id_software == v}
        elif k == 'id_software_category':
            dic = {k:softwareswcat.c.id_software_category == v}
        return  dic[k]


    #@property
    #def ruolo(self):
        #if self.role: return self.role.name
        #else: return ""

softwareswcat=Table('software_software_category',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)
std_mapper = mapper(SoftwareCategorySoftware, softwareswcat, properties={
            #'software':relation(Software, backref='sw_sw_cat'),
            #'categoria':relation(SoftwareCategory, backref='sw_sw_cat'),
                }, order_by=softwareswcat.c.id_software)



