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
from sqlalchemy.orm import mapper, relation
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.TipoAliquotaIva import TipoAliquotaIva


class AliquotaIva(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'denominazione':
            dic = {k: t_aliquota_iva.c.denominazione.ilike("%" + v + "%")}
        elif k == "percentuale":
            dic = {k: t_aliquota_iva.c.percentuale == v}
        elif k == "idTipo":
            dic = {k: t_aliquota_iva.c.id_tipo == v}
        return  dic[k]

    def _tipoAliquota(self):
        if self.tipo_aliquota_iva:
            return self.tipo_aliquota_iva.denominazione
        else:
            return None
    tipo_ali_iva = property(_tipoAliquota)

t_aliquota_iva = Table('aliquota_iva', meta,
        schema=params["schema"], autoload=True)

std_mapper = mapper(AliquotaIva, t_aliquota_iva, properties={
        'tipo_aliquota_iva': relation(TipoAliquotaIva, backref='aliquota_iva')
            }, order_by=t_aliquota_iva.c.id)
