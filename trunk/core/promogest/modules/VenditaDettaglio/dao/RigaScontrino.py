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

from promogest.dao.Dao import Dao, Base
from promogest.dao.Articolo import Articolo
from promogest.modules.VenditaDettaglio.dao.ScontoScontrino import ScontoScontrino
from promogest.modules.VenditaDettaglio.ui.VenditaDettaglioUtils import scontoRigaScontrinoDel
from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino

class RigaScontrino(Base, Dao):
    try:
        __table__ = Table('riga_scontrino',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
    except:
        __table__ = Table('riga_scontrino', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('prezzo',Numeric(16,4),nullable=True),
                Column('prezzo_scontato',Numeric(16,4),nullable=True),
                Column('quantita',Numeric(16,4),nullable=False),
                Column('descrizione',String(200),nullable=False),
                Column('id_testata_scontrino',Integer,ForeignKey(fk_prefix +"testata_scontrino.id", onupdate="CASCADE", ondelete="CASCADE"),nullable=True),
                Column('id_articolo',Integer, ForeignKey(fk_prefix +"articolo.id", onupdate="CASCADE", ondelete="RESTRICT"),nullable=False),
                schema=params['schema'],
                useexisting =True
                )

    arti = relationship("Articolo") #serve
    srs = relationship("ScontoRigaScontrino",cascade="all, delete") #serve

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def _getScontiRigaScontrino(self):
        self.__dbScontiRigaScontrino = self.srs
        if self.__dbScontiRigaScontrino:
            self.__scontiRigaScontrino = self.__dbScontiRigaScontrino[:]
        else:
            self.__scontiRigaScontrino = None
        return self.__scontiRigaScontrino

    def _setScontiRigaScontrino(self, value):
        if not value:
            self.__scontiRigaScontrino = []
        else:
            self.__scontiRigaScontrino = value
    sconti = property(_getScontiRigaScontrino, _setScontiRigaScontrino)

    @property
    def valore_sconto(self):
        if self.srs:
            return self.srs[0].valore
        else:
            return []

    @property
    def tipo_sconto(self):
        if self.srs:
            return self.srs[0].tipo_sconto
        else:
            return []

    @property
    def codice_articolo(self):
        """ esempio di funzione  unita alla property """
        if self.arti: return self.arti.codice
        else: return ""

    @property
    def iva_articolo(self):
        """ esempio di funzione  unita alla property """
        if self.arti: return self.arti.percentuale_aliquota_iva
        else: return ""

    @property
    def codice_a_barre(self):
        """ esempio di funzione  unita alla property """
        if self.arti: return self.arti.codice_a_barre
        else: return ""

    def filter_values(self,k,v):
        if k == 'id':
            dic= {k: RigaScontrino.__table__.c.id ==v}
        elif k == 'idArticolo':
            dic = {k: RigaScontrino.__table__.c.id_articolo==v}
        elif k == 'idTestataScontrino':
            dic = {k: RigaScontrino.__table__.c.id_testata_scontrino==v}
        return  dic[k]

    def persist(self):
        params['session'].add(self)
        params['session'].commit()

        #cancellazione sconti associati alla riga
        #scontoRigaScontrinoDel(id=self.id)
        if self.__scontiRigaScontrino:
            for rigasconto in self.__scontiRigaScontrino:
                #annullamento id dello sconto
                rigasconto._resetId()
                #associazione allo sconto della riga
                rigasconto.id_riga_scontrino = self.id
                #salvataggio sconto
                rigasconto.persist()
