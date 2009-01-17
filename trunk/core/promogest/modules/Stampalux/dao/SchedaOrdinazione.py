# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
# Author: Francesco <francesco@promotux.it>

import promogest.dao.Dao
from promogest.dao.Dao import Dao
import promogest.modules.Stampalux.dao.RigaSchedaOrdinazione
import promogest.dao.Listino
from promogest.dao.Listino import Listino
from promogest import Environment
from promogest.ui.utils import *

"""
CREATE TABLE schede_ordinazioni
(
  id bigserial NOT NULL ,
  numero int8 NOT NULL,
  nomi_sposi varchar(100),
  mezzo_ordinazione varchar(50),
  mezzo_spedizione varchar(50),
  bomba_in_cliche bool NOT NULL DEFAULT false,
  codice_spedizione varchar(100),
  ricevuta_associata varchar(50),
  fattura bool DEFAULT false,
  documento_saldato bool DEFAULT false,
  operatore varchar(50) NOT NULL,
  provenienza varchar(50),
  disp_materiale bool NOT NULL DEFAULT true,
  applicazione_sconti varchar(20),
  totale_lordo numeric(16,4) DEFAULT 0,
  userid_cliente varchar(50),
  passwd_cliente varchar(15),
  lui_e_lei varchar(50),
  id_colore_stampa int8 NOT NULL,
  id_carattere_stampa int8 NOT NULL,
  id_cliente int8,
  id_magazzino int8,
  CONSTRAINT schede_ordinazioni_pkey PRIMARY KEY (id),
  CONSTRAINT schede_ordinazioni_id_carattere_stampa_fkey FOREIGN KEY (id_carattere_stampa)
      REFERENCES caratteri_stampa (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT schede_ordinazioni_id_cliente_fkey FOREIGN KEY (id_cliente)
      REFERENCES cliente (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT schede_ordinazioni_id_magazzino_fkey FOREIGN KEY (id_magazzino)
      REFERENCES magazzino (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT schede_ordinazioni_id_colore_stampa_fkey FOREIGN KEY (id_colore_stampa)
      REFERENCES colori_stampa (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT schede_ordinazioni_id_key UNIQUE (id, numero)
);

CREATE TABLE contatti_schede (
    id                      BIGSERIAL       NOT NULL PRIMARY KEY
    ,referente              VARCHAR(100)        NULL
    ,prima_email            VARCHAR(100)        NULL
    ,seconda_email          VARCHAR(100)        NULL
    ,telefono               VARCHAR(15)         NULL
    ,cellulare              VARCHAR(15)         NULL
    ,skype                  VARCHAR(30)         NULL
    ,id_scheda              BIGINT          NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
    ,UNIQUE (id,id_scheda)
);

CREATE TABLE datari (
    id                      BIGSERIAL   PRIMARY KEY
    ,matrimonio             date        NOT NULL
    ,presa_in_carico        date        NOT NULL
    ,ordine_al_fornitore    date            NULL
    ,consegna_bozza         date            NULL
    ,spedizione             date            NULL
    ,consegna               date            NULL
    ,ricevuta               date            NULL
    ,id_scheda              BIGINT      NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
    ,UNIQUE (id, id_scheda)
);

CREATE TABLE recapiti_spedizioni (
    id                      BIGSERIAL       NOT NULL PRIMARY KEY
    ,referente              VARCHAR(100)        NULL
    ,presso                 VARCHAR(100)        NULL
    ,via_piazza             VARCHAR(50)         NULL
    ,num_civ                VARCHAR(5)          NULL
    ,zip                    VARCHAR(5)          NULL
    ,localita               VARCHAR(50)         NULL
    ,provincia              VARCHAR(50)         NULL
    ,stato                  VARCHAR(50)         NULL
    ,id_scheda              BIGINT          NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
    ,UNIQUE (id, id_scheda)
);

CREATE TABLE note_schede (
    id                      BIGSERIAL       NOT NULL PRIMARY KEY
    ,note_text              text                NULL
    ,note_spedizione        varchar(300)        NULL
    ,note_fornitore         varchar(300)        NULL
    ,note_final             varchar(300)        NULL
    ,id_scheda              BIGINT          NOT NULL REFERENCES schede_ordinazioni(id) ON UPDATE CASCADE ON DELETE CASCADE
    ,UNIQUE (id, id_scheda)
);

"""


class SchedaOrdinazione(Dao):
    """
    Fornisce nuove funzionalit� abbinate alla personalizzazione "Stampalux"
    """

    def __init__(self, connection, idScheda = None):
        Dao.__init__(self, connection,
                         'SchedaOrdinazioneGet', 'SchedaOrdinazioneSet', 'SchedaOrdinazioneDel',
                         ('id', ), (idScheda, ))
        self.__dbScontiSchedaOrdinazione = None
        self.__scontiSchedaOrdinazione = None
        self.__dbRigheSchedaOrdinazione = None
        self.__righeSchedaOrdinazione = None
        self.__dbPromemoriaSchedaOrdinazione = None
        self.__promemoriaSchedaOrdinazione = None

    def _getRigheSchedaOrdinazione(self):
        if self.__dbRigheSchedaOrdinazione is None:
            self.__dbRigheSchedaOrdinazione = promogest.modules.Stampalux.dao.RigaSchedaOrdinazione.select(Environment.connection,
                    self.id, immediate=True)
        if self.__righeSchedaOrdinazione is None:
            self.__righeSchedaOrdinazione = self.__dbRigheSchedaOrdinazione[:]
        return self.__righeSchedaOrdinazione

    def _setRigheSchedaOrdinazione(self, value):
        self.__righeSchedaOrdinazione = value

    righe = property(_getRigheSchedaOrdinazione, _setRigheSchedaOrdinazione)

    def _getScontiSchedaOrdinazione(self):
        if self.__dbScontiSchedaOrdinazione is None:
            self.__dbScontiSchedaOrdinazione = promogest.modules.Stampalux.dao.ScontoSchedaOrdinazione.select(Environment.connection,
                    self.id, immediate=True)
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
            self.__dbPromemoriaSchedeOrdinazioni = promogest.modules.Stampalux.dao.PromemoriaSchedaOrdinazione.select(Environment.connection,
                                                                          idScheda=self.id, immediate=True)
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

def select(connection, orderBy='numero', daNumero=None, aNumero=None,\
                    coloreStampa=None, carattereStampa=None, daDataMatrimonio=None,\
                    aDataMatrimonio=None, daDataSpedizione=None,\
                    aDataSpedizione=None, daDataConsegna=None,\
                    aDataConsegna=None, daDataScheda=None, aDataScheda=None, operatore=None,\
                    referente=None, nomiSposi=None, codiceSpedizione=None,\
                    ricevutaAssociata=None, documentoSaldato=None,\
                    idCliente=None, offset=0, batchSize=5, immediate=False):
    """
    Seleziona le schede ordinazione dal database
    """
    cursor = connection.execStoredProcedure('SchedaOrdinazioneSel',
                                            (orderBy, daNumero, aNumero,coloreStampa,
                                            carattereStampa, daDataMatrimonio, aDataMatrimonio,
                                            daDataSpedizione, aDataSpedizione, daDataConsegna,
                                            aDataConsegna, daDataScheda, aDataScheda,
                                            operatore, referente, nomiSposi,
                                            codiceSpedizione, ricevutaAssociata,
                                            documentoSaldato, idCliente, offset, batchSize),
                                            returnCursor=True)

    if immediate:
        return promogest.dao.Dao.select(cursor=cursor, daoClass=SchedaOrdinazione)
    else:
        return (cursor, SchedaOrdinazione)

def count( connection, daNumero=None, aNumero=None,
                    coloreStampa=None, carattereStampa=None,
                    daDataMatrimonio=None, aDataMatrimonio=None,
                    daDataSpedizione=None, aDataSpedizione=None,
                    daDataConsegna=None, aDataConsegna=None,
                    daDataScheda=None, aDataScheda=None,
                    operatore=None, referente=None, nomiSposi=None,
                    codiceSpedizione=None, ricevutaAssociata=None,
                    documentoSaldato=None, idCliente=None):
    """
    conta le schede ordinazione nel database secondo nessun criterio :D
    """
    return connection.execStoredProcedure('SchedaOrdinazioneSel',
                                            ( daNumero, aNumero,coloreStampa,
                                            carattereStampa, daDataMatrimonio, aDataMatrimonio,
                                            daDataSpedizione, aDataSpedizione, daDataConsegna,
                                            aDataConsegna, daDataScheda, aDataScheda,
                                            operatore, referente, nomiSposi,
                                            codiceSpedizione, ricevutaAssociata,
                                            documentoSaldato, idCliente),
                                            countResults = True)
