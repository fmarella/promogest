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

class CompanyDb(object):

    def __init__(self, schema = None, mainSchema=None, tipo=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.mainSchema = mainSchema
        self.tipo = tipo
        self.debug = debug



    def create(self):
        if not self.mainSchema:
            self.schema = "AziendaPromo"
        companyTable = Table('azienda', self.metadata,
            Column('schemaa', String(100), primary_key=True),
            Column('denominazione', String(200), nullable=True, unique=True),
            Column('ragione_sociale', String(200), nullable=True),
            Column('sede_operativa_localita', String(200), nullable=True),
            Column('sede_operativa_indirizzo', String(200), nullable=True),
            Column('sede_operativa_numero', String(10), nullable=True),
            Column('sede_operativa_provincia', String(4), nullable=True),
            Column('sede_operativa_cap', String(5), nullable=True),
            Column('sede_legale_localita', String(200), nullable=True),
            Column('sede_legale_indirizzo', String(200), nullable=True),
            Column('sede_legale_numero', String(200), nullable=True),
            Column('sede_legale_provincia', String(200), nullable=True),
            Column('sede_legale_cap', String(200), nullable=True),
            Column('partita_iva', String(11), nullable=True),
            Column('codice_fiscale', String(16), nullable=True),
            Column('iscrizione_cciaa_data', DateTime, nullable=True),
            Column('iscrizione_cciaa_numero', String(50), nullable=True),
            Column('iscrizione_tribunale_data', DateTime, nullable=True),
            Column('iscrizione_tribunale_numero', String(50), nullable=True),
            Column('codice_rea', String(30), nullable=True),
            Column('matricola_inps', String(20), nullable=True),
            Column('numero_conto', String(30), nullable=True),
            Column('iban', String(27), nullable=True),
            Column('cin', String(20), nullable=True),
            Column('abi', String(20), nullable=True),
            Column('cab', String(20), nullable=True),
            Column('percorso_immagine', String(300), nullable=True),
            Column('tipo_schemaa', String(10), nullable=True),
            schema=self.mainSchema
                )
        companyTable.create(checkfirst=True)
        try:
            company = companyTable.insert()
            company.execute(schemaa = self.schema, tipo_schemaa=self.tipo)
        except:
            print"azienda presente nello schema"

    def data(self):
        #companyTable = Table('azienda',self.metadata, autoload=True)
        #company = companyTable.insert()
        #company.execute(schema ='test', denominazione='test', ragione_sociale='test')
        pass
