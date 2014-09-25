# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

from sqlalchemy import Table, Column, String
from sqlalchemy.orm import mapper
from promogest.Environment import params, engine, delete_pickle, restart_program
from Dao import Dao

from promogest.lib.alembic.migration import MigrationContext
from promogest.lib.alembic.operations import Operations
from promogest.lib.alembic import op
from promogest.dao.DaoUtils import get_columns

try:
    t_azienda = Table('azienda', params['metadata'], autoload=True,
                                    schema=params['mainSchema'])
except:
    from data.azienda import t_azienda


c_t_azienda = get_columns(t_azienda)

if "telefono" not in c_t_azienda:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.add_column('azienda', Column('telefono', String(12), nullable=True), schema=params["mainSchema"])

if "progressivo_fatturapa" not in c_t_azienda:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.add_column('azienda', Column('progressivo_fatturapa', String(5), nullable=True), schema=params["mainSchema"])
    delete_pickle()
    restart_program()

class Azienda(Dao):

    def __init__(self,campo=[], req=None):
        Dao.__init__(self,campo=campo, entity=self)

    def filter_values(self, k, v):
        if k == "schemaa":
            dic = { 'schemaa': t_azienda.c.schemaa==v}
        elif k == "denominazione":
            dic = { k: t_azienda.c.denominazione.ilike("%"+v+"%")}
        return dic[k]

std_mapper = mapper(Azienda, t_azienda,
                properties={ },
                order_by=t_azienda.c.schemaa)
