# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promoCMS.Environment import *
from Dao import Dao
from Language import Language
from User import User

class StaticPages(Dao):

    def __init__(self, req=None, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        if k=='id_language':
            dic= {  k : staticpage.c.id_language == v}
        elif k == "titlePage":
            dic = { k: staticpage.c.title==v }
        elif k == "permalink":
            dic = { k: staticpage.c.permalink==v }
        return  dic[k]

staticpage=Table('static_page',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(StaticPages, staticpage, properties = {
        'lang' : relation(Language),
        'user' : relation(User) })
