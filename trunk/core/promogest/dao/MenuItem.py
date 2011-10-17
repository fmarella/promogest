#-*- coding: utf-8 -*-
#
# Promogest -Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from Language import Language
from Menu import Menu
#from StaticPages import StaticPages

languageTable = Table('language', params['metadata'], autoload=True, schema=params['mainSchema'])
#pageTable = Table('static_page', params['metadata'], autoload=True, schema=params['schema'])
menu=Table('menu', params['metadata'],schema = params['schema'],autoload=True)

try:
    menuitem= Table('menu_item',params['metadata'],schema = params['schema'],autoload=True)
except:

    if params["tipo_db"] == "sqlite":
        staticpageFK = 'static_page.id'
        menuFK = 'menu.id'
    else:
        staticpageFK = params['schema']+'.static_page.id'
        menuFK = params['schema']+'.menu.id'

    if params["tipo_db"] == "sqlite":
        languageFK = 'language.id'
    else:
        languageFK = params['mainSchema']+'.language.id'

    menuitem = Table('menu_item', params['metadata'],
            Column('id', Integer, primary_key=True),
            Column('item', String(50), nullable=True),
            Column('id_page', Integer, ForeignKey(staticpageFK),nullable=True),
            Column('url',String(100), nullable=True),
            Column('target',String(20), nullable=True),
            Column('id_menu', Integer,ForeignKey(menuFK),nullable=True),
            Column('id_padre', Integer),
            Column('id_language', Integer,ForeignKey(languageFK)),
            Column('active', Boolean),
            Column('number', Integer, nullable=True),
            Column('position', Integer, nullable=True),
            schema = params['schema']            )
    menuitem.create(checkfirst=True)

class MenuItem(Dao):

    def __init__(self,req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        if k == 'id_language':
            dic= {  k : menuitem.c.id_language == v}
        elif k =='id_languageList':
            dic= {  k : menuitem.c.id_language.in_(v)}
        return  dic[k]

    def _permalink(self):
        if self.page :return self.page.permalink or ""

    permalink = property(_permalink)

std_mapper=mapper(MenuItem, menuitem,
        properties={
        "lang":relation(Language,backref="menuitem"),
#        "page":relation(StaticPages,backref="menuitem")
        })
