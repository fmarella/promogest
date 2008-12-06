# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>


import Dao
from promogest import Environment

class InformazioniFatturazioneDocumento(Dao.Dao):

    def __init__(self, connection, idFattura=None):
        Dao.Dao.__init__(self, connection,
                         'InformazioniFatturazioneDocumentoGet', 'InformazioniFatturazioneDocumentoSet', 'InformazioniFatturazioneDocumentoDel',
                         ('id_fattura', ), (idFattura, ))


    def persist(self, conn):
        if conn is None:
            raise NotImplementedError, 'Connection must be passed'

        #salvataggio riga
        Dao.Dao.persist(self, conn)



def select(connection, idFattura=None, idDDT=None, immediate=False):
    """ 
    Seleziona le informazioni sulle fatture desiderate
    """

    cursor = connection.execStoredProcedure('InformazioniFatturazioneDocumentoSel',
                                            (idFattura,
                                             idDDT),
                                            returnCursor=True)

    if immediate:
        return Dao.select(cursor=cursor, daoClass=InformazioniFatturazioneDocumento)
    else:
        return (cursor, InformazioniFatturazioneDocumento)

