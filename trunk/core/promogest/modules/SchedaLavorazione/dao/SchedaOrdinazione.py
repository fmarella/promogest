# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author: Francesco <francesco@promotux.it>

from promogest.dao.Dao import Dao
from promogest.dao.Listino import Listino
from promogest.Environment import *
from promogest.ui.utils import *
from promogest.modules.SchedaLavorazione.dao.RigaSchedaOrdinazione import RigaSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.ScontoSchedaOrdinazione import ScontoSchedaOrdinazione
from promogest.modules.SchedaLavorazione.dao.ColoreStampa import ColoreStampa
from promogest.modules.SchedaLavorazione.dao.CarattereStampa import CarattereStampa
from promogest.dao.Cliente import Cliente
from promogest.dao.Magazzino import Magazzino

class SchedaOrdinazione(Dao):
    """ Fornisce nuove funzionalità abbinate alla personalizzazione"
    """

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

        self.__dbScontiSchedaOrdinazione = None
        self.__scontiSchedaOrdinazione = None
        self.__dbRigheSchedaOrdinazione = None
        self.__righeSchedaOrdinazione = None
        self.__dbPromemoriaSchedaOrdinazione = None
        self.__promemoriaSchedaOrdinazione = None

    def _getRigheSchedaOrdinazione(self):
        if self.__dbRigheSchedaOrdinazione is None:
            self.__dbRigheSchedaOrdinazione = RigaSchedaOrdinazione().select(id=self.id, batchSize=None)
        if self.__righeSchedaOrdinazione is None:
            self.__righeSchedaOrdinazione = self.__dbRigheSchedaOrdinazione[:]
        return self.__righeSchedaOrdinazione

    def _setRigheSchedaOrdinazione(self, value):
        self.__righeSchedaOrdinazione = value

    righe = property(_getRigheSchedaOrdinazione, _setRigheSchedaOrdinazione)

    def _getScontiSchedaOrdinazione(self):
        if self.__dbScontiSchedaOrdinazione is None:
            self.__dbScontiSchedaOrdinazione = ScontoSchedaOrdinazione().select(id=self.id,batchSize=None)
        if self.__scontiSchedaOrdinazione is None:
            self.__scontiSchedaOrdinazione = self.__dbScontiSchedaOrdinazione
        return self.__scontiSchedaOrdinazione

    def _setScontiSchedaOrdinazione(self, value):
        self.__scontiSchedaOrdinazione = value

    sconti = property(_getScontiSchedaOrdinazione, _setScontiSchedaOrdinazione)

    def _getStringaScontiSchedaOrdinazione(self):
        (listSconti, applicazione) = getScontiFromDao(self._getScontiSchedaOrdinazione(), self.applicazione_sconti)
        return getStringaSconti(listSconti)

    stringaSconti = property(_getStringaScontiSchedaOrdinazione)

    def _getPromemoriaSchedaOrdinazione(self):
        if self.__dbPromemoriaSchedaOrdinazione is None:
            self.__dbPromemoriaSchedeOrdinazioni = PromemoriaSchedaOrdinazione().select(idScheda=self.id,
                                                                        batchSize=None)
        if self.__promemoriaSchedaOrdinazione is None:
            self.__promemoriaSchedaOrdinazione = self.__dbPromemoriaSchedaOrdinazione
        return self.__promemoriaSchedaOrdinazione

    def _setPromemoriaSchedaOrdinazione(self, value):
        self.__promemoriaSchedaOrdinazione = value

    promemoria = property(_getPromemoriaSchedaOrdinazione, _setPromemoriaSchedaOrdinazione)

    def persist(self):

        #assegnamento della connessione alla scheda e inizio transazione
        self.setConnection(Environment.connection)
        self._connection.startTransaction()

        try:
            #salvataggio scheda ordinazione
            Dao.persist(self, self._connection)

            #cancellazione righe associate alla scheda
            self._connection.execStoredProcedure('RigheSchedaDel',
                    (self.id, ))

            #cancellazione sconti associati alla scheda
            self._connection.execStoredProcedure('ScontiSchedaOrdinazioneDel',
                    (self.id, ))

            #cancellazione promemoria associati alla scheda
            self._connection.execStoredProcedure('PromemoriaSchedaDeleteAll',
                    (self.id, ))

            # salvataggio degli articoli associati alla scheda
            for riga in self.__righeSchedaOrdinazione:
                riga._resetId()
                riga.id_scheda = self.id
                riga.persist(self._connection)

            #salvataggio degli sconti associati alla scheda
            if self.__scontiSchedaOrdinazione is not None:
                for i in range(0, len(self.__scontiSchedaOrdinazione)):
                    #annullamento id dello sconto
                    self.__scontiSchedaOrdinazione[i]._resetId()
                    #associazione allo sconto della testata
                    self.__scontiSchedaOrdinazione[i].id_scheda_ordinazione = self.id
                    #salvataggio sconto
                    self.__scontiSchedaOrdinazione[i].persist(self._connection)

            if self.__promemoriaSchedaOrdinazione is not None:
                if self.data_consegna is None:
                    for promemoria in self.__promemoriaSchedaOrdinazione:
                        promemoria._resetId()
                        promemoria.id_scheda= self.id
                        promemoria.persist(self._connection)
                else:
                    if datetime.date.today <= self.data_consegna:
                        for promemoria in self.__promemoriaSchedaOrdinazione:
                            promemoria._resetId()
                            promemoria.id_scheda= self.id
                            promemoria.persist(self._connection)
                    elif datetime.date.today > self.data_consegna:
                        self.__promemoriaSchedaOrdinazione = None

                    #chiusura positiva transazione
            self._connection.commitTransaction()
        except:
            self._connection.abortTransaction()
            raise

    def filter_values(self,k,v):
        if k=="id":
            dic= {k:schedaordinazione.c.id ==v}
        elif k == 'daDataMatrimonio':
            dic = {k:None}
            #dic = {k:schedaordinazione.c.data_documento >= v}
        elif k== 'aDataMatrimonio':
            dic = {k:scheda_ordinazione.c.data_documento <= v}
        return  dic[k]


schedaordinazione=Table('scheda_ordinazione',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)

std_mapper = mapper(SchedaOrdinazione, schedaordinazione, properties={
                "cli":relation(Cliente,primaryjoin=
                    schedaordinazione.c.id_cliente==Cliente.id, backref="sched_ord"),
                "CARATTSTAM":relation(CarattereStampa,primaryjoin=
                    schedaordinazione.c.id_carattere_stampa==CarattereStampa.id, backref="sched_ord"),
                "COLOSTAMP":relation(ColoreStampa,primaryjoin=
                    schedaordinazione.c.id_colore_stampa==ColoreStampa.id, backref="sched_ord"),
                "magazz":relation(Magazzino,primaryjoin=
                    schedaordinazione.c.id_magazzino==Magazzino.id, backref="sched_ord") },
                order_by=schedaordinazione.c.id)

