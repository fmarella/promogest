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

class InformazioniContabiliDocumentoDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.debug = debug

    def create(self):
        azTable = Table('testata_documento', self.metadata, autoload=True, schema=self.schema)
        if self.schema:
            testata_documentoFK =self.schema+'.testata_documento.id'
        else:
            testata_documentoFK = 'testata_documento.id'

        informazioniContabiliDocumentoTable = Table('informazioni_contabili_documento', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('documento_saldato', Boolean, default=False),
                Column('id_documento',Integer,ForeignKey(testata_documentoFK,onupdate="CASCADE",ondelete="RESTRICT"),nullable=False, ),
                Column('id_primo_riferimento',Integer,ForeignKey(testata_documentoFK,onupdate="CASCADE",ondelete="RESTRICT")),
                Column('id_secondo_riferimento',Integer,ForeignKey(testata_documentoFK,onupdate="CASCADE",ondelete="RESTRICT")),
                Column('totale_pagato', Numeric(16,4), nullable=False, default=0),
                Column('totale_sospeso', Numeric(16,4), nullable=False, default=0),
                schema=self.schema
                )
        informazioniContabiliDocumentoTable.create(checkfirst=True)

    def alter(self, req=None, arg=None):
        pass
