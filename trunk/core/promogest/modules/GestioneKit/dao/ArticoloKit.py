# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from promogest.dao.Dao import Dao
from migrate import *


try:
    articolokit = Table('articolo_kit',
        params['metadata'],
        schema=params['schema'],
        autoload=True)

except:
    articoloTable = Table('articolo',
        params['metadata'],
        autoload=True,
        schema=params['schema'])

    if params["tipo_db"] == "sqlite":
        articoloFK = 'articolo.id'
    else:
        articoloFK = params['schema'] + '.articolo.id'


    articolokit = Table('articolo_kit', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('id_articolo_wrapper', Integer,
                ForeignKey(articoloFK, onupdate="CASCADE", ondelete="CASCADE")),
            Column('id_articolo_filler', Integer,
                ForeignKey(articoloFK, onupdate="CASCADE", ondelete="CASCADE"),
                nullable=True),
            Column('quantita', Numeric(16, 4), nullable=False),
            Column('data_inserimento', DateTime, nullable=False),
            Column('data_esclusione', DateTime, nullable=True),
            Column('attivo', Boolean, default=True), #potrebbe non servire ma lasciamolo
            Column('note', Text, nullable=True),
            schema=params["schema"],
            useexisting=True)
    articolokit.create(checkfirst=True)


class ArticoloKit(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "id":
            dic = {k: articolokit.c.id == v}
        elif k == 'idArticoloWrapper':
            dic = {k: articolokit.c.id_articolo_wrapper == v}
        elif k == 'idArticoloFiller':
            dic = {k: articolokit.c.id_articolo_filler == v}
        elif k == 'dataInserimento':
            dic = {k: rigaprimanota.c.data_inserimento >= v}
        elif k == 'dataEsclusione':
            dic = {k: rigaprimanota.c.data_esclusione <= v}
        return dic[k]

    #def _banca(self):
        #bn = Banca().getRecord(id=self.id_banca)
        #if bn:
            #return bn.denominazione
        #else:
            #return ""
    #banca= property(_banca)

std_mapper = mapper(ArticoloKit,
                    articolokit,
                    properties={},
                    order_by=articolokit.c.id)
