# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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
from Dao import Dao, Base

class Faq(Base, Dao):
    try:
        __table__ = Table('faq', params['metadata'],schema = params['schema'],autoload=True)
    except:
        from data.faq import t_faq
        __table__ = t_faq

    __mapper_args__ = {
            "order_by": __table__.c.id.desc()
    }

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "title":
            dic= { k :Faq.__table__.c.title == v}
        elif k =="active":
            dic= { k :Faq.__table__.c.active == v}
        elif k =="permalink":
            dic= { k :Faq.__table__.c.permalink == v}
        elif k == 'searchkey':
            dic = {k:or_(Faq.__table__.c.title.ilike("%"+v+"%"),
                        Faq.__table__.c.abstract.ilike("%"+v+"%"),
                        Faq.__table__.c.body.ilike("%"+v+"%"))}
        return  dic[k]
