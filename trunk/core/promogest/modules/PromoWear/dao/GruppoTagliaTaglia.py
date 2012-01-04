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
from promogest.modules.PromoWear.dao.Taglia import Taglia


class GruppoTagliaTaglia(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'idGruppoTaglia':
            dic= {k: gruppotagliataglia.c.id_gruppo_taglia ==v}
        elif k == 'idTaglia':
            dic= {k: gruppotagliataglia.c.id_taglia ==v}
        return  dic[k]

    def _denominazione_breve_gt(self):
        if self.GTTGT: return self.GTTGT.denominazione_breve or ""
    denominazione_breve_gruppo_taglia= property(_denominazione_breve_gt)

    def _denominazione_gt(self):
        if self.GTTGT: return self.GTTGT.denominazione or ""
    denominazione_gruppo_taglia= property(_denominazione_gt)

    def _denominazione_breve_ta(self):
        if self.TAG: return self.TAG.denominazione_breve or ""
    denominazione_breve_taglia= property(_denominazione_breve_ta)

    def _denominazione_ta(self):
        if self.TAG: return self.TAG.denominazione or ""
    denominazione_taglia= property(_denominazione_ta)

gruppotagliataglia=Table('gruppo_taglia_taglia',
           params['metadata'],
           schema = params['schema'],
           autoload=True)

std_mapper = mapper(GruppoTagliaTaglia, gruppotagliataglia, properties={
            "TAG": relation(Taglia,primaryjoin=
            (Taglia.id==gruppotagliataglia.c.id_taglia), backref="GTTTAG"), },
    order_by=(gruppotagliataglia.c.id_gruppo_taglia,gruppotagliataglia.c.ordine))
