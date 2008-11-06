# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Marco Pinna) <zoccolodignu@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import promogest.dao.Dao
from promogest.dao.Dao import Dao
from promogest import Environment
from decimal import *
import promogest.modules.Stampalux.dao.ScontoRigaScheda
from promogest.modules.Stampalux.dao.ScontoRigaScheda import ScontoRigaScheda

from promogest.ui.utils import *

"""
CREATE TABLE righe_schede_ordinazioni (
       id                       bigint          NOT NULL PRIMARY KEY REFERENCES riga ( id ) ON UPDATE CASCADE ON DELETE CASCADE
      ,id_scheda                bigint          NOT NULL REFERENCES schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

class RigaSchedaOrdinazione(Dao):

    def __init__(self, connection, idRigaScheda=None):
        Dao.__init__(self, connection,
                         'RigaSchedaGet', 'RigaSchedaSet',
                         'RigaSchedaDel',
                         ('id', ), (idRigaScheda, ))

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

def select(connection, idSchedaOrdinazione=None, immediate=False):
    """ Seleziona le righe documento """
    cursor = connection.execStoredProcedure('RigaSchedaSel',
                                            (None, idSchedaOrdinazione,
                                             None, None),
                                            returnCursor=True)

    if immediate:
        return promogest.dao.Dao.select(cursor=cursor, daoClass=RigaSchedaOrdinazione)
    else:
        return (cursor, RigaSchedaOrdinazione)


def count(connection, idSchedaOrdinazione=None):
    """ Conta le righe documenti """
    return connection.execStoredProcedure('RigaSchedaSel',
                                          (None, idSchedaOrdinazione,
                                           None, None),
                                          countResults = True)

