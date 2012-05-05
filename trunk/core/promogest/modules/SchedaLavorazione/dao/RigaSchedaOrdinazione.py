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
from promogest.dao.Dao import Dao
from promogest.Environment import *
from decimal import *
from promogest.modules.SchedaLavorazione.dao.ScontoRigaScheda import ScontoRigaScheda
from promogest.dao.Articolo import Articolo
from promogest.dao.AliquotaIva import AliquotaIva
#from promogest.modules.SchedaLavorazione.ui.SchedaLavorazioneUtils import *
#from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione
from promogest.lib.utils import *
from promogest.dao.DaoUtils import giacenzaArticolo
from promogest.dao.Riga import Riga

class RigaSchedaOrdinazione(Dao):

    def __init__(self, req=None):
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


#    def _getTotaleRiga(self):
#        # Il totale e' ivato o meno a seconda del prezzo
#        if (self.moltiplicatore is None) or (self.moltiplicatore == 0):
#            self.moltiplicatore = 1
#        self.valore_unitario_netto = Decimal(str(self.valore_unitario_netto)).quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)
#        totaleRiga = self.valore_unitario_netto * Decimal(str(self.quantita)) * Decimal(str(self.moltiplicatore))
#        return totaleRiga.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

#    totaleRiga = property(_getTotaleRiga)

    def __codiceArticolo(self):
        """ esempio di funzione  unita alla property """
        if self.arti: return self.arti.codice
        else: return ""
    codice_articolo= property(__codiceArticolo)

    def _setGiacenzaArticolo(self):
        if self.arti.codice not in ["Stampa", "z-CONTR","z-BONIFICO"]:
            giace =giacenzaArticolo(year=Environment.workingYear,
                                        idMagazzino=self.id_magazzino,
                                        idArticolo=self.id_articolo)[0]
        else:
            giace = 0
        return giace
    giacenza_articolo = property(_setGiacenzaArticolo)

    def _impegnatoSuLavorazione(self):
        if self.arti.codice not in ["Stampa", "z-CONTR","z-BONIFICO"]:
            year = Environment.workingYear
            t=0
            part= Environment.params["session"]\
                .query(Riga.quantita)\
                .filter(and_(schedaordinazione.c.fattura!=True,
                            riga.c.id==rigaschedaordinazione.c.id,
                                rigaschedaordinazione.c.id_scheda == schedaordinazione.c.id,
                                riga.c.id_articolo==self.id_articolo,
                                Articolo.id==self.id_articolo)).all()
            for r in part:
                t +=r[0]
            return t
    impegnato_su_lavorazione = property(_impegnatoSuLavorazione)

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


schedaordinazione=Table('schede_ordinazioni',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)



rigaschedaordinazione=Table('righe_schede_ordinazioni',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)

riga=Table('riga', params['metadata'],schema = params['schema'], autoload=True)

j = join(rigaschedaordinazione, riga)

std_mapper = mapper(RigaSchedaOrdinazione, j, properties={
        'id':[rigaschedaordinazione.c.id, riga.c.id],
        "arti":relation(Articolo,primaryjoin=riga.c.id_articolo==Articolo.id),
        'totaleRiga': column_property(riga.c.quantita * riga.c.moltiplicatore * riga.c.valore_unitario_netto ),
            },
                    order_by=rigaschedaordinazione.c.id)
