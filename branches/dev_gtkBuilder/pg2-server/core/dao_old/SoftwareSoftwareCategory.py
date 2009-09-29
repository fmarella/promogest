# -*- coding: utf-8 -*-

# Promogest -Janas
#
# Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
# Licenza: GNU GPLv2

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
    def __init__(self, arg=None):
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



