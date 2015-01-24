# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from promogest.dao.TipoAliquotaIva import TipoAliquotaIva

class AliquotaIva(Base, Dao):
    try:
        __table__ = Table('aliquota_iva', meta,
                        schema=params["schema"], autoload=True)
    except:
        from data.aliquotaIva import t_aliquota_iva
        __table__ = t_aliquota_iva

    __mapper_args__ = {
        'order_by' : "id"
    }

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'denominazione':
            dic = {k: AliquotaIva.__table__.c.denominazione.ilike("%" + v + "%")}
        elif k == "percentuale":
            dic = {k: AliquotaIva.__table__.c.percentuale == v}
        elif k == "idTipo":
            dic = {k: AliquotaIva.__table__.c.id_tipo == v}
        return  dic[k]

    @property
    def tipo_aliquota_iva(self):
        aa = TipoAliquotaIva().getRecord(id=self.id_tipo)
        if aa:
            return aa
        else:
            return None

    @property
    def tipo_ali_iva(self):
        if self.tipo_aliquota_iva:
            return self.tipo_aliquota_iva.denominazione
        else:
            return None
