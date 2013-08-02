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

try:
    t_static_page=Table('static_page',
        params['metadata'],
        schema = params['schema'],
        autoload=True)
except:
    from data.staticPages import t_static_page

from promogest.dao.Dao import Dao
from promogest.dao.Language import Language, t_language
from promogest.dao.User import User


class StaticPages(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)


    def filter_values(self,k,v):
        if k=='id_language':
            dic= {  k : t_static_page.c.id_language == v}
        elif k == "titlePage":
            dic = { k: t_static_page.c.title==v }
        elif k == "permalink":
            dic = { k: t_static_page.c.permalink==v }
        return  dic[k]


std_mapper = mapper(StaticPages, t_static_page,
        properties = {
            'lang' : relation(Language,
                        primaryjoin= t_static_page.c.id_language==t_language.c.id,
                        foreign_keys=[t_language.c.id]),
        },
        order_by=t_static_page.c.id)
