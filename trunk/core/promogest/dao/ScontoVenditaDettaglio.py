# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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
from Dao import Dao
from Sconto import t_sconto


class ScontoVenditaDettaglio(Dao):
    """  """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=='idListino':
            dic = {k: t_sconti_vendita_dettaglio.c.id_listino==v}
        elif k=='idArticolo':
            dic = {k: t_sconti_vendita_dettaglio.c.id_articolo==v}
        elif k=='dataListinoArticolo':
            dic = {k: t_sconti_vendita_dettaglio.c.data_listino_articolo==v}
        return dic[k]

t_sconti_vendita_dettaglio = Table('sconti_vendita_dettaglio',
                                   params['metadata'],
                                   schema=params['schema'],
                                   autoload=True)

std_mapper = mapper(ScontoVenditaDettaglio,
    join(t_sconto, t_sconti_vendita_dettaglio),
    properties={
        "id": [t_sconto.c.id, t_sconti_vendita_dettaglio.c.id]
    },
    order_by=t_sconti_vendita_dettaglio.c.id)