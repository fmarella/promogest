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

class Azienda(Base, Dao):
    try:
        __table__ =Table('azienda', params['metadata'], autoload=True,
                                    schema=params['mainSchema'])
    except:
        from data.azienda import t_azienda
        __table__ = t_azienda


    def __init__(self,campo=[], req=None):
        Dao.__init__(self,campo=campo, entity=self)

    def filter_values(self, k, v):
        if k == "schemaa":
            dic = { 'schemaa': Azienda.__table__.c.schemaa==v}
        elif k == "denominazione":
            dic = { k: Azienda.__tables__.c.denominazione.ilike("%"+v+"%")}
        return dic[k]

#PARTI DI MODIFICA ALLO SCHEMA AZIENDA
try:
    Azienda.__table__.c.telefono
except:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.add_column('azienda', Column('telefono', String(12), nullable=True), schema=params["mainSchema"])
    delete_pickle()
    print "HO AGGIUNTO LA COLONNA telefono NELLA TABELLA AZIENDA E ORA RIAVVIO IL PROGRAMMA ( dao.Azienda )"
    restart_program()

try:
    Azienda.__table__.c.progressivo_fatturapa
except:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.add_column('azienda', Column('progressivo_fatturapa', String(5), nullable=True), schema=params["mainSchema"])
    delete_pickle()
    print "HO AGGIUNTO LA COLONNA prograssivo_fatturapa NELLA TABELLA Azienda E ORA RIAVVIO IL PROGRAMMA ( dao.Azienda )"
    restart_program()
