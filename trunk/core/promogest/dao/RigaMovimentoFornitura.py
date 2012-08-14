# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
from promogest.dao.Fornitura import Fornitura
from promogest.dao.RigaMovimento import RigaMovimento, t_riga_movimento
from Dao import Dao

try:
    rigamovimentofornitura = Table('riga_movimento_fornitura',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    rigamovimentofornitura = Table('riga_movimento_fornitura', params['metadata'],
            Column('id', Integer, primary_key=True),
            Column('id_articolo', Integer,
                ForeignKey(fk_prefix + 'articolo.id'),
                nullable=False),
            Column('id_riga_movimento_acquisto', Integer,
                ForeignKey(fk_prefix + 'riga_movimento.id'),
                nullable=True),
            Column('id_riga_movimento_vendita', Integer,
                ForeignKey(fk_prefix + 'riga_movimento.id'),
                nullable=True),
            Column('id_fornitura', Integer,
                ForeignKey(fk_prefix + 'fornitura.id'),
                nullable=False),
            schema=params["schema"])
    rigamovimentofornitura.create(checkfirst=True)

class RigaMovimentoFornitura(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "idRigaMovimentoAcquisto":
            dic= {k:rigamovimentofornitura.c.id_riga_movimento_acquisto ==v}
        elif k == 'idFornitura':
            dic = {k:rigamovimentofornitura.c.id_fornitura==v}
        elif k == "idRigaMovimentoVendita":
            dic= {k:rigamovimentofornitura.c.id_riga_movimento_vendita ==v}
        elif k == "idRigaMovimentoVenditaBool":
            dic= {k:rigamovimentofornitura.c.id_riga_movimento_vendita != None}
        elif k == "idRigaMovimentoVenditaBoolFalse":
            dic= {k:rigamovimentofornitura.c.id_riga_movimento_vendita == None}
        elif k == "idArticolo":
            dic= {k:rigamovimentofornitura.c.id_articolo ==v}
        return  dic[k]


std_mapper = mapper(RigaMovimentoFornitura, rigamovimentofornitura,
    properties={
        "forni": relation(Fornitura,
            primaryjoin = (rigamovimentofornitura.c.id_fornitura==Fornitura.id)),
        "rigamovacq": relation(RigaMovimento,
            primaryjoin = (rigamovimentofornitura.c.id_riga_movimento_acquisto==t_riga_movimento.c.id), backref="rmfac"),
        "rigamovven": relation(RigaMovimento,
            primaryjoin = (rigamovimentofornitura.c.id_riga_movimento_vendita==t_riga_movimento.c.id), backref="rmfve"),
    },
    order_by=rigamovimentofornitura.c.id)
