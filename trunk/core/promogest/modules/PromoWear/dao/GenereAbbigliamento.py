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
from promogest.dao.Dao import Dao, Base



class GenereAbbigliamento(Base, Dao):
    try:
        __table__ = Table('genere_abbigliamento',
                                params['metadata'],
                                schema=params['mainSchema'],
                                autoload=True)
    except:
        __table__ = Table('genere_abbigliamento', params['metadata'],
                            Column('id', Integer, primary_key=True),
                            Column('denominazione', String(50), nullable=False),
                            schema=params['mainSchema'])

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=="id":
            dic= {k: GenereAbbigliamento.__table__.c.id ==v}
        elif k == "denominazioneBreve":
            dic = {k:GenereAbbigliamento.__table__.c.denominazione_breve == v }
        elif k == "denominazione":
            dic = {k:GenereAbbigliamento.__table__.c.denominazione == v }
        return  dic[k]


s= select([GenereAbbigliamento.__table__.c.denominazione]).execute().fetchall()
tipo = GenereAbbigliamento.__table__.insert()
if (u'Unisex', ) not in s or s==[]:
    tipo.execute(denominazione='Unisex')
if (u"Uomo", ) not in s or s == []:
    tipo.execute(denominazione='Uomo')
if (u"Donna", ) not in s or s == []:
    tipo.execute(denominazione='Donna')
if (u"Bambino", ) not in s or s == []:
    tipo.execute(denominazione='Bambino')
