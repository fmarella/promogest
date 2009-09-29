#-*- coding: utf-8 -*-
#
# Promogest - Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao

news_categoryTable  = Table('news_category', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('denominazione',String(100),unique=True),
        schema = params['schema'])
news_categoryTable.create(checkfirst=True)

def filler():
    datas = ["Novita' Linux","Software","Sicurezza","Mondo Opensource",
    "Distribuzioni Linux","Finanza","Linux VS Windows",
    "Pubblicazioni Linux","Games","Recensioni","Eventi Linux"]
    for da in datas:
        cate = NewsCategory().select(denominazione=da)
        if not cate:
            new = NewsCategory()
            new.denominazione = str(da)
            new.persist()


class NewsCategory(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione':newscategory.c.denominazione == v,
                }
        return  dic[k]

newscategory=Table('news_category', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(NewsCategory, newscategory)
#filler()