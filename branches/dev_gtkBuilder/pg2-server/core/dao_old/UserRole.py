# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2007-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
# Licenza: GNU GPLv2

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from core.Environment import params
from core.dao.Dao import Dao
from Software import Software
from SoftwareCategory import SoftwareCategory
#from core.dao.User import User

softwareTable = Table('software', params['metadata'], autoload=True, schema=params['schema'])
categoriaContattoTable = Table('software_category', params['metadata'], autoload=True, schema=params['schema'])

if self.schema:
    softwareFK = params['schema']+'.software.id'
    softwarecategoryFK = params['schema']'.software_category.id'
else:
    softwareFK = 'software.id'
    softwarecategoryFK = 'software_category.id'

contattoCategoriaContattoTable = Table('contatto_categoria_contatto', self.metadata,
        Column('id_contatto',Integer,ForeignKey(contattoFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
        Column('id_categoria_contatto',Integer,ForeignKey(categoriacontattoFK,onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
        schema=self.schema
        )
contattoCategoriaContattoTable.create(checkfirst=True)



class SoftwareCaterorySoftware(Dao):
    """ RoleAction class database functions  """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_role':
            dic = {k:userrole.c.id_role == v}
        elif k == 'idUser':
            dic = {k:userrole.c.id_user == v}
        return  dic[k]

userrole=Table('userrole',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)
std_mapper = mapper(UserRole, userrole, properties={
            'rol':relation(Role, backref='userrole'),
            #'use':relation(User, backref='userrole'),
                }, order_by=userrole.c.id_role)



