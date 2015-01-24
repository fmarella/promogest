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

from promogest.dao.Dao import Dao, Base
from promogest.dao.CategoriaNews import CategoriaNews
from promogest.dao.Language import Language
from promogest.dao.User import User


class News(Base, Dao):
    try:
        __table__ = Table('news', params['metadata'], schema=params['schema'], autoload=True)
    except:
        from data.categoriaNews import t_news_category
        from data.news import t_news
        __table__ = t_news

    __mapper_args__ = {
        'order_by' : __table__.c.id.desc()
    }

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    @property
    def tipo_news(self):
        if self.id_categoria and self.categor:
            return self.categor.denominazione
        else:
            return ""
    @property
    def categor(self):
        aa = CategoriaNews().getRecord(id=self.id_categoria)
        return aa

    def filter_values(self,k,v):
        if k == "title":
            dic= { k :News.__table__.c.title == v}
        elif k =="active":
            dic= { k :News.__table__.c.active == v}
        elif k =="permalink":
            dic= { k :News.__table__.c.permalink == v}
        elif k == 'searchkey':
            dic = {k:or_(News.__table__.c.title.ilike("%"+v+"%"),
                        News.__table__.c.abstract.ilike("%"+v+"%"),
                        News.__table__.c.body.ilike("%"+v+"%"))
}
        return  dic[k]
