# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Maccis <amaccis@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao

class Page(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'denominazione' : page.c.title.ilike("%"+v+"%")}
        return  dic[k]

page=Table('static_page',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
std_mapper = mapper(Page, page, order_by=page.c.id)