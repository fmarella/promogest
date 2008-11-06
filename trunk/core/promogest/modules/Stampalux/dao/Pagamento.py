# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Authors: Andrea Argiolas <andrea@promotux.it>
#               Dr astico (Pinna Marco) <zoccolodignu@gmail.com>
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



class Pagamento(Dao.Dao):

    def __init__(self, connection, idPagamento = None):
        Dao.Dao.__init__(self, connection,
                        'PagamentoGet', 'PagamentoSet', 'PagamentoDel',
                        ('id', ), (idPagamento, ))



def select(connection, denominazione=None, orderBy='denominazione',
           offset=0, batchSize=5, immediate=False):
    """ Seleziona i pagamenti """
    cursor = connection.execStoredProcedure('PagamentoSel',
                                            (orderBy, denominazione,
                                             offset, batchSize),
                                            returnCursor=True)

    if immediate:
        return Dao.select(cursor=cursor, daoClass=Pagamento)
    else:
        return (cursor, Pagamento)


def count(connection, denominazione=None):
    """ Conta i pagamenti """
    return connection.execStoredProcedure('PagamentoSel',
                                          (None, denominazione,
                                           None, None),
                                          countResults = True)
