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
from ListinoComplessoListino import ListinoComplessoListino


class Listino(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    #def __repr__(self):
        #return "il modulo è %s" %self.denominazione

    def _getCategorieCliente(self):
        self.__dbCategorieCliente = ListinoCategoriaCliente().select(idListino=self.id, batchSize=None)
        self.__categorieCliente = self.__dbCategorieCliente[:]
        return self.__categorieCliente

    def _setCategorieCliente(self, value):
        self.__categorieCliente = value

    categorieCliente = property(_getCategorieCliente, _setCategorieCliente)

    def _getMagazzini(self):
        self.__dbMagazzini = ListinoMagazzino().select(idListino=self.id, batchSize=None)
        self.__magazzini = self.__dbMagazzini[:]
        return self.__magazzini

    def _setMagazzini(self, value):
        self.__magazzini = value

    magazzini = property(_getMagazzini, _setMagazzini)

    def _getListinoComplesso(self):
        self.__dbListinoComplesso = ListinoComplessoListino().select(idListinoComplesso=self.id, batchSize=None)
        self.__listinocomplesso = self.__dbListinoComplesso[:]
        return self.__listinocomplesso

    def _setListinoComplesso(self, value):
        self.__listinocomplesso = value

    listiniComplessi = property(_getListinoComplesso, _setListinoComplesso)

    def _isComplex(self):
        if ListinoComplessoListino().select(idListinoComplesso=self.id):
            return True
        else:
            return False
    isComplex = property(_isComplex)

    def _sottoListini(self):
        """
            Return a list of Listini ID
        """
        if self.isComplex:
            lista = []
            for sotto in self.listiniComplessi:
                lista.append(sotto.id_listino)
            self. __sottoListiniID = lista
        else:
            self. __sottoListiniID=None
            return self. __sottoListiniID
        return self. __sottoListiniID
    sottoListiniID = property(_sottoListini)


    def delete(self, multiple=False, record = True):
        cleanListinoCategoriaCliente = ListinoCategoriaCliente()\
                                                .select(idListino=self.id,
                                                            batchSize=None)
        for lcc in cleanListinoCategoriaCliente:
            lcc.delete()
        cleanMagazzini = ListinoMagazzino().select(idListino=self.id,
                                                    batchSize=None)
        for mag in cleanMagazzini:
            mag.delete()
        params['session'].delete(self)
        params['session'].commit()
        #self.saveToLogApp(self)


    def filter_values(self,k,v):
        if k=='id' or k=='idListino':
            dic= {k:listino.c.id ==v}
        elif k =='listinoAttuale':
            dic= {k:listino.c.listino_attuale ==v}
        elif k=='denominazione':
            dic= {k:listino.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

listino=Table('listino', params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(Listino, listino, properties={
    "listino_categoria_cliente" :relation(ListinoCategoriaCliente, backref="listino"),
    "listino_magazzino" :relation(ListinoMagazzino, backref="listino"),
    "listino_complesso":relation(ListinoComplessoListino,primaryjoin=
                        ListinoComplessoListino.id_listino==listino.c.id, backref="listino")},
        order_by=listino.c.id)