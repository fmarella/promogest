# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation
from promogest.Environment import params
from promogest.dao.Dao import Dao
from promogest.dao.Magazzino import Magazzino

try:
    t_listino_magazzino = Table('listino_magazzino',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
except:
    from data.listinoMagazzino import t_listino_magazzino

class ListinoMagazzino(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    @property
    def magazzino(self):
        if self.magazzin:
            mag = self.magazzin.denominazione
            return mag
        else:
            return ""

    def filter_values(self,k,v):
        dic= {  'idListino' : t_listino_magazzino.c.id_listino ==v,
                'idMagazzino' : t_listino_magazzino.c.id_magazzino ==v}
        return  dic[k]


std_mapper = mapper(ListinoMagazzino, t_listino_magazzino, properties={
        "magazzin": relation(Magazzino, backref="listino_magazzino")
            }, order_by=t_listino_magazzino.c.id_listino)
