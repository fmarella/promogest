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

class StatoArticolo(Base, Dao):
    try:
        __table__ = Table('stato_articolo',
                        params['metadata'],
                        schema = params['mainSchema'],
                        autoload=True,
                        autoload_with=engine)
    except:
        from data.statoArticolo import t_stato_articolo
        __table__ = t_stato_articolo

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {}
        return  dic[k]

    def preSave(self):
        stati_articolo = []
        return True

s= select([StatoArticolo.__table__.c.denominazione]).execute().fetchall()

if  (u'Web',) not in s or s==[]:
    tipo = StatoArticolo.__table__.insert()
    tipo.execute(denominazione='Web')
