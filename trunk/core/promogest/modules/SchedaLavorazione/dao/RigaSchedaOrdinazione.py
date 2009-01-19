# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.dao.Dao import Dao
from promogest.Environment import *
from decimal import *
from promogest.modules.SchedaLavorazione.dao.ScontoRigaScheda import ScontoRigaScheda

from promogest.ui.utils import *


class RigaSchedaOrdinazione(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

        self.__scontiRigaScheda = None
        self.__dbScontiRigaScheda = None
        # usata per mantenere il valore del codice articolo fornitore proveniente da un
        # documento o movimento di carico, per salvare la fornitura
        self.__codiceArticoloFornitore = None


    def _getScontiRigaScheda(self):
        if self.__dbScontiRigaScheda is None:
            self.__dbScontiRigaScheda = promogest.modules.Stampalux.dao.ScontoRigaScheda.select(Environment.connection, self.id, immediate=True)
        if self.__scontiRigaScheda is None:
            self.__scontiRigaScheda = self.__dbScontiRigaScheda[:]
        return self.__scontiRigaScheda


    def _setScontiRigaScheda(self, value):
        self.__scontiRigaScheda = value

    sconti = property(_getScontiRigaScheda, _setScontiRigaScheda)

    def _getStringaScontiRigaScheda(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiRigaScheda(), self.applicazione_sconti)
        return getStringaSconti(listSconti)

    stringaSconti = property(_getStringaScontiRigaScheda)


    def _getCodiceArticoloFornitore(self):
        return self.__codiceArticoloFornitore

    def _setCodiceArticoloFornitore(self, value):
        self.__codiceArticoloFornitore = value

    codiceArticoloFornitore = property(_getCodiceArticoloFornitore, _setCodiceArticoloFornitore)


    def _getTotaleRiga(self):
        # Il totale e' ivato o meno a seconda del prezzo
        if (self.moltiplicatore is None) or (self.moltiplicatore == 0):
            self.moltiplicatore = 1
        self.valore_unitario_netto = Decimal(str(self.valore_unitario_netto)).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
        totaleRiga = self.valore_unitario_netto * Decimal(str(self.quantita)) * Decimal(str(self.moltiplicatore))
        return totaleRiga.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)


    totaleRiga = property(_getTotaleRiga)


    def _getAliquotaIva(self):
        # Restituisce la denominazione breve dell'aliquota iva
        _denominazioneBreveAliquotaIva = '%2.0f' % (self.percentuale_iva or 0)
        daoArticolo = promogest.dao.Articolo.Articolo(Environment.connection, self.id_articolo)
        if daoArticolo is not None:
            if daoArticolo.id_aliquota_iva is not None:
                daoAliquotaIva = promogest.dao.AliquotaIva.AliquotaIva(Environment.connection,
                                                                       daoArticolo.id_aliquota_iva)
                if daoAliquotaIva is not None:
                    _denominazioneBreveAliquotaIva = daoAliquotaIva.denominazione_breve or ''
        if (_denominazioneBreveAliquotaIva == '0' or _denominazioneBreveAliquotaIva == '00'):
            _denominazioneBreveAliquotaIva = ''

        return _denominazioneBreveAliquotaIva

    aliquota = property(_getAliquotaIva)


    def persist(self, conn):
        if conn is None:
            raise NotImplementedError, 'Connection must be passed'

        #salvataggio riga
        Dao.persist(self, conn)

        #cancellazione sconti associati alla riga
        conn.execStoredProcedure('ScontiRigaSchedaDel', (self.id, ))

        if self.__scontiRigaScheda is not None:
            for i in range(0, len(self.__scontiRigaScheda)):
                #annullamento id dello sconto
                self.__scontiRigaScheda[i]._resetId()
                #associazione allo sconto della riga
                self.__scontiRigaScheda[i].id_riga_scheda = self.id
                #salvataggio sconto
                self.__scontiRigaScheda[i].persist(conn)

    def filter_values(self,k,v):
        dic= {'id':rigaschedaordinazione.c.id ==v}
        return  dic[k]


rigaschedaordinazione=Table('riga_scheda_ordinazione',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)

std_mapper = mapper(RigaSchedaOrdinazione, rigaschedaordinazione, properties={},
                                    order_by=rigaschedaordinazione.c.id)

