# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 2011 by Promotux
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
from promogest.dao.DaoUtils import *
from promogest.lib.utils import *
from promogest.dao.Cliente import Cliente

try:
    testatainfopeso = Table('testata_info_peso',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
except:
    clienteTable = Table('cliente', params['metadata'], autoload=True, schema=params['schema'])

    if params["tipo_db"] == "sqlite":
        clienteFK ='cliente.id'
    else:
        clienteFK = params['schema']+'.cliente.id'

    testatainfopeso = Table('testata_info_peso', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('note', Text, nullable=True),
            Column('id_cliente', Integer,ForeignKey(clienteFK,onupdate="CASCADE",ondelete="CASCADE")),
            Column('data_inizio', DateTime, nullable=True),
            Column('citta', String(10), nullable=True),
            Column('data_fine', DateTime, nullable=True),
            Column('privacy', Boolean, default=True),
            schema=params["schema"],
            useexisting=True)
    testatainfopeso.create(checkfirst=True)

from promogest.modules.InfoPeso.dao.RigaInfoPeso import RigaInfoPeso

class TestataInfoPeso(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        self.__righeInfoPeso = []
        self.__dbRigheInfoPeso = []

    @reconstructor
    def init_on_load(self):
        self.__righeInfoPeso = []
        self.__dbRigheInfoPeso = []

    def _getRigheInfoPeso(self):
#        if not self.__righePrimaNota:
        self.__dbRigheInfoPeso = session.query(RigaInfoPeso)\
                                            .with_parent(self)\
                                            .filter_by(id_testata_info_peso=self.id)\
                                            .all()
        self.__righeInfoPeso = self.__dbRigheInfoPeso[:]
        return self.__righeInfoPeso

    def _setRigheInfoPeso(self, value):
        self.__righeInfoPeso = value

    righeinfopeso = property(_getRigheInfoPeso, _setRigheInfoPeso)

    def filter_values(self,k,v):
        if k == 'idCliente':
            dic = {k:testatainfopeso.c.id_cliente == v}
        return  dic[k]

    def righeInfoPesoDel(self,id=None):
        """ Cancella le righe associate ad un info peso
        """
        row = RigaInfoPeso().select(idTestataInfoPeso= id,
                                    offset = None,
                                    batchSize = None)
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
        return True


    def delete(self):
        row = RigaInfoPeso().select(idTestataInfoPeso= self.id,
                                    offset = None,
                                    batchSize = None)
        if row:
            for r in row:
                params['session'].delete(r)
                params["session"].commit()
        params['session'].delete(self)
        params["session"].commit()


    def persist(self):
        """ cancellazione righe associate alla testata """
        params["session"].add(self)
        params["session"].commit()
#        self.righeInfoPesoDel(self.id)
        if self.__righeInfoPeso:
            for riga in self.__righeInfoPeso:
                riga.id_testata_info_peso = self.id
                riga.persist()
        self.__righeInfoPeso= []

std_mapper = mapper(TestataInfoPeso, testatainfopeso,properties={
        "rigatestinfo": relation(RigaInfoPeso,primaryjoin=
                testatainfopeso.c.id==RigaInfoPeso.id_testata_info_peso,
#                foreign_keys=[RigaPrimaNota.id_testata_prima_nota],
                cascade="all, delete")},
                order_by=testatainfopeso.c.id)
