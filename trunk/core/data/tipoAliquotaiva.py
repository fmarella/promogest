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

class TipoAliquotaIvaDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.mainSchema=mainSchema
        self.debug = debug

    def create(self):
        tipoAliquotaIvaTable = Table('tipo_aliquota_iva', self.metadata,
                Column('id', Integer, primary_key=True),
                Column('denominazione',String(100),nullable=True, unique=True),
                schema=self.mainSchema
                )
        tipoAliquotaIvaTable.create(checkfirst=True)
        s= select([tipoAliquotaIvaTable.c.denominazione]).execute().fetchall()
        if (u'Ordinaria',) not in s or s==[]:
            tipo = tipoAliquotaIvaTable.insert()
            tipo.execute(denominazione='Ordinaria')
            tipo.execute(denominazione='Non imponibile')
            tipo.execute(denominazione='Esente')
            tipo.execute(denominazione='Fuori campo Iva')
            tipo.execute(denominazione='Escluso')

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
