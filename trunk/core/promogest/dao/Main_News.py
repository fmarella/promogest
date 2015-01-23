# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from promogest.dao.DaoUtils import get_columns


from promogest.dao.Dao import Dao, Base
from promogest.dao.CategoriaNews import CategoriaNews
from promogest.dao.Language import Language
from promogest.dao.User import User


class MainNews(Base, Dao):

    try:
        __table__=Table('main_news', meta, schema=mainSchema, autoload=True,autoload_with=engine)
    except:
        #from data.categoriaNews import t_news_category
        from data.main_news import t_main_news
        __table__ = t_main_news


    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    @property
    def tipo_news(self):
        if self.id_categoria:
            a = CategoriaNews().getRecord(id=self.id_categoria)
            if a:
                return a.denominazione
            else:
                return None
        else:
            return None

    def filter_values(self,k,v):
        if k == "title":
            dic= { k :MainNews.__table__.c.title == v}
        elif k =="active":
            dic= { k :MainNews.__table__.c.active == v}
        elif k =="permalink":
            dic= { k :MainNews.__table__.c.permalink == v}
        elif k=='id_categoria':
            dic= {  k : MainNews.__table__.c.id_categoria == v}
        elif k=='other_then_id_categoria':
            dic= {  k : MainNews.__table__.c.id_categoria != v}
        elif k == 'searchkey':
            dic = {k:or_(MainNews.__table__.c.title.ilike("%"+v+"%"),
                        MainNews.__table__.c.abstract.ilike("%"+v+"%"),
                        MainNews.__table__.c.body.ilike("%"+v+"%"))
                }
        return  dic[k]
