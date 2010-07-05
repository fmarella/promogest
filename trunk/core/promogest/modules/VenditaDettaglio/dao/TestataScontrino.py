# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.CCardType import CCardType
from promogest.dao.Magazzino import Magazzino
from promogest.dao.User import User
from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino
from promogest.modules.VenditaDettaglio.dao.ScontoTestataScontrino import ScontoTestataScontrino
from promogest.modules.VenditaDettaglio.dao.Pos import Pos
from promogest.ui.utils import *


class TestataScontrino(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    @reconstructor
    def init_on_load(self):
        self.__dbScontiScontrino = []
        self.__righeScontrino = []
        self.__scontiTestataScontrino = []

    def _getRigheScontrino(self):
        self.__dbRigheScontrino = RigaScontrino().select(idTestataScontrino=self.id, batchSize=None)
        self.__righeScontrino = self.__dbRigheScontrino[:]
        return self.__righeScontrino

    def _setRigheScontrino(self, value):
        self.__righeScontrino = value

    righe = property(_getRigheScontrino, _setRigheScontrino)

    def _dataMovimento(self):
        if self.testatamovimento: return self.testatamovimento.data_movimento
        else: return ""
    data_movimento=property(_dataMovimento)

    def _numeroMovimento(self):
        if self.testatamovimento: return self.testatamovimento.numero
        else: return ""
    numero_movimento=property(_numeroMovimento)

    def _getScontiTestataScontrino(self):
        if self.id:
            self.__dbScontiTestataScontrino = ScontoTestataScontrino().select(join = ScontoTestataScontrino.TS,
                                                                                idScontoTestataScontrino=self.id,
                                                                                batchSize=None)
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
            dic= {k: testata_scontrino.c.id ==v}
        elif k == 'idTestataMovimento':
            dic= {k: testata_scontrino.c.id_testata_movimento==v}
        elif k == 'daData':
            dic = {k: testata_scontrino.c.data_inserimento >= v}
        elif k == 'aData':
            dic = {k: testata_scontrino.c.data_inserimento <= v}
        elif k == 'idMagazzino':
            dic = {k: testata_scontrino.c.id_magazzino == v}
        elif k == 'idPuntoCassa':
            dic = {k: testata_scontrino.c.id_pos == v}
        elif k== 'idArticolo':
            dic = {k: and_(testata_scontrino.c.id==riga_scontrinoo.c.id_testata_scontrino, riga_scontrinoo.c.id_articolo==v)}
        return  dic[k]

    def update(self):
        return

    def persist(self, chiusura=False):

        #salvataggio testata scontrino
        params['session'].add(self)
        params['session'].commit()

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
        params['session'].flush()

    def scontiTestataScontrinoDel(self, id=None):
        """
        Cancella gli sconti associati ad un documento
        """
        row = ScontoTestataScontrino().select(idScontoTestataScontrino= id,
                                                        offset = None,
                                                        batchSize = None,
                                                        orderBy=ScontoTestataScontrino.id_testata_scontrino)
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
            return True

riga_scontrinoo=Table('riga_scontrino',
                params['metadata'],
                schema = params['schema'],
                autoload=True)

testata_scontrino=Table('testata_scontrino',
                    params['metadata'],
                    schema = params['schema'],
                    autoload=True)

std_mapper = mapper(TestataScontrino, testata_scontrino,properties={
        "cctypee":relation(CCardType,primaryjoin=(testata_scontrino.c.id_ccardtype==CCardType.id)),
        "mag":relation(Magazzino,primaryjoin=(testata_scontrino.c.id_magazzino==Magazzino.id)),
        "usr":relation(User,primaryjoin=(testata_scontrino.c.id_user==User.id)),
        "poss":relation(Pos,primaryjoin=(testata_scontrino.c.id_pos==Pos.id)),
        "testatamovimento": relation(TestataMovimento,primaryjoin=
                (testata_scontrino.c.id_testata_movimento==TestataMovimento.id), backref="testata_scontrino"),
        "riga_scontr":relation(RigaScontrino,primaryjoin=RigaScontrino.id_testata_scontrino==testata_scontrino.c.id, backref="testata_scontrino",cascade="all, delete"),
        "STS":relation(ScontoTestataScontrino,primaryjoin = (testata_scontrino.c.id==ScontoTestataScontrino.id_testata_scontrino), backref="TS",cascade="all, delete"),
        }, order_by=testata_scontrino.c.id)
