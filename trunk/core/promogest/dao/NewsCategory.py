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
from promogest.Environment import *
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
