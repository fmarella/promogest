# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 2011 by Promotux
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

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import params
from Dao import Dao
from Magazzino import Magazzino

class ListinoMagazzino(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _magazzino(self):
        if self.magazzin:
            mag = self.magazzin.denominazione
            return mag
        else:
            return ""
    magazzino = property(_magazzino)

    def filter_values(self,k,v):
        dic= {  'idListino' : listino_magazzino.c.id_listino ==v,
                'idMagazzino' : listino_magazzino.c.id_magazzino ==v}
        return  dic[k]

listino_magazzino = Table('listino_magazzino',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
std_mapper = mapper(ListinoMagazzino, listino_magazzino, properties={
        "magazzin": relation(Magazzino, backref="listino_magazzino")
            }, order_by=listino_magazzino.c.id_listino)
