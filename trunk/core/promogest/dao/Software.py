#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from core.dao.Language import Language
from Dao import Dao
from core.dao.SoftwareCategory import SoftwareCategory
from core.dao.User import User

categoryTable = Table('software_category', params["metadata"], autoload=True, schema=params["schema"])
userTable = Table('utente',params["metadata"], autoload=True, schema=params["schema"])
languageTable = Table('language', params['metadata'], autoload=True, schema = params['mainSchema'])

if tipo_db == "sqlite":
    categoriFK = "software_category.id"
    userFK = "utente.id"
    language = 'language.id'
else:
    categoriFK = params["schema"]+".software_category.id"
    userFK = params["schema"]+".utente.id"
    language= params['mainSchema']+'.language.id'

sotwareTable  = Table('software', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('denomination',String(100), unique=True, nullable=False),
        Column('license',String(200), nullable=False),
        Column('opensource',Boolean, nullable=False),
        Column('category_id',Integer,ForeignKey(categoriFK), nullable=True),
        Column('id_user',Integer,ForeignKey(userFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
        Column('url',String(200)),
        Column('imagepath',String(500)),
        Column('versione',String(500)),
        Column('email',String(200)),
        Column('insertdate',DateTime),
        Column('description',Text),
        Column('active', Boolean, default=0),
        Column('abstract', String(500), nullable=True),
        Column('id_language', Integer,ForeignKey(language)),
        Column('clicks', Integer, default=0),
        #useexisting=True,
        schema = params['schema'])
sotwareTable.create(checkfirst=True)

from core.dao.SoftwareSoftwareCategory import SoftwareCategorySoftware

class Software(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)
        self.__dbcategorie = []
        self.__categorie = []

    @reconstructor
    def init_on_load(self):
        self.__dbcategorie = []
        self.__categorie = []


    def filter_values(self, k,v):
        if k == "denomination":
            dic= { k : software.c.denomination.ilike("%"+v+"%")}
        elif k == "denominationEM":
            dic= { k : software.c.denomination == v}
        elif k =="active":
            dic = { k :software.c.active ==v}
        return  dic[k]

    def _getcategorie(self):
        if not self.__categorie:
            if self.categ:
                for swcat in self.categ:
                    sc = SoftwareCategory().getRecord(id=swcat.id_software_category)
                    self.__dbcategorie.append(sc)
        self.__categorie = self.__dbcategorie[:]
        #print "categproeeeeeeeeeeeeee",self.__categorie
        return self.__categorie

    def _setcategorie(self, value):
        self.__categorie = value
    categorie = property(_getcategorie, _setcategorie)


    def categorieDel(self, id=None):
        """
        Cancella le categorie
        """
        row = SoftwareCategorySoftware().select(id_software= id,
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
                softcat = SoftwareCategorySoftware()
                softcat.id_software = self.id
                softcat.id_software_category = int(cat)
                params["session"].add(softcat)
            params["session"].commit()
                    #softcat.persist()

software=Table('software', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Software, software, properties={
            'user' : relation(User, backref="sw"),
            'lang' : relation(Language),
            'categ':relation(SoftwareCategorySoftware,primaryjoin = software.c.id==SoftwareCategorySoftware.id_software, backref='sw'),
                }, order_by=software.c.id.desc())
