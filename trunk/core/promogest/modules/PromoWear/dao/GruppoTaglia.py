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
from promogest.modules.PromoWear.dao.GruppoTagliaTaglia import GruppoTagliaTaglia
from promogest.modules.PromoWear.dao.Taglia import Taglia


class GruppoTaglia(Base, Dao):
    try:
        __table__ = Table('gruppo_taglia',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
    except:
        __table__ = Table('gruppo_taglia', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione', 'denominazione_breve'),
                schema=params["schema"])

    GTT = relationship("GruppoTagliaTaglia",backref="GTTGT")
    #denominazione_gruppo_taglia = column_property("denominazione")
    #denominazione_breve_gruppo_taglia = column_property("denominazione_breve")

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

        self.__taglie = None

    @property
    def taglie(self):
        return [Taglia().getRecord(id=grtt.id_taglia) for grtt in self.GTT] or None

    @property
    def denominazione_gruppo_taglia(self):
        return self.denominazione

    @property
    def denominazione_breve_gruppo_taglia(self):
        return self.denominazione_breve

    @property
    def denominazione_taglia(self):
        """ esempio di funzione  unita alla property """
        a =  params["session"].query(GruppoTaglia)\
                                .filter(and_(GruppoTagliaTaglia.id_gruppo_taglia == self.id,GruppoTagliaTaglia.id_taglia==Taglia.id)).all()
        if not a: return a
        else: return a[0].denominazione

    @property
    def denominazione_breve_taglia(self):
        """ esempio di funzione  unita alla property """
        a = params["session"].query(GruppoTaglia)\
                                .filter(and_(GruppoTagliaTaglia.id_gruppo_taglia == self.id,GruppoTagliaTaglia.id_taglia==Taglia.id)).all()
        if not a: return a
        else: return a[0].denominazione_breve

    def filter_values(self,k,v):
        if k == "id":
            dic= {'id': GruppoTaglia.__table__.c.id ==v}
        elif k == "idTaglia":
            dic = {k: GruppoTaglia.__table__.c.id_taglia ==v}
        elif k == "denominazione":
            dic = {k: GruppoTaglia.__table__.c.denominazione ==v}
        return  dic[k]
