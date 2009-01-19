# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
#from promogest.Environment import *
from promoCMS.Environment import *
from Role import Role
from Language import Language
from Dao import Dao


class Feed(Dao):
    # UserSl() class provides to make a Users dao which include more used
    # database functions

    def __init__(self, req=None, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        dic= {'name' : feed.c.name==v}
        return  dic[k]


feed=Table('feed', params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(Feed, feed)
