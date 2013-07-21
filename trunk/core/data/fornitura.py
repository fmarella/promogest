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

class FornituraDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.debug = debug

    def create(self):
        multiploTable = Table('multiplo', self.metadata, autoload=True, schema=self.schema)
        articleTable = Table('articolo', self.metadata, autoload=True, schema=self.schema)
        fornitoreTable = Table('fornitore', self.metadata, autoload=True, schema=self.schema)

        if self.schema:
            articoloFK =self.schema+'.articolo.id'
            multiploFK =self.schema+'.multiplo.id'
            fornitoreFK =self.schema+'.fornitore.id'
        else:
            articoloFK ='articolo.id'
            multiploFK ='multiplo.id'
            fornitoreFK ='fornitore.id'

        fornituraTable = Table('fornitura', self.metadata,
                Column('id',Integer,primary_key=True),
                Column('codice_articolo_fornitore',String(100),nullable=True),
                Column('prezzo_lordo',Numeric(16,4),nullable=False),
                Column('prezzo_netto',Numeric(16,4),nullable=False),
                Column('applicazione_sconti',String(20),nullable=True),
                Column('scorta_minima',Integer,nullable=True),
                Column('tempo_arrivo_merce',Integer,nullable=True),
                Column('fornitore_preferenziale',Boolean,nullable=True, default=False),
                Column('percentuale_iva',Numeric(8,4),nullable=True),
                Column('data_fornitura',DateTime,nullable=True),
                Column('data_prezzo',DateTime,nullable=True),
                #chiavi esterne
                Column('id_fornitore',Integer,ForeignKey(fornitoreFK, onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_articolo',Integer,ForeignKey(articoloFK, onupdate="CASCADE", ondelete="CASCADE")),
                Column('id_multiplo',Integer,ForeignKey(multiploFK, onupdate="CASCADE", ondelete="RESTRICT")),
                UniqueConstraint('id_fornitore', 'id_articolo', 'data_prezzo'),
                CheckConstraint( "applicazione_sconti = 'scalare' or applicazione_sconti = 'non scalare'" ),
                schema=self.schema
                )
        fornituraTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
