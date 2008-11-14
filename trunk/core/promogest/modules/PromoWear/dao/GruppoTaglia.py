# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.modules.PromoWear.dao.GruppoTagliaTaglia import GruppoTagliaTaglia
from Taglia import Taglia

class GruppoTaglia(Dao):

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

        self.__taglie = None


    def _getTaglie(self):
        #if self.__taglie is None:
        grtts = GruppoTagliaTaglia(isList=True).select(idGruppoTaglia=self.id,
                                                        batchSize=None)

        self.__taglie = [Taglia(id=grtt.id_taglia).getRecord() for grtt in grtts]
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
        a =  params["session"].query(GruppoTaglia)\
                                .filter(and_(GruppoTagliaTaglia.id_gruppo_taglia == self.id,GruppoTagliaTaglia.id_taglia==Taglia.id)).all()
        if not a: return a
        else: return a[0].denominazione_breve
    denominazione_breve_taglia = property(_denominazione_breve_taglia)

    def filter_values(self,k,v):
        if k == "id":
            dic= {'id':gruppotaglia.c.id ==v }
        elif k == "idTaglia":
            dic = {k:gruppotaglia.c.id_taglia ==v}
        return  dic[k]

gruppotaglia=Table('gruppo_taglia', params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(GruppoTaglia, gruppotaglia, properties={
        "GTT":relation(GruppoTagliaTaglia,primaryjoin=
                (GruppoTagliaTaglia.id_gruppo_taglia==gruppotaglia.c.id), backref="GTTGT"),},
        order_by=gruppotaglia.c.id)