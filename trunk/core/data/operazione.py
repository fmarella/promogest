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

class OperazioneDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.mainSchema = mainSchema
        self.debug = debug

    def create(self):
        operazioneTable = Table('operazione', self.metadata,
                Column('denominazione', String(100), primary_key=True),
                Column('segno',String(3), nullable=True),
                Column('fonte_valore', String(50), nullable=True),
                Column('tipo_persona_giuridica', String(50), nullable=True),
                Column('tipo_operazione', String(50), nullable=True),
                schema=self.mainSchema
                )
        operazioneTable.create(checkfirst=True)
        s= select([operazioneTable.c.denominazione]).execute().fetchall()
        if (u'Fattura vendita',) not in s or s ==[]:
            tipo = operazioneTable.insert()
            tipo.execute(denominazione='Fattura vendita', segno='-', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )
            tipo.execute(denominazione='Fattura acquisto', segno='+', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore' )
            tipo.execute(denominazione='DDT vendita', segno='-', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )
            tipo.execute(denominazione='DDT acquisto', segno='+', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore' )
            tipo.execute(denominazione='DDT reso a fornitore', segno='-', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore' )
            tipo.execute(denominazione='DDT reso da cliente', segno='+', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )
            tipo.execute(denominazione='Nota di credito a cliente', segno='+', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )
            tipo.execute(denominazione='Nota di credito da fornitore', segno='-', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore')
            tipo.execute(denominazione='Scarico per uso interno', segno='-', fonte_valore='acquisto_senza_iva', tipo_operazione="movimento")
            tipo.execute(denominazione='Scarico per deterioramento o rottura', segno='-', fonte_valore='acquisto_senza_iva', tipo_operazione="movimento" )
            tipo.execute(denominazione='Scarico per omaggio', segno='-', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="movimento")
            tipo.execute(denominazione='Carico per inventario', segno='+', fonte_valore='acquisto_senza_iva', tipo_operazione="movimento" )
            tipo.execute(denominazione='Scarico venduto da cassa', segno='-', fonte_valore='vendita_iva', tipo_operazione="movimento" )
            tipo.execute(denominazione='Fattura accompagnatoria', segno='-', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="documento" )
            tipo.execute(denominazione='Preventivo', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="documento" )
            tipo.execute(denominazione='Ordine da cliente', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="documento" )
            tipo.execute(denominazione='Ordine a fornitore', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore', tipo_operazione="documento" )
            tipo.execute(denominazione='Vendita dettaglio', segno='-', fonte_valore='vendita_iva', tipo_persona_giuridica='cliente')
            tipo.execute(denominazione='Fattura differita vendita', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="documento" )
            tipo.execute(denominazione='Fattura differita acquisto', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore', tipo_operazione="documento" )



    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
