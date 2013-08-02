# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.


from sqlalchemy import Table
from sqlalchemy.orm import mapper, join
from promogest.Environment import *

try:
    t_sconto_riga_documento=Table('sconto_riga_documento',
                        params['metadata'],
                        schema = params['schema'],
                        autoload=True)
except:
    from data.rigaDocumento import t_riga_documento
    from data.scontoRigaDocumento import t_sconto_riga_documento

from Dao import Dao
from promogest.dao.Sconto import t_sconto

class ScontoRigaDocumento(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':t_sconto_riga_documento.c.id ==v,
            'idRigaDocumento':t_sconto_riga_documento.c.id_riga_documento==v,}
        return  dic[k]


std_mapper = mapper(ScontoRigaDocumento,join(t_sconto, t_sconto_riga_documento), properties={
    'id':[t_sconto.c.id, t_sconto_riga_documento.c.id],
    }, order_by=t_sconto_riga_documento.c.id)
