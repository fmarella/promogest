# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>

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
from promogest.dao.Dao import Dao
from migrate import *
from promogest.modules.CSA.dao.GasRefrigerante import GasRefrigerante
from promogest.modules.CSA.dao.TipoApparecchio import TipoApparecchio

try:
    t_articolo_csa = Table('gestione_commesse_csa', params['metadata'],
                         schema=params['schema'], autoload=True)
except:

    t_articolo_csa = Table(
        'gestione_commesse_csa',
        params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('id_articolo', Integer,
               ForeignKey(fk_prefix + 'articolo.id',
                          onupdate='CASCADE', ondelete='CASCADE')),
        Column('numero_serie', String(200), nullable=True),
        Column('combustibile', String(200), nullable=True),
        Column('data_avviamento', DateTime, nullable=True),
        Column('tenuta_libretto', Boolean, default=False, nullable=False),
        Column('tenuta_libretto', Boolean),
        Column('id_luogo_installazione', Integer,
               ForeignKey(fk_prefix + 'luogo_installazione.id',
                          onupdate='CASCADE', ondelete='CASCADE')),
        Column('id_cliente_installatore', Integer,
               ForeignKey(fk_prefix + 'installatore.id',
                          onupdate='CASCADE', ondelete='CASCADE')),
        Column('id_cadenza', Integer,
               ForeignKey(fk_prefix + 'anagrafica_cadenze.id',
                          onupdate='CASCADE', ondelete='CASCADE')),
        schema=params['schema'],
        useexisting=True,
        )
    t_articolo_csa.create(checkfirst=True)


class ArticoloCSA(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'id':
            dic = {k: t_articolo_csa.c.id==v}
        elif k == 'id_articolo':
            dic = {k: t_articolo_csa.c.id_articolo==v}
        return dic[k]

    @property
    def tipo_apparecchio(self):
        a = TipoApparecchio().getRecord(id=self.id_tipo_apparecchio)
        if a:
            return a.denominazione
        else:
            return _('tipo apparecchio indeterminato')

    @property
    def gas_refrigerante(self):
        a = GasRefrigerante().getRecord(id=self.id_gas_refrigerante)
        if a:
            return a.denominazione
        else:
            return _('gas refrigerante indeterminato')


std_mapper = mapper(ArticoloCSA, t_articolo_csa,
                    order_by=t_articolo_csa.c.id_articolo)
