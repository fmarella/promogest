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
from Dao import Dao
from migrate import *


class Magazzino(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'denominazione' : magazzino.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

magazzino=Table('magazzino',params['metadata'],schema = params['schema'],autoload=True)

#if "pvcode_" not in [c.name for c in magazzino.columns]:
#    col = Column('pvcode_', String)
#    col.create(magazzino)

if "pvcode" not in [c.name for c in magazzino.columns]:
    col = Column('pvcode', String)
    col.create(magazzino)


std_mapper = mapper(Magazzino, magazzino,
        properties={
        'indirizzo':deferred(magazzino.c.indirizzo),
        'cap':deferred(magazzino.c.cap),
        'provincia':deferred(magazzino.c.provincia),
        'nazione':deferred(magazzino.c.nazione),
        'pvcode':deferred(magazzino.c.pvcode),
        'data_ultima_stampa_giornale':deferred(magazzino.c.data_ultima_stampa_giornale),

    },
 order_by=magazzino.c.id)
