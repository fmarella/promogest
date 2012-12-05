# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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
from promogest.dao.Dao import Dao

try:
    t_cliente_variazione_listino = Table('cliente_variazione_listino',
                             params['metadata'],
                             schema=params['schema'],
                             autoload=True)
except:
    t_cliente_variazione_listino = Table('cliente_variazione_listino', params["metadata"],
        Column('id_cliente', Integer,
            ForeignKey(fk_prefix + 'cliente.id', onupdate="CASCADE", ondelete="CASCADE"),
             primary_key=True),
        Column('id_variazione', Integer,
            ForeignKey(fk_prefix + 'variazione_listino.id', onupdate="CASCADE", ondelete="RESTRICT"),
             primary_key=True),
        schema=params["schema"],
        useexisting=True)
    t_cliente_variazione_listino.create(checkfirst=True)

class ClienteVariazioneListino(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'idCliente':
            dic = {k: t_cliente_variazione_listino.c.id_cliente==v}
        elif k == 'idVariazione':
            dic = {k: t_cliente_variazione_listino.c.id_variazione==v}
        elif k == 'idVariazioneList':
            dic = {k: t_cliente_variazione_listino.c.id_variazione.in_(v)}
        return dic[k]
