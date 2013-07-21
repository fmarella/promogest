# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

class RigaDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.debug = debug

    def create(self):
        a = Table('articolo',self.metadata, autoload=True, schema=self.schema)
        b = Table('magazzino',self.metadata, autoload=True, schema=self.schema)
        c = Table('multiplo',self.metadata, autoload=True, schema=self.schema)
        d = Table('listino',self.metadata, autoload=True, schema=self.schema)

        if self.schema:
            articoloFK = self.schema+'.articolo.id'
            magazzinoFK = self.schema+'.magazzino.id'
            multiploFK = self.schema+'.multiplo.id'
            listinoFK = self.schema+'.listino.id'
        else:
            articoloFK = 'articolo.id'
            magazzinoFK = 'magazzino.id'
            multiploFK = 'multiplo.id'
            listinoFK = 'listino.id'

        rigaTable = Table('riga', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('valore_unitario_netto', Numeric(16,4), nullable=True),
                Column('valore_unitario_lordo', Numeric(16,4), nullable=True),
                Column('quantita', Numeric(16,4), nullable=True),
                Column('moltiplicatore', Numeric(16,4), nullable=True),
                Column('applicazione_sconti', String(20), nullable=True),
                Column('percentuale_iva', Numeric(8,4), nullable=False, default=0),
                Column('descrizione', String(500), nullable=True),
                #chiavi esterne
                Column('id_articolo',Integer,ForeignKey(articoloFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
                Column('id_magazzino',Integer,ForeignKey(magazzinoFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
                Column('id_multiplo',Integer,ForeignKey(multiploFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
                Column('id_listino',Integer,ForeignKey(listinoFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
                schema=self.schema
                )
        rigaTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
