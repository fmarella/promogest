# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao, Base

from data.sconto import t_sconto
from data.scontiVenditaDettaglio import t_sconti_vendita_dettaglio
s_svd = join(t_sconto, t_sconti_vendita_dettaglio)

class ScontoVenditaDettaglio(Base, Dao):
    __table__ = s_svd
    id = column_property(t_sconto.c.id, t_sconti_vendita_dettaglio.c.id)

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=='idListino':
            dic = {k: ScontoVenditaDettaglio.__table__.c.id_listino==v}
        elif k=='idArticolo':
            dic = {k: ScontoVenditaDettaglio.__table__.c.id_articolo==v}
        elif k=='dataListinoArticolo':
            dic = {k: ScontoVenditaDettaglio.__table__.c.data_listino_articolo==v}
        return dic[k]
