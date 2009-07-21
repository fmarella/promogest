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
from promogest.dao.Articolo import Articolo
from promogest.dao.AliquotaIva import AliquotaIva
#from promogest.modules.SchedaLavorazione.ui.SchedaLavorazioneUtils import *
#from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione
from promogest.ui.utils import *


class RigaSchedaOrdinazione(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

        self.__scontiRigaScheda = None
        self.__dbScontiRigaScheda = None
        # usata per mantenere il valore del codice articolo fornitore proveniente da un
        # documento o movimento di carico, per salvare la fornitura
        self.__codiceArticoloFornitore = None

    @reconstructor
    def init_on_load(self):
        self.__scontiRigaScheda = None
        self.__dbScontiRigaScheda = None
        # usata per mantenere il valore del codice articolo fornitore proveniente da un
        # documento o movimento di carico, per salvare la fornitura
        self.__codiceArticoloFornitore = None


    def _getScontiRigaScheda(self):
        #if self.__dbScontiRigaScheda is None:
        if self.id:
            self.__dbScontiRigaScheda = ScontoRigaScheda().select(idRigaScheda= self.id)
            #if self.__scontiRigaScheda is None:
            self.__scontiRigaScheda = self.__dbScontiRigaScheda[:]
        else:
            self.__scontiRigaScheda = []
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

    def __codiceArticolo(self):
        """ esempio di funzione  unita alla property """
        #a =  params["session"].query(Articolo).with_parent(self).filter(RigaSchedaOrdinazione.id_articolo==Articolo.id).all()
        #if not a:
            #return a
        #else:
            #return a[0].codice
        if self.arti: return self.arti.codice
        else: return ""
    codice_articolo= property(__codiceArticolo)

    def _getAliquotaIva(self):
        # Restituisce la denominazione breve dell'aliquota iva
        _denominazioneBreveAliquotaIva = '%2.0f' % (self.percentuale_iva or 0)
        daoArticolo = Articolo().getRecord(id=self.id_articolo)
        if daoArticolo is not None:
            if daoArticolo.id_aliquota_iva is not None:
                daoAliquotaIva = AliquotaIva().getRecord(id = daoArticolo.id_aliquota_iva)
                if daoAliquotaIva is not None:
                    _denominazioneBreveAliquotaIva = daoAliquotaIva.denominazione_breve or ''
        if (_denominazioneBreveAliquotaIva == '0' or _denominazioneBreveAliquotaIva == '00'):
            _denominazioneBreveAliquotaIva = ''

        return _denominazioneBreveAliquotaIva

    aliquota = property(_getAliquotaIva)

    def scontiRigaSchedaDel(self,id=None):
        """Cancella gli sconti legati ad una riga movimento"""
        row = ScontoRigaScheda().select(idRigaScheda= id,
                                        batchSize = None)
        if row:
            for r in row:
                params['session'].delete(r)
            params["session"].commit()
            return True

    def persist(self):
        params["session"].add(self)
        params["session"].commit()
        #self.scontiRigaSchedaDel(self.id)
        if self.__scontiRigaScheda is not None:
            for row in self.__scontiRigaScheda:
                #annullamento id dello sconto
                #row._resetId()
                #associazione allo sconto della riga
                row.id_riga_scheda = self.id
                #salvataggio sconto
                row.persist()

    def filter_values(self,k,v):
        if k =="id":
            dic= {k:rigaschedaordinazione.c.id ==v}
        elif k =="idSchedaOrdinazione":
            dic = {k:rigaschedaordinazione.c.id_scheda == v}
        elif k =="idArticolo":
            dic = {k:rigaschedaordinazione.c.id_articolo == v}
        return  dic[k]

rigaschedaordinazione=Table('righe_schede_ordinazioni',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)

riga=Table('riga', params['metadata'],schema = params['schema'], autoload=True)

j = join(rigaschedaordinazione, riga)

std_mapper = mapper(RigaSchedaOrdinazione, j, properties={
        'id':[rigaschedaordinazione.c.id, riga.c.id],
        "arti":relation(Articolo,primaryjoin=riga.c.id_articolo==Articolo.id),
            },
                    order_by=rigaschedaordinazione.c.id)

