# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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

try:
    t_riga_prima_nota = Table('riga_prima_nota',
                            params['metadata'],
                            schema=params['schema'],
                            autoload=True)
except:
    from data.rigaPrimaNota import t_riga_prima_nota


from promogest.dao.Dao import Dao
from promogest.dao.Banca import Banca
from promogest.lib.migrate import *




#if "id_banca" not in [c.name for c in t_riga_prima_nota.columns]:
    #col = Column('id_banca', Integer,
##            ForeignKey(bancaFK, onupdate="CASCADE", ondelete="RESTRICT"),
        #nullable=True)
    #col.create(t_riga_prima_nota)

#if "note_primanota" not in [c.name for c in t_riga_prima_nota.columns]:
    #col = Column('note_primanota', Text, nullable=True)
    #col.create(t_riga_prima_nota)

class RigaPrimaNota(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "id":
            dic = {k: t_riga_prima_nota.c.id == v}
        elif k == 'idTestataDocumento':
            dic = {k: t_riga_prima_nota.c.id_testata_documento == v}
        elif k == 'segno':
            dic = {k: t_riga_prima_nota.c.segno == v}
        elif k == 'tipo':
            dic = {k: t_riga_prima_nota.c.tipo == v}
        elif k == 'idTestataPrimaNota':
            dic = {k: t_riga_prima_nota.c.id_testata_prima_nota == v}
        return dic[k]

    @property
    def banca(self):
        bn = Banca().getRecord(id=self.id_banca)
        if bn:
            return bn.denominazione
        else:
            return ''

std_mapper = mapper(RigaPrimaNota,
                    t_riga_prima_nota,
                    properties={},
                    order_by=t_riga_prima_nota.c.id)
