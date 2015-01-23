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

from dao.StaticPagesCategory import StaticPagesCategory

class MainStaticPages(Base, Dao):
    try:
        __table__=Table('main_static_page',
                            meta,
                            schema = mainSchema,
                            autoload=True)
    except:
        from data.main_staticPages import t_main_static_page
        __table__ = t_main_static_page

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    @property
    def tipo_static_pages(self):
        if self.id_categoria:
            a = StaticPagesCategory().getRecord(id=self.id_categoria)
            if a:
                return a.denominazione
            else:
                return None
        else:
            return None


    def filter_values(self,k,v):
        if k=='id_categoria':
            dic= {  k : MainStaticPages.__table__.c.id_categoria == v}
        elif k == "titlePage":
            dic = { k: MainStaticPages.__table__.c.title==v }
        elif k == "permalink":
            dic = { k: MainStaticPages.__table__.c.permalink==v }
        return  dic[k]
