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
from promogest.dao.Dao import Dao

class AnnoAbbigliamento(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)


    def filter_values(self,k,v):
        if k=="id":
            dic= {k:annoabbigliamento.c.id ==v}
        elif k =="denominazione":
            dic= {k:annoabbigliamento.c.denominazione == v}
        return  dic[k]

annoabbigliamento=Table('anno_abbigliamento',
    params['metadata'],
    schema = params['mainSchema'],
    autoload=True)

s= select([annoabbigliamento.c.denominazione]).execute().fetchall()
if (u'2014', ) not in s or s==[]:
    tipo = annoabbigliamento.insert()
    tipo.execute(denominazione='2014')
    tipo.execute(denominazione='2015')
    tipo.execute(denominazione='2016')
    tipo.execute(denominazione='2017')


std_mapper = mapper(AnnoAbbigliamento, annoabbigliamento, properties={},
                order_by=annoabbigliamento.c.id)
