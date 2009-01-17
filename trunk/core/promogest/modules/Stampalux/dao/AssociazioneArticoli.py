# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.Articolo import Articolo

"""
CREATE TABLE associazioni_articoli(
    id              BIGSERIAL   NOT NULL    PRIMARY KEY
    ,id_padre       BIGINT          NULL    REFERENCES articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,id_figlio      BIGINT          NULL    REFERENCES articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
    ,posizione      INTEGER         NULL
    -- sono tutti riferimenti esterni alla tabella articolo. Questa tabella associa
    -- ad n articoli, n altri articoli della stessa tabella
    ,UNIQUE (id_padre,id_figlio));
"""




class AssociazioneArticoli(Dao):
    """
    Rappresenta un raggruppamento di articoli relazionati ad un unico articolo "padre"
    """
    def __init__(self, connection, id=None):
        Dao.__init__(self, connection,
                                    'AssociazioneArticoloGet','AssociazioneArticoloSet','AssociazioneArticoloDel',
                                    ('id', ), (id, ))

    def persist(self, connection=None):
        """
        Salva l'associazione nel database
        """
        if connection is None:
            if  self._connection is not None:
                self._connection.execStoredProcedure('AssociazioneArticoloSet',
                                                            (self.id ,self.id_associato, self.id_articolo, self.posizione))
            else:
                self.raiseException(NotImplementedError('Object is read-only '
                                                        + '(no connection has '
                                                        + 'been associated)'))
        else:
            connection.execStoredProcedure('AssociazioneArticoloSet',
                                                            (self.id ,self.id_associato, self.id_articolo, self.posizione))

    def delete(self, conn=None, son=False):
        if conn is not None:
            conn.execStoredProcedure(self._delSPName,
                                     (self.id,))
        else:
            if self._connection is None:
                self.raiseException(NotImplementedError('Object is read-only '
                                                        + '(no connection has '
                                                        + 'been associated)'))

            self._connection.execStoredProcedure(self._delSPName,
                                                 (self.id_articolo, son))

def select(connection, idPadre = None, orderBy='posizione, codice', nodo=False,
                    denominazione=None, codice=None,\
                    codiceABarre=None, codiceArticoloFornitore=None,
                    produttore=None, idFamiglia=None,\
                    idCategoria=None, idStato=None,\
                    cancellato=False, offset=0, batchSize=30, immediate=False):
    """ Seleziona le associazioni articoli """

    cursor = connection.execStoredProcedure('associazionearticolosel',\
                                            (nodo, idPadre, orderBy,denominazione, codice,
                                            codiceABarre, codiceArticoloFornitore, produttore,
                                            idFamiglia, idCategoria,idStato, cancellato, offset, batchSize),
                                            returnCursor=True)

    if immediate:
        return promogest.dao.Dao.select(cursor=cursor, daoClass=AssociazioneArticoli)
    else:
        return (cursor, AssociazioneArticoli)

def count(connection, idPadre = None, orderBy=None, nodo=False,
                    denominazione=None, codice=None,\
                    codiceABarre=None, codiceArticoloFornitore=None,
                    produttore=None, idFamiglia=None,\
                    idCategoria=None, idStato=None, cancellato=False,\
                    offset=None, batchSize=None, ):
    """ Conta gli articoli associati"""

    cursor = connection.execStoredProcedure('AssociazioneArticoloSel',\
                                            (nodo, idPadre, None, denominazione, codice, codiceABarre,\
                                            codiceArticoloFornitore, produttore,idFamiglia, idCategoria,idStato,\
                                             cancellato, None, None), countResults=True)
