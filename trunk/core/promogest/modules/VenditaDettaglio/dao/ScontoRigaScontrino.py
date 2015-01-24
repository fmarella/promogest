# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015  by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao, Base

from data.scontoRigaScontrino import t_sconto_riga_scontrino
from data.scontoScontrino import t_sconto_scontrino
ss_srs = join(t_sconto_scontrino, t_sconto_riga_scontrino)

class ScontoRigaScontrino(Base, Dao):
    __table__ = ss_srs
    id = column_property(t_sconto_scontrino.c.id, t_sconto_riga_scontrino.c.id)

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {'id':ScontoRigaScontrino.__table__.c.id ==v,
        'idRigaScontrino':ScontoRigaScontrino.__table__.c.id_riga_scontrino==v,}
        return  dic[k]
