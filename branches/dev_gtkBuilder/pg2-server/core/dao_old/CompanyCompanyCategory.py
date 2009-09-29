# -*- coding: utf-8 -*-

# Promogest - Janas
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

companyTable = Table('company', params['metadata'], autoload=True, schema=params['schema'])
categoriaCompanyTable = Table('category', params['metadata'], autoload=True, schema=params['schema'])

if tipo_db == "sqlite":
    companyFK = 'company.id'
    companycategoryFK = 'category.id'
else:
    companyFK = params['schema']+'.company.id'
    companycategoryFK = params['schema']+'.category.id'


companycompanycategoryTable = Table('company_company_category', params['metadata'],
        Column('id_company',Integer,ForeignKey(companyFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
        Column('id_company_category',Integer,ForeignKey(companycategoryFK,onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
        schema=params['schema']
        )
companycompanycategoryTable.create(checkfirst=True)

class CompanyCategoryCompany(Dao):
    """ RoleAction class database functions  """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_company':
            dic = {k:compcompcat.c.id_company == v}
        elif k == 'id_company_category':
            dic = {k:compcompcat.c.id_company_category == v}
        return  dic[k]


compcompcat=Table('company_company_category',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)
std_mapper = mapper(CompanyCategoryCompany, compcompcat, properties={
            #'software':relation(Software, backref='sw_sw_cat'),
            #'categoria':relation(SoftwareCategory, backref='sw_sw_cat'),
                }, order_by=compcompcat.c.id_company)



