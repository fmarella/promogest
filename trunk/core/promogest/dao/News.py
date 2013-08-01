# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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
from promogest.dao.Dao import Dao
from promogest.dao.NewsCategory import NewsCategory
from promogest.dao.Language import Language
from User import User

languageTable = Table('language', params['metadata'], autoload=True, schema=params['mainSchema'])
userTable = Table('utente', params['metadata'], autoload=True, schema=params['mainSchema'])
neswCategoryTable = Table('news_category', params['metadata'], autoload=True, schema=params['schema'])

if params["tipo_db"] == "sqlite":
    utenteFK ='utente.id'
    languageFK = 'language.id'
    categoriaFK = 'news_category.id'
else:
    utenteFK =params['mainSchema']+'.utente.id'
    languageFK =params['mainSchema']+'.language.id'
    categoriaFK =params['schema']+'.news_category.id'

newsTable= Table('news', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('title', String(200), nullable=False),
        Column('abstract', String(400), nullable=True),
        Column('body', Text, nullable=True),
        Column('source_url', String(400), nullable=True),
        Column('source_url_alt_text', String(400), nullable=True),
        Column('imagepath', String(400), nullable=True),
        Column('insert_date', DateTime, nullable=True),
        Column('publication_date', DateTime, nullable=True),
        Column('clicks', Integer),
        Column("permalink", String(500), nullable=True),
        Column('active', Boolean, default=0),
        Column('id_categoria', Integer,ForeignKey(categoriaFK)),
        Column('id_user', Integer,ForeignKey(utenteFK)),
        Column('id_language', Integer,ForeignKey(languageFK)),
        schema=params['schema']
        )
newsTable.create(checkfirst=True)

class News(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "title":
            dic= { k :news.c.title == v}
        elif k =="active":
            dic= { k :news.c.active == v}
        elif k =="permalink":
            dic= { k :news.c.permalink == v}
        elif k == 'searchkey':
            dic = {k:or_(news.c.title.ilike("%"+v+"%"),
                        news.c.abstract.ilike("%"+v+"%"),
                        news.c.body.ilike("%"+v+"%"))
}
        return  dic[k]



news=Table('news', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(News, news, properties={
            'categor':relation(NewsCategory, backref='news'),
            'lang' : relation(Language),
            'user' : relation(User)
                }, order_by=news.c.id.desc())
