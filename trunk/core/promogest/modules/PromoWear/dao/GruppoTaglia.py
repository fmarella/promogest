# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Alessandro Scano <alessandro@promotux.it>


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
        if self.__taglie is None:
            grtts = GruppoTagliaTaglia(isList=True).select(idGruppoTaglia=self.id,
                                                        batchSize=None)

            self.__taglie = [Taglia(id=grtt.id_taglia).getRecord()
                             for grtt in grtts]
        return self.__taglie

    taglie = property(_getTaglie)

    def filter_values(self,k,v):
        dic= {'id':gruppotaglia.c.id ==v }
        return  dic[k]

gruppotaglia=Table('gruppo_taglia',
           params['metadata'],
           schema = params['schema'],
           autoload=True)

std_mapper = mapper(GruppoTaglia, gruppotaglia, properties={

    },
        order_by=gruppotaglia.c.id)