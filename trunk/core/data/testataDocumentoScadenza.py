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
from promogest.Environment import *


t_testata_documento_scadenza = Table('testata_documento_scadenza', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('id_testata_documento', Integer,ForeignKey(fk_prefix+'testata_documento.id',onupdate="CASCADE",ondelete="CASCADE"), nullable=False),
        Column('data',DateTime, nullable=False),
        Column('id_banca', Integer, nullable=True),
        Column('importo', Numeric(16,4),nullable=False),
        Column('pagamento',String(100),nullable=False),
        Column('note_per_primanota', String(400),nullable=True),
        Column('data_pagamento',DateTime,nullable=True),
        Column('numero_scadenza', Integer, nullable=False),
        schema=params["schema"]
        )
t_testata_documento_scadenza.create(checkfirst=True)
#self.metadata.remove(testataDocumentoScadenzaTable)
#tryToUpdate = Table('testata_documento_scadenza', self.metadata,schema=self.schema,autoload=True)
#if len(tryToUpdate.c) <7:
    #tryToUpdate.drop()
    #print "CANCELLO TABELLA TESTATA DOCUMENTO SCADENZA PERCHE' ERRATA"
    #testataDocumentoScadenzaTable.create(checkfirst=True)
    #print "RICREO TABELLA TESTATA DOCUMENTO SCADENZA CORRETTO"
