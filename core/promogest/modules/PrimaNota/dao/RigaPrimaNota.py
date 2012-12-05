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
from promogest.dao.Dao import Dao
from promogest.dao.Banca import Banca
from migrate import *


try:
    rigaprimanota = Table('riga_prima_nota',
        params['metadata'],
        schema=params['schema'],
        autoload=True)

    if "id_banca" not in [c.name for c in rigaprimanota.columns]:
        col = Column('id_banca', Integer,
#            ForeignKey(bancaFK, onupdate="CASCADE", ondelete="RESTRICT"),
            nullable=True)
        col.create(rigaprimanota)

    if "note_primanota" not in [c.name for c in rigaprimanota.columns]:
        col = Column('note_primanota', Text, nullable=True)
        col.create(rigaprimanota)

    #rigaprimanota.c.valore.alter(Numeric(16, 4), nullable=False)

except Exception as e:
    pg2log.info(str(e))
    userTableTable = Table('testata_documento',
        params['metadata'],
        autoload=True,
        schema=params['schema'])
    testata_prima_notaTable = Table('testata_prima_nota',
        params['metadata'],
        schema=params['schema'],
        autoload=True)

    if params["tipo_db"] == "sqlite":
        primanotaFK = 'testata_prima_nota.id'
        testatadocumentoFK = 'testata_documento.id'
        bancaFK = "banca.id"
    else:
        primanotaFK = params['schema'] + '.testata_prima_nota.id'
        testatadocumentoFK = params['schema'] + '.testata_documento.id'
        bancaFK = params["schema"] + ".banca.id"

    rigaprimanota = Table('riga_prima_nota', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('denominazione', String(400), nullable=False),
            Column('id_testata_prima_nota', Integer,
                ForeignKey(primanotaFK, onupdate="CASCADE", ondelete="CASCADE")),
            Column('id_testata_documento', Integer,
                ForeignKey(testatadocumentoFK, onupdate="CASCADE", ondelete="RESTRICT"),
                nullable=True),
            Column('id_banca', Integer,
                ForeignKey(bancaFK, onupdate="CASCADE", ondelete="RESTRICT"),
                nullable=True),
            Column('numero', Integer, nullable=False),
            Column('data_registrazione', DateTime, nullable=True),
            Column('tipo', String(25), nullable=False),
            Column('segno', String(25), nullable=False),
            Column('valore', Numeric(16, 4), nullable=False),
            Column('note_primanota', Text, nullable=True),
            schema=params["schema"],
            useexisting=True)
    rigaprimanota.create(checkfirst=True)


class RigaPrimaNota(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "id":
            dic = {k: rigaprimanota.c.id == v}
        elif k == 'idTestataDocumento':
            dic = {k: rigaprimanota.c.id_testata_documento == v}
        elif k == 'segno':
            dic = {k: rigaprimanota.c.segno == v}
        elif k == 'tipo':
            dic = {k: rigaprimanota.c.tipo == v}
        elif k == 'idTestataPrimaNota':
            dic = {k: rigaprimanota.c.id_testata_prima_nota == v}
        return dic[k]

    @property
    def banca(self):
        bn = Banca().getRecord(id=self.id_banca)
        if bn:
            return bn.denominazione
        else:
            return ''

std_mapper = mapper(RigaPrimaNota,
                    rigaprimanota,
                    properties={},
                    order_by=rigaprimanota.c.id)
