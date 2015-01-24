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



from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *

from promogest.dao.Dao import Dao, Base

from data.sconto import t_sconto
from data.scontoTestataDocumento import t_sconto_testata_documento
s_std = join(t_sconto, t_sconto_testata_documento)

class ScontoTestataDocumento(Base, Dao):
    __table__ = s_std
    id = column_property(t_sconto.c.id, t_sconto_testata_documento.c.id)

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= { k :ScontoTestataDocumento.__table__.c.id == v}
        elif k== 'idScontoTestataDocumento':
            dic ={k:ScontoTestataDocumento.__table__.c.id_testata_documento==v}
        return  dic[k]
