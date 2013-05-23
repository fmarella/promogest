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
from promogest.dao.Cliente import Cliente, t_cliente
from promogest.dao.Articolo import Articolo , t_articolo
from promogest.modules.GestioneCommesse.dao.StadioCommessa import StadioCommessa , t_stadiocommessa

try:
    t_testatacommessa = Table('testata_commessa',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
except:
    t_testatacommessa = Table('testata_commessa', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('numero', Integer, nullable=False),
            Column('denominazione', String(300), nullable=False),
            Column('note', Text, nullable=True),
            Column('id_cliente', Integer,ForeignKey(fk_prefix +'cliente.id',onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_articolo', Integer,ForeignKey(fk_prefix +'articolo.id')),
            Column('id_stadio_commessa', Integer,ForeignKey(fk_prefix +'stadio_commessa.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=True),
            Column('data_inizio', DateTime, nullable=True),
            Column('data_fine', DateTime, nullable=True),
            schema=params["schema"],
            useexisting=True)
    t_testatacommessa.create(checkfirst=True)

from RigaCommessa import RigaCommessa

class TestataCommessa(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        self.__righeCommessa = []
        self.__dbRigheCommessa= []

    @reconstructor
    def init_on_load(self):
        self.__righeCommessa = []
        self.__dbRigheCommessa = []

    def _getRigheCommessa(self):
#        if not self.__righePrimaNota:
        self.__dbRigheCommessa = session.query(RigaCommessa)\
                                            .with_parent(self)\
                                            .filter_by(id_testata_commessa=self.id)\
                                            .all()
        self.__righeCommessa = self.__dbRigheCommessa[:]
        return self.__righeCommessa

    def _setRigheCommessa(self, value):
        self.__righeCommessa = value

    righecommessa = property(_getRigheCommessa, _setRigheCommessa)

    def ultimaCommessa(self):
        a = select([func.max(testatacommessa.c.data_fine)]).execute().fetchall()
        if a:
            return a[0][0]
        else:
            return None

    @property
    def cliente(self):
        """ esempio di funzione  unita alla property """
        cli=  Cliente().getRecord(id=self.id_cliente)
        if cli:
            return cli.ragione_sociale
        else:
            return ""

    @property
    def articolo(self):
        """ esempio di funzione  unita alla property """
        art=  Articolo().getRecord(id=self.id_articolo)
        if art:
            return art.codice + " " + art.denominazione
        else:
            return ""
        return ""

    @property
    def stadio_commessa(self):
        """ esempio di funzione  unita alla property """
        cli=  StadioCommessa().getRecord(id=self.id_stadio_commessa)
        if cli:
            return cli.denominazione
        else:
            return ""

    def filter_values(self,k,v):
        if k == 'daNumero':
            dic = {k:t_testatacommessa.c.numero >= v}
        elif k == 'aNumero':
            dic = {k:t_testatacommessa.c.numero <= v}
        elif k == 'datafinecheck':
            dic = {k:t_testatacommessa.c.data_fine == None}
        elif k == 'datafine':
            dic = {k:t_testatacommessa.c.data_fine == v}
        elif k == 'numero':
            dic = {k:t_testatacommessa.c.numero == v}
        elif k == 'daDataInizio':
            dic = {k:t_testatacommessa.c.data_inizio >= v}
        elif k== 'aDataInizio':
            dic = {k:t_testatacommessa.c.data_inizio <= v}
        elif k == 'daDataFine':
            dic = {k:t_testatacommessa.c.data_fine >= v}
        elif k== 'aDataFine':
            dic = {k:t_testatacommessa.c.data_fine <= v}
        elif k == 'idStadioCommessa':
            dic = {k:rigacommessa.c.id_stadio_commessa==v}
        elif k == 'denominazione':
            dic = {k:t_testatacommessa.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

    def righeCommessaDel(self,id=None):
        """ Cancella le righe associate ad una cmmessa
        """
        row = RigaCommessa().select(idTestataCommessa= id,
                                    offset = None,
                                    batchSize = None)
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
        return True


    def delete(self):
        row = RigaCommessa().select(idTestataCommessa= self.id,
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
        pg2log.info("DENTRO IL TESTATA COMMESSA")
        params["session"].add(self)
        params["session"].commit()
        if self.__righeCommessa:
            for riga in self.__righeCommessa:
                riga.id_testata_commessa = self.id
                riga.persist()
        self.__righeCommessa = []

std_mapper = mapper(TestataCommessa, t_testatacommessa,properties={
        "rigatestcomm": relation(RigaCommessa,primaryjoin=
                t_testatacommessa.c.id==RigaCommessa.id_testata_commessa,
#                foreign_keys=[RigaPrimaNota.id_testata_prima_nota],
                cascade="all, delete"),
        "cli": relation(Cliente,primaryjoin=
                t_testatacommessa.c.id_cliente==Cliente.id,
                backref="testata_commessa"),

                },
                order_by=t_testatacommessa.c.id)
