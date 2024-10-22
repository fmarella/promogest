# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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

from promogest.dao.Dao import Dao, Base
from promogest.dao.ListinoCategoriaCliente import ListinoCategoriaCliente
from promogest.dao.ListinoMagazzino import ListinoMagazzino
from promogest.dao.ListinoComplessoListino import ListinoComplessoListino


class Listino(Base, Dao):
    try:
        __table__ = Table('listino', params['metadata'],
                          schema=params['schema'],
                          autoload=True)
    except:
        from data.listino import t_listino
        __table__ = t_listino

    listino_categoria_cliente = relationship("ListinoCategoriaCliente", backref="listino")
    listino_magazzino = relationship("ListinoMagazzino", backref="listino")
    listino_complesso = relationship("ListinoComplessoListino",backref="listino")


    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def __repr__(self):
        return '<Listino ID={0}>'.format(self.id)

    def persist(self):
        if not self.id:
            self.id = self.idListinoGet()
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
        """ Return a list of Listini ID
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


    def idListinoGet(self):
        if tipo_eng == "postgresql":
            try:
                listino_sequence = Sequence("listino_id_seq",
                                    schema=params['schema'])
                return params['session'].connection().execute(listino_sequence)
            except:
                params['session'].rollback()
                __listini__ = self.select(batchSize=None)
                if not __listini__:
                    return 1
                else:
                    return max([p.id for p in __listini__]) + 1
        elif tipo_eng == "sqlite":
            # TODO: ottimizzare questa query usando func.max da sqlalchemy
            listini = self.select(batchSize=None)
            if not listini:
                return 1
            else:
                return max([p.id for p in listini]) + 1
        else:
            raise Exception("Impossibile generare l'ID listino per l'engine in uso.")

    def filter_values(self,k,v):
        if k=='id' or k=='idListino':
            dic= {k:Listino.__table__.c.id ==v}
        elif k =='listinoAttuale':
            dic= {k:Listino.__table__.c.listino_attuale ==v}
        elif k=='denominazione':
            dic= {k:Listino.__table__.c.denominazione.ilike("%"+v+"%")}
        elif k=='denominazioneEM':
            dic= {k:Listino.__table__.c.denominazione ==v}
        elif k=='dataListino':
            dic= {k:Listino.__table__.c.data_listino ==v}
        elif k=='visibileCheck':
            dic= {k:Listino.__table__.c.visible ==None}
        elif k=='visibili':
            dic= {k:Listino.__table__.c.visible ==v}
        return  dic[k]
