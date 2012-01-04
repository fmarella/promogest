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
from promogest.Environment import params
from promogest.dao.Dao import Dao
#from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione


class ScontoSchedaOrdinazione(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= { k :scontoschedaordinazione.c.id == v}
        elif k== 'idSchedaOrdinazione' or k == "idScontoSchedaOrdinazione":
            dic ={k:scontoschedaordinazione.c.id_scheda_ordinazione==v}
        return  dic[k]

sconto=Table('sconto', params['metadata'], schema = params['schema'], autoload=True)

scontoschedaordinazione=Table('sconti_schede_ordinazioni',params['metadata'],schema = params['schema'],
                                        autoload=True)
j = join(sconto, scontoschedaordinazione)

std_mapper = mapper(ScontoSchedaOrdinazione,j, properties={
            'id':[sconto.c.id, scontoschedaordinazione.c.id],
            }, order_by=scontoschedaordinazione.c.id)
