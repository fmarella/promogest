# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
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

import Dao
from promogest import Environment
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo

class AssociazioneArticoli(Dao.Dao):
    """
    Rappresenta un raggruppamento di articoli relazionati ad un unico articolo "padre"
    """
    def __init__(self, connection, id=None):
        Dao.Dao.__init__(self, connection,
                                    'DistintaBaseGet','DistintaBaseSet','DistintaBaseDel',
                                    ('id', ), (id, ))

    def persist(self, connection=None):
        """
        Salva la disinta nel database
        """
        if connection is None:
            if  self._connection is not None:
                self._connection.execStoredProcedure('DistintaBaseSet',
                                                            (self.id ,self.id_associato, self.id_articolo))
            else:
                self.raiseException(NotImplementedError('Object is read-only '
                                                        + '(no connection has '
                                                        + 'been associated)'))
                return
        else:
            connection.execStoredProcedure('AssociazioneArticoloSet',
                                                            (self.id ,self.id_associato, self.id_articolo))
    
    def delete(self, conn=None, son=False):
        if conn is not None:
            conn.execStoredProcedure(self._delSPName,
                                     (self.id_articolo, son))
        else:
            if self._connection is None:
                self.raiseException(NotImplementedError('Object is read-only '
                                                        + '(no connection has '
                                                        + 'been associated)'))
                return
            self._connection.execStoredProcedure(self._delSPName,
                                                 (self.id_articolo, son))

def select(connection, idPadre = None, orderBy='codice', nodo=False,
                    denominazione=None, codice=None,\
                    codiceABarre=None, codiceArticoloFornitore=None,
                    produttore=None, idFamiglia=None,\
                    idCategoria=None, idStato=None,
                    cancellato=False, offset=0, batchSize=5, immediate=False):
    """ Seleziona le associazioni articoli """

    cursor = connection.execStoredProcedure('DistintaBasesel',\
                                            (nodo, idPadre, orderBy,denominazione, codice,
                                            codiceABarre, codiceArticoloFornitore, produttore,
                                            idFamiglia, idCategoria,idStato, cancellato, offset, batchSize),
                                            returnCursor=True)

    if immediate:
        return Dao.select(cursor=cursor, daoClass=AssociazioneArticoli)
    else:
        return (cursor, AssociazioneArticoli)

def count(connection, idPadre = None, orderBy=None, nodo=False,
                    denominazione=None, codice=None,\
                    codiceABarre=None, codiceArticoloFornitore=None,
                    produttore=None, idFamiglia=None,\
                    idCategoria=None, idStato=None, cancellato=False, offset=0, batchSize=5, ):
    """ Conta gli articoli associati"""

    cursor = connection.execStoredProcedure('DistintaBaseSel',\
                                            (nodo, idPadre, None, denominazione, codice, codiceABarre,\
                                            codiceArticoloFornitore, produttore,idFamiglia, idCategoria,idStato,\
                                             cancellato, None, None), countResults=True)
