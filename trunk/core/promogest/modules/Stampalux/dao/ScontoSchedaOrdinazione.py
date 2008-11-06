# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
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
CREATE TABLE sconti_schede_ordinazioni (
     id                         bigint          NOT NULL PRIMARY KEY REFERENCES sconto ( id ) ON UPDATE CASCADE ON DELETE CASCADE
    ,id_scheda_ordinazione       bigint          NOT NULL REFERENCES schede_ordinazioni ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

class ScontoSchedaOrdinazione(Dao):

    def __init__(self, connection, idScontoSchedaOrdinazione = None):
        Dao.__init__(self, connection,
                         'ScontoSchedaOrdinazioneGet', 'ScontoSchedaOrdinazioneSet', 'ScontoSchedaOrdinazioneDel',
                         ('id', ), (idScontoSchedaOrdinazione, ))



def select(connection, idSchedaOrdinazione=None, immediate=False):
    """ Seleziona gli sconti relativi alla scheda del ordinazione """
    cursor = connection.execStoredProcedure('ScontoSchedaOrdinazioneSel',
                                            ('id', idSchedaOrdinazione,
                                             None, None),
                                            returnCursor=True)

    if immediate:
        return promogest.dao.Dao.select(cursor=cursor, daoClass=ScontoSchedaOrdinazione)
    else:
        return (cursor, ScontoSchedaOrdinazione)


def count(connection, idSchedaOrdinazione=None):
    """ Conta gli sconti relativi alla scheda del ordinazione """
    return connection.execStoredProcedure('ScontoSchedaOrdinazioneSel',
                                          (None, idSchedaOrdinazione,
                                           None, None),
                                          countResults = True)
