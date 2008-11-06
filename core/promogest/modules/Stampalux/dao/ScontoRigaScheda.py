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
CREATE TABLE sconti_righe_schede (
     id                         bigint          NOT NULL PRIMARY KEY REFERENCES sconto ( id ) ON UPDATE CASCADE ON DELETE CASCADE
    ,id_riga_scheda             bigint          NOT NULL REFERENCES righe_schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);
"""


class ScontoRigaScheda(Dao):

    def __init__(self, connection, idScontoRigaScheda = None):
        Dao.__init__(self, connection,
                         'ScontoRigaSchedaGet', 'ScontoRigaSchedaSet', 'ScontoRigaSchedaDel',
                         ('id', ), (idScontoRigaScheda, ))



def select(connection, idRigaScheda=None, immediate=False):
    """ Seleziona gli sconti relativi alla riga della scheda ordinazione"""
    cursor = connection.execStoredProcedure('ScontoRigaSchedaSel',
                                            ('id', idRigaScheda,
                                             None, None),
                                            returnCursor=True)

    if immediate:
        return promogest.dao.Dao.select(cursor=cursor, daoClass=ScontoRigaScheda)
    else:
        return (cursor, ScontoRigaScheda)


def count(connection, idRigaScheda=None):
    """ Conta gli sconti relativi alla riga della scheda ordinazione"""
    return connection.execStoredProcedure('ScontoRigaSchedaSel',
                                          (None, idRigaScheda,
                                           None, None),
                                          countResults = True)
