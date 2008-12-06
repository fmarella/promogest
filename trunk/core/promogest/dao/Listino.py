#-*- coding: utf-8 -*-
#
"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao
from ListinoCategoriaCliente import ListinoCategoriaCliente
from ListinoMagazzino import ListinoMagazzino


class Listino(Dao):

    def __init__(self, arg=None,isList=False):
        Dao.__init__(self, entity=self.__class__, isList=isList)

    def _getCategorieCliente(self):
        self.__dbCategorieCliente = params['session'].query(ListinoCategoriaCliente).with_parent(self).filter_by(id_listino=self.id).all()
        self.__categorieCliente = self.__dbCategorieCliente[:]
        return self.__categorieCliente

    def _setCategorieCliente(self, value):
        self.__categorieCliente = value

    categorieCliente = property(_getCategorieCliente, _setCategorieCliente)

    def _getMagazzini(self):
        self.__dbMagazzini = params['session'].query(ListinoMagazzino).with_parent(self).filter_by(id_listino=self.id).all()
        self.__magazzini = self.__dbMagazzini[:]
        return self.__magazzini

    def _setMagazzini(self, value):
        self.__magazzini = value

    magazzini = property(_getMagazzini, _setMagazzini)

    def delete(self, multiple=False, record = True):
        cleanListinoCategoriaCliente = ListinoCategoriaCliente(isList=True)\
                                                .select(idListino=self.id,
                                                            batchSize=None)
        for lcc in cleanListinoCategoriaCliente:
            lcc.delete()
        cleanMagazzini = ListinoMagazzino(isList=True)\
                                            .select(idListino=self.id,
                                            batchSize=None)
        for mag in cleanMagazzini:
            mag.delete()
        params['session'].delete(self)
        params["session"].commit()
        params['session'].flush()

    def filter_values(self,k,v):
        if k=='id':
            dic= {k:listino.c.id ==v}
        elif k =='idListino':
            dic= {k:listino.c.id ==v}
        elif k=='denominazione':
            dic= {k:listino.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

listino=Table('listino',
           params['metadata'],
           schema = params['schema'],
           autoload=True)

std_mapper = mapper(Listino, listino, properties={
    "listino_categoria_cliente" :relation(ListinoCategoriaCliente, backref="listino"),
    "listino_magazzino" :relation(ListinoMagazzino, backref="listino")},
        order_by=listino.c.id)




