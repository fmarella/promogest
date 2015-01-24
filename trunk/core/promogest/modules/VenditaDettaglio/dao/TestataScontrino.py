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
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.CCardType import CCardType
from promogest.dao.Magazzino import Magazzino
from promogest.dao.User import User
from promogest.dao.Cliente import Cliente
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoTestataScontrino import ScontoTestataScontrino
from promogest.modules.VenditaDettaglio.dao.TestataScontrinoCliente import TestataScontrinoCliente
from promogest.modules.VenditaDettaglio.dao.Pos import Pos
from promogest.lib.utils import *



class TestataScontrino(Base, Dao):
    try:
        __table__ = Table('testata_scontrino',
                    params['metadata'],
                    schema = params['schema'],
                    autoload=True)
    except:
        __table__ = Table('testata_scontrino', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('data_inserimento',DateTime,ColumnDefault(datetime.datetime.now),nullable=False),
                Column('totale_scontrino',Numeric(16,4),nullable=False),
                Column('totale_contanti',Numeric(16,4),nullable=False),
                Column('totale_assegni',Numeric(16,4),nullable=False),
                Column('totale_carta_credito',Numeric(16,4),nullable=False),
                Column('id_magazzino',Integer,ForeignKey(fk_prefix + "magazzino.id", onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_pos',Integer,ForeignKey(fk_prefix +"pos.id", onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_ccardtype',Integer,ForeignKey(fk_prefix +"credit_card_type.id", onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_user',Integer),
                Column('id_testata_movimento',Integer,ForeignKey(fk_prefix + "testata_movimento.id", onupdate="CASCADE", ondelete="RESTRICT")),
                schema=params['schema'],
                )

    cctypee = relationship("CCardType")
    mag = relationship("Magazzino")
    poss = relationship("Pos")
    testatamovimento = relationship("TestataMovimento", backref="testata_scontrino") #serve
    riga_scontr = relationship("RigaScontrino",backref="testata_scontrino",cascade="all, delete") #serve
    STS = relationship("ScontoTestataScontrino", backref="TS",cascade="all, delete") #serve

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    @reconstructor
    def init_on_load(self):
        self.__dbScontiScontrino = []
        self.__righeScontrino = []
        self.__scontiTestataScontrino = []
        self.__idCliTs = None

    def _getRigheScontrino(self):
        self.__dbRigheScontrino = self.riga_scontr
        self.__righeScontrino = self.__dbRigheScontrino[:]
        return self.__righeScontrino

    def _setRigheScontrino(self, value):
        self.__righeScontrino = value

    righe = property(_getRigheScontrino, _setRigheScontrino)

    def _idClienteTestata(self):
        self.__idCliTs = TestataScontrinoCliente().select(id_testata_scontrino = self.id)
        if self.__idCliTs:
            return self.__idCliTs[0].id_cliente
        else:
            return None
    id_cliente_testata_scontrino = property(_idClienteTestata)

    def _clienteTestata(self):
        if self._idClienteTestata():
            return Cliente().getRecord(id=self._idClienteTestata())
        else:
            return None
    cliente_testata_scontrino = property(_clienteTestata)

    @property
    def data_movimento(self):
        if self.testatamovimento: return self.testatamovimento.data_movimento
        else: return ""

    @property
    def numero_movimento(self):
        if self.testatamovimento: return self.testatamovimento.numero
        else: return ""

    @property
    def operatore(self):
        if self.id_user:
            operatore = User().getRecord(id=self.id_user)
            if operatore:
                return operatore.username
        else:
            return "NON DISPONIBILE"

    def _getScontiTestataScontrino(self):
        if self.id:
            self.__dbScontiTestataScontrino = self.STS
            self.__scontiTestataScontrino = self.__dbScontiTestataScontrino
        else:
            self.__scontiTestataScontrino = []
        return self.__scontiTestataScontrino

    def _setScontiTestataScontrino(self, value):
        self.__scontiTestataScontrino = value
    sconti = property(_getScontiTestataScontrino, _setScontiTestataScontrino)

    def _getStringaScontiTestataScontrino(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiTestataScontrino(), self.applicazione_sconti)
        return getStringaSconti(listSconti)
    stringaSconti = property(_getStringaScontiTestataScontrino)

    def filter_values(self, k, v):
        if k == 'id':
            dic= {k: TestataScontrino.__table__.c.id ==v}
        elif k == 'idTestataMovimento':
            dic= {k: TestataScontrino.__table__.c.id_testata_movimento==v}
        elif k == 'daData':
            dic = {k: TestataScontrino.__table__.c.data_inserimento >= v}
        elif k == 'aData':
            dic = {k: TestataScontrino.__table__.c.data_inserimento <= v}
        elif k == 'idMagazzino':
            dic = {k: TestataScontrino.__table__.c.id_magazzino == v}
        elif k == 'idPuntoCassa':
            dic = {k: TestataScontrino.__table__.c.id_pos == v}
        elif k== 'idArticolo':
            dic = {k: and_(TestataScontrino.__table__.c.id==t_riga_scontrino.c.id_testata_scontrino, t_riga_scontrino.c.id_articolo==v)}
        elif k=='idArticoloList':
            dic={ k :and_(TestataScontrino.__table__.c.id==t_riga_scontrinoo.c.id_testata_scontrino, t_riga_scontrino.c.id_articolo.in_(v))}
        elif k=='idCliente':
            dic={ k :and_(TestataScontrino.__table__.c.id==TestataScontrinoCliente.id_testata_scontrino, TestataScontrinoCliente.id_cliente ==v)}
        return  dic[k]

    def update(self):
        return

    def persist(self, chiusura=False):

        #salvataggio testata scontrino
        params['session'].add(self)
        self.commit()
        #self.scontiTestataScontrinoDel(id=self.id)
        #se siamo in chiusura fiscale non serve che vengano toccati i dati delle righe
        if not chiusura:
            if self.__righeScontrino:
                #rigaScontrinoDel(id=self.id)
                #cancellazione righe associate alla testata
                for riga in self.__righeScontrino:
                    #annullamento id della riga
                    riga._resetId()
                    #associazione alla riga della testata
                    riga.id_testata_scontrino = self.id
                    #salvataggio riga
                    riga.persist()
            if self.scontiSuTotale:
                self.scontiTestataScontrinoDel(id=self.id)
                for scontisutot in self.scontiSuTotale:
                    scontisutot.id_testata_scontrino = self.id
                    scontisutot.persist()

    def scontiTestataScontrinoDel(self, id=None):
        """
        Cancella gli sconti associati ad un documento
        """
        row = self.STS
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
            return True
