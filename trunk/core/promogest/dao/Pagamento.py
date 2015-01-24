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
from promogest.lib.alembic.migration import MigrationContext
from promogest.lib.alembic.operations import Operations
from promogest.lib.alembic import op


class Pagamento(Base, Dao):
    try:
        __table__ = Table('pagamento',
                  params['metadata'],
                  schema=params['schema'],
                  autoload=True)
    except:
        from data.pagamento import t_pagamento
        __table__ = t_pagamento

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "denominazione":
            dic= {k : Pagamento.__table__.c.denominazione.ilike("%"+v+"%")}
        if k == "denominazioneEM":
            dic= {k : Pagamento.__table__.c.denominazione == v}
        elif k == "tipo":
            dic= {k : Pagamento.__table__.c.tipo == v} # cassa o banca
        return  dic[k]

    @property
    def aliquota_iva(self):
        if self.id_aliquota_iva:
            from promogest.dao.CachedDaosDict import CachedDaosDict
            cache = CachedDaosDict()
            if self.id_aliquota_iva in cache['aliquotaiva']:
                return cache['aliquotaiva'][self.id_aliquota_iva][0].denominazione_breve or ""
            else:
                return ""
        else:
            return ""

    @property
    def perc_aliquota_iva(self):
        if self.id_aliquota_iva:
            from promogest.dao.CachedDaosDict import CachedDaosDict
            cache = CachedDaosDict()
            if self.id_aliquota_iva in cache['aliquotaiva']:
                return cache['aliquotaiva'][self.id_aliquota_iva][0].percentuale or ""
            else:
                return 0
        else:
            return 0

try:
    Pagamento.__table__.c.codice
except:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.add_column('pagamento', Column('codice', String(4), nullable=True), schema=params["schema"])
    delete_pickle()
    restart_program()


#from promogest.dao.CachedDaosDict import cache_objj
#cache_objj.add(Pagamento, use_key='denominazione')
#cache_obj = cache_objj
