#-*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
#from promogest.dao.Category import Category
from promogest.modules.Multilingua.dao.Language import Language
from promogest.dao.User import User

#languageTable = Table('language', params['metadata'], autoload=True, schema=params['mainSchema'])
#user = Table('utente', params['metadata'], autoload=True, schema=params['mainSchema'])

#if params["tipo_db"] == "sqlite":
#    utenteFK ='utente.id'
#    languageFK = 'language.id'

#else:
#    utenteFK =params['mainSchema']+'.utente.id'
#    languageFK =params['mainSchema']+'.language.id'


#companyTableTable = Table('company', params['metadata'],
#        Column('id', Integer, primary_key=True),
#        Column('social', String(100), nullable=False),
#        Column('ensign', String(100), nullable=True),
#        Column('firstname', String(100), nullable=False),
#        Column('lastname', String(100), nullable=False),
#        Column('iva', String(11), nullable=True),
#        Column('fiscalcode', String(16), nullable=True),
#        Column('address', String(100), nullable=False),
#        Column('cap', String(5), nullable=False),
#        Column('city', String(5), nullable=False),
#        Column('telephone', String(20), nullable=True),
#        Column('mobile', String(20), nullable=True),
#        Column('description', Text, nullable=False),
#        Column('url', String(200), nullable=True),
#        Column('email', String(100), nullable=False),
#        Column('option_number', Integer, nullable=False),
#        Column('id_user', Integer,ForeignKey(utenteFK, onupdate="CASCADE",ondelete="RESTRICT"), nullable=False),
#        Column('id_language', Integer,ForeignKey(languageFK)),
#        Column('insert_date', DateTime, nullable=True),
#        Column('active', Boolean, default=0),
#        Column('imagepath', String(400), nullable=True),
#        Column('province', String(11), nullable=True),
#        Column('abstract', String(500), nullable=True),
#        Column('clicks', Integer, default=0),
#        UniqueConstraint('fiscalcode', 'address', 'city'),
#        schema=params['schema'],
#        useexisting =True
#)
#companyTableTable.create(checkfirst=True)

#from core.dao.CompanyCompanyCategory import CompanyCategoryCompany

class Company(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self,req=None, arg=None):
        Dao.__init__(self, entity=self)
        self.__dbcategorie = []
        self.__categorie = []

    @reconstructor
    def init_on_load(self):
        self.__dbcategorie = []
        self.__categorie = []

    def filter_values(self, k,v):
        if k == "description":
            dic= { k : company.c.description.ilike("%"+v+"%")}
        elif k == "denominationEM":
            dic= { k : or_(company.c.ensign == v,
                            company.c.social == v,
                            company.c.lastname == v)
}
        elif k =="active":
            dic = { k :company.c.active ==v}
        return  dic[k]

    def categorieDel(self, id=None):
        """
        Cancella le categorie
        """
        row = CompanyCategoryCompany().select(id_company= id,
                                                offset = None,
                                                batchSize = None,
                                                )
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
            return True

    def persist(self):
        params["session"].add(self)
        params["session"].commit()
        if self.__categorie:
            self.categorieDel(self.id)
            for cat in self.__categorie:
                compacat = CompanyCategoryCompany()
                compacat.id_company = self.id
                compacat.id_company_category = int(cat)
                params["session"].add(compacat)
            params["session"].commit()
                    #softcat.persist()

company=Table('azienda',
        params['metadata'],
        autoload=True,
        schema = params['mainSchema'])

std_mapper = mapper(Company, company, properties={
#        'lang' : relation(Language),
#        'user' : relation(User, backref="azienda"),
#        'categ': relation(CompanyCategoryCompany,primaryjoin = company.c.id==CompanyCategoryCompany.id_company,cascade="all, delete", backref='compa')
    }, order_by=company.c.schemaa)
