#-*- coding: utf-8 -*-
#
# Promogest -Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao
from Language import Language
from StaticPages import StaticPages

languageTable = Table('language', params['metadata'], autoload=True, schema=params['mainSchema'])
pageTable = Table('static_page', params['metadata'], autoload=True, schema=params['schema'])

if params["tipo_db"] == "sqlite":
    staticpageFK = 'static_page.id'
else:
    staticpageFK = params['schema']+'.static_page.id'

if params["tipo_db"] == "sqlite":
    languageFK = 'language.id'
else:
    languageFK = params['mainSchema']+'.language.id'

staticmenuTable= Table('static_menu', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('item', String(50), nullable=True),
        Column('id_page', Integer, ForeignKey(staticpageFK),nullable=True),
        Column('url',String(100), nullable=True),
        Column('id_padre', Integer),
        Column('id_language', Integer,ForeignKey(languageFK)),
        Column('visible', Boolean, default=True),
        Column('number', Integer, nullable=True),
        Column('position', Integer, nullable=True),
        schema = params['schema']
        )
staticmenuTable.create(checkfirst=True)

class StaticMenu(Dao):

    def __init__(self,req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        if k == 'id_language':
            dic= {  k : staticmenu.c.id_language == v}
        elif k =='id_languageList':
            dic= {  k : staticmenu.c.id_language.in_(v)}
        return  dic[k]

    def _permalink(self):
        if self.page :return self.page.permalink or ""

    permalink = property(_permalink)
staticmenu= Table('static_menu',params['metadata'],schema = params['schema'],autoload=True)

std_mapper=mapper(StaticMenu, staticmenu,
        properties={
        "lang":relation(Language,backref="static_menu"),
        "page":relation(StaticPages,backref="static_menu")})
