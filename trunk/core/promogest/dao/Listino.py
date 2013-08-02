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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *

try:
    t_listino=Table('listino', params['metadata'],schema = params['schema'],autoload=True)
except:
    from data.listino import t_listino

from promogest.dao.Dao import Dao
from promogest.dao.ListinoCategoriaCliente import ListinoCategoriaCliente
from promogest.dao.ListinoMagazzino import ListinoMagazzino
from promogest.dao.ListinoComplessoListino import ListinoComplessoListino
from migrate import *



def idListinoGet():
    if tipo_eng == "postgresql":
        listino_sequence = Sequence("listino_id_seq",
                                    schema=params['schema'])
        return params['session'].connection().execute(listino_sequence)
    elif tipo_eng == "sqlite":
        # TODO: ottimizzare questa query usando func.max da sqlalchemy
        listini = Listino().select(orderBy=Listino.id, batchSize=None)
        if not listini:
            return 1
        else:
            return max([p.id for p in listini]) + 1
    else:
        raise Exception("Impossibile generare l'ID listino per l'engine in uso.")


class Listino(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def __repr__(self):
        return '<Listino ID={0}>'.format(self.id)

    def persist(self):
        if not self.id:
            self.id = idListinoGet()
        params["session"].add(self)
        params["session"].commit()

    def _getCategorieCliente(self):
        #self.__dbCategorieCliente = ListinoCategoriaCliente().select(idListino=self.id, batchSize=None)
        self.__dbCategorieCliente = self.listino_categoria_cliente
        self.__categorieCliente = self.__dbCategorieCliente[:]
        return self.__categorieCliente

    def _setCategorieCliente(self, value):
        self.__categorieCliente = value

    categorieCliente = property(_getCategorieCliente, _setCategorieCliente)

    def _getMagazzini(self):
        #self.__dbMagazzini = ListinoMagazzino().select(idListino=self.id, batchSize=None)
        self.__dbMagazzini = self.listino_magazzino
        self.__magazzini = self.__dbMagazzini[:]
        return self.__magazzini

    def _setMagazzini(self, value):
        self.__magazzini = value

    magazzini = property(_getMagazzini, _setMagazzini)

    def _getListinoComplesso(self):
        self.__dbListinoComplesso = ListinoComplessoListino().select(idListinoComplesso=self.id, batchSize=None)
        #self.__dbListinoComplesso = self.listino_complesso
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
    #isComplex = property(_isComplex)

    def _sottoListiniIDD(self):
        """
            Return a list of Listini ID
        """
        if ListinoComplessoListino().select(idListinoComplesso=self.id):
            lista = []
            for sotto in self.listiniComplessi:
                lista.append(sotto.id_listino)
            self. __sottoListiniID = lista
        else:
            self. __sottoListiniID=None
            return self. __sottoListiniID
        return self. __sottoListiniID
    sottoListiniID = property(_sottoListiniIDD)


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
            dic= {k:t_listino.c.id ==v}
        elif k =='listinoAttuale':
            dic= {k:t_listino.c.listino_attuale ==v}
        elif k=='denominazione':
            dic= {k:t_listino.c.denominazione.ilike("%"+v+"%")}
        elif k=='denominazioneEM':
            dic= {k:t_listino.c.denominazione ==v}
        elif k=='dataListino':
            dic= {k:t_listino.c.data_listino ==v}
        elif k=='visibileCheck':
            dic= {k:t_listino.c.visible ==None}
        elif k=='visibili':
            dic= {k:t_listino.c.visible ==v}
        return  dic[k]


std_mapper = mapper(Listino, t_listino, properties={
    "listino_categoria_cliente" :relation(ListinoCategoriaCliente, backref="listino"),
    "listino_magazzino" :relation(ListinoMagazzino, backref="listino"),
    "listino_complesso":relation(ListinoComplessoListino,primaryjoin=
                        ListinoComplessoListino.id_listino==t_listino.c.id, backref="listino")},
        order_by=t_listino.c.id)
