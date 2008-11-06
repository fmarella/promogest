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

import promogest.dao.Dao
from promogest.dao.Dao import Dao
from promogest import Environment

"""
CREATE TABLE colori_stampa (
    id                      BIGSERIAL   NOT NULL PRIMARY KEY
    ,denominazione          VARCHAR(50) NOT NULL
    ,UNIQUE (id, denominazione)
);
"""



class ColoreStampa(Dao):
    """
    Duplicazione dati listino articolo associato a scheda ordinazione
    per eventuali variazioni  pezzo ed inserimento quantità
    """

    def __init__(self,connection, id=None):
        Dao.__init__(self, connection, 'ColoreStampaGet', 'ColoreStampaSet',\
                                    'ColoreStampaDel',
                                    ('id', ), (id, ))

def select(connection, orderBy = None, denominazione=None,  offset=0,\
                    batchSize=5, immediate=False):
    """ Seleziona le associazioni articoli """

    cursor = connection.execStoredProcedure('ColoreStampaSel',
                                            (orderBy, denominazione, offset, batchSize),
                                            returnCursor=True)

    if immediate:
        return promogest.dao.Dao.select(cursor=cursor, daoClass=ColoreStampa)
    else:
        return (cursor, ColoreStampa)

def count(connection, denominazione=None):
    """ Conta gli articoli """
    return connection.execStoredProcedure('ColoreStampaSel',
                                          (denominazione,),
                                          countResults = True)
