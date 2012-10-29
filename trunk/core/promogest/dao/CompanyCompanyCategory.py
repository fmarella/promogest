# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

companyTable = Table('company', params['metadata'], autoload=True, schema=params['schema'])
categoriaCompanyTable = Table('category', params['metadata'], autoload=True, schema=params['schema'])

companycompanycategoryTable = Table('company_company_category', params['metadata'],
        Column('id_company',Integer,ForeignKey(fk_prefix + "company.id",onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
        Column('id_company_category',Integer,ForeignKey(fk_prefix + "category.id",onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
        schema=params['schema']
        )
companycompanycategoryTable.create(checkfirst=True)

class CompanyCategoryCompany(Dao):
    """ RoleAction class database functions  """
    def __init__(self, req=None):
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
