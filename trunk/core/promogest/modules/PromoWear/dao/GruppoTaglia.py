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
from promogest.modules.PromoWear.dao.GruppoTagliaTaglia import GruppoTagliaTaglia
from promogest.modules.PromoWear.dao.Taglia import Taglia


class GruppoTaglia(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

        self.__taglie = None


    def _getTaglie(self):
        #if self.__taglie is None:
        grtts = GruppoTagliaTaglia().select(idGruppoTaglia=self.id,
                                                        batchSize=None)
        self.__taglie = [Taglia().getRecord(id=grtt.id_taglia) for grtt in grtts]
        return self.__taglie or None

    taglie = property(_getTaglie)


    def _denominazione_gruppo_taglia(self):
        """ esempio di funzione  unita alla property """
        return self.denominazione
    denominazione_gruppo_taglia = property(_denominazione_gruppo_taglia)

    def _denominazione_breve_gruppo_taglia(self):
        """ esempio di funzione  unita alla property """
        return self.denominazione_breve
    denominazione_breve_gruppo_taglia = property(_denominazione_breve_gruppo_taglia)


    def _denominazione_taglia(self):
        """ esempio di funzione  unita alla property """
        a =  params["session"].query(GruppoTaglia)\
                                .filter(and_(GruppoTagliaTaglia.id_gruppo_taglia == self.id,GruppoTagliaTaglia.id_taglia==Taglia.id)).all()
        if not a: return a
        else: return a[0].denominazione
    denominazione_taglia = property(_denominazione_taglia)

    def _denominazione_breve_taglia(self):
        """ esempio di funzione  unita alla property """
        a = params["session"].query(GruppoTaglia)\
                                .filter(and_(GruppoTagliaTaglia.id_gruppo_taglia == self.id,GruppoTagliaTaglia.id_taglia==Taglia.id)).all()
        if not a: return a
        else: return a[0].denominazione_breve
    denominazione_breve_taglia = property(_denominazione_breve_taglia)

    def filter_values(self,k,v):
        if k == "id":
            dic= {'id': gruppotaglia.c.id ==v}
        elif k == "idTaglia":
            dic = {k: gruppotaglia.c.id_taglia ==v}
        elif k == "denominazione":
            dic = {k: gruppotaglia.c.denominazione ==v}
        return  dic[k]

gruppotaglia=Table('gruppo_taglia',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

std_mapper = mapper(GruppoTaglia, gruppotaglia, properties={
        "GTT":relation(GruppoTagliaTaglia, primaryjoin=
                (GruppoTagliaTaglia.id_gruppo_taglia==gruppotaglia.c.id), backref="GTTGT"), },
        order_by=gruppotaglia.c.id)
