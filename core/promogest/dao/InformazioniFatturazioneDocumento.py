# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>
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

