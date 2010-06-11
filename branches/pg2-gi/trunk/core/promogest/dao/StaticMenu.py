#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promoCMS.Environment import *
from Dao import Dao
from Language import Language
from StaticPages import StaticPages

class StaticMenu(Dao):

    def __init__(self,req=None, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

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
