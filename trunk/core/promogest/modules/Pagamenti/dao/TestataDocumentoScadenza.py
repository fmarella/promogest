# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012
#by Promotux di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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
from migrate import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

class TestataDocumentoScadenza(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k =="idTestataDocumento":
            dic= {k: tesdocsca.c.id_testata_documento ==v}
        elif k == "numeroScadenza":
            dic= {k: tesdocsca.c.numero_scadenza==v}
        return  dic[k]

tesdocsca=Table('testata_documento_scadenza',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

if "id_banca" not in [c.name for c in tesdocsca.columns]:
    col = Column('id_banca', Integer, nullable=True)
    # ForeignKey(bancaFK, onupdate="CASCADE", ondelete="RESTRICT"),
    col.create(tesdocsca)

if "note_per_primanota" not in [c.name for c in tesdocsca.columns]:
    col = Column('note_per_primanota', String(400), nullable=True)
    col.create(tesdocsca)
else:
    if tipodb == "postgresql":
        col = tesdocsca.c.note_per_primanota
        col.alter(nullable=True)

std_mapper = mapper(TestataDocumentoScadenza, tesdocsca, properties={},
                                order_by=tesdocsca.c.id)
