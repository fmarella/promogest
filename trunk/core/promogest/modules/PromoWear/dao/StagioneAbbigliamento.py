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

class StagioneAbbigliamento(Base, Dao):
    try:
        __table__ = Table('stagione_abbigliamento',
                        params['metadata'],
                        schema = params['mainSchema'],
                        autoload=True)
    except:
        __table__ = Table('stagione_abbigliamento', params['metadata'],
                            Column('id', Integer, primary_key=True),
                            Column('denominazione', String(50), nullable=False),
                            schema=params['mainSchema'])

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=="id":
            dic= {k: stagioneabbigliamento.c.id ==v}
        elif k == "denominazioneBreve":
            dic = {k:stagioneabbigliamento.c.denominazione_breve == v }
        elif k == "denominazione":
            dic = {k:stagioneabbigliamento.c.denominazione == v }
        return  dic[k]


s= select([StagioneAbbigliamento.__table__.c.denominazione]).execute().fetchall()
if (u'Primavera - Estate',) not in s or s==[]:
    tipo = StagioneAbbigliamento.__table__.insert()
    tipo.execute(denominazione='Primavera - Estate')
    tipo.execute(denominazione='Autunno - Inverno')
