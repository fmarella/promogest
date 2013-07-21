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

class TestataDocumentoDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.schema = schema
        self.mainSchema= mainSchema
        self.debug = debug

    def create(self):
        opTable = Table('operazione', self.metadata, autoload=True, schema=self.mainSchema)
        cliTable = Table('cliente', self.metadata, autoload=True, schema=self.schema)
        forTable = Table('fornitore', self.metadata, autoload=True, schema=self.schema)
        pagamentoTable = Table('pagamento', self.metadata, autoload=True, schema=self.schema)
        demTable = Table('destinazione_merce', self.metadata, autoload=True, schema=self.schema)
        banTable = Table('banca', self.metadata, autoload=True, schema=self.schema)
        aiTable = Table('aliquota_iva', self.metadata, autoload=True, schema=self.schema)
        veTable = Table('vettore', self.metadata, autoload=True, schema=self.schema)
        agTable = Table('agente', self.metadata, autoload=True, schema=self.schema)

        if self.schema:
            clienteFK = self.schema+'.cliente.id'
            fornitoreFK = self.schema+'.fornitore.id'
            pagamentoFK = self.schema+'.pagamento.id'
            destinazione_merceFK = self.schema+'.destinazione_merce.id'
            bancaFK = self.schema+'.banca.id'
            aliquota_ivaFK = self.schema+'.aliquota_iva.id'
            vettoreFK = self.schema+'.vettore.id'
            agenteFK = self.schema+'.agente.id'
            testata_documentoFK= self.schema+'.testata_documento.id'
        else:
            clienteFK = 'cliente.id'
            fornitoreFK = 'fornitore.id'
            pagamentoFK = 'pagamento.id'
            destinazione_merceFK = 'destinazione_merce.id'
            bancaFK = 'banca.id'
            aliquota_ivaFK = 'aliquota_iva.id'
            vettoreFK = 'vettore.id'
            agenteFK ='agente.id'
            testata_documentoFK = 'testata_documento.id'
        if self.mainSchema:
            operazioneFK =self.mainSchema+'.operazione.denominazione'
        else:
            operazioneFK = 'operazione.denominazione'



        testataDocumentoTable = Table('testata_documento', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('numero', Integer, nullable=False),
            Column('parte', Integer, nullable=True, default=1),
            Column('operazione', String(100),ForeignKey(operazioneFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=False),
            Column('registro_numerazione', String(50), nullable=False),
            Column('note_interne', Text, nullable=True),
            Column('note_pie_pagina', String(800), nullable=True),
            Column('data_documento',DateTime,PassiveDefault(func.now()), nullable=True),
            Column('data_inserimento',DateTime,PassiveDefault(func.now()), nullable=True),
            Column('protocollo', String(100), nullable=True),
            Column('causale_trasporto', String(100), nullable=True),
            Column('aspetto_esteriore_beni', String(100), nullable=True),
            Column('inizio_trasporto',DateTime, nullable=True),
            Column('fine_trasporto',DateTime, nullable=True),
            Column('incaricato_trasporto', String(100), nullable=True),
            Column('totale_colli', Integer, nullable=True),
            Column('totale_peso', String(200), nullable=True),
            Column('applicazione_sconti', String(20), nullable=True),
            Column('porto', String(10), nullable=True),
            Column('documento_saldato', Boolean, default=False),
            Column('totale_pagato', Numeric(16,4), nullable=True),
            Column('totale_sospeso', Numeric(16,4), nullable=True),
            Column('costo_da_ripartire', Numeric(16,4), nullable=True),
            Column('ripartire_importo', Boolean, default=False),
            #chiavi esterne
            Column('id_cliente', Integer,ForeignKey(clienteFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            Column('id_fornitore', Integer,ForeignKey(fornitoreFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            Column('id_destinazione_merce', Integer,ForeignKey(destinazione_merceFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            Column('id_pagamento', Integer,ForeignKey(pagamentoFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            Column('id_banca', Integer,ForeignKey(bancaFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            Column('id_aliquota_iva_esenzione', Integer,ForeignKey(aliquota_ivaFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            Column('id_vettore', Integer,ForeignKey(vettoreFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            Column('id_agente', Integer,ForeignKey(agenteFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            Column('id_primo_riferimento', Integer,ForeignKey(testata_documentoFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            Column('id_secondo_riferimento', Integer,ForeignKey(testata_documentoFK,onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
            CheckConstraint("parte < 4  AND parte >= 1"),
            CheckConstraint("id_cliente IS NULL AND id_fornitore IS NOT NULL  OR id_cliente IS NOT NULL AND id_fornitore IS NULL"),
            CheckConstraint("incaricato_trasporto = 'destinatario'  AND id_vettore IS NULL  OR incaricato_trasporto = 'mittente'  AND  id_vettore IS NULL  OR incaricato_trasporto = 'vettore'  AND  id_vettore IS NOT NULL"),
            CheckConstraint("applicazione_sconti = 'scalare'  OR applicazione_sconti = 'non scalare'"),
            UniqueConstraint('parte', 'numero', 'data_documento','id_primo_riferimento', 'id_secondo_riferimento'),
            schema=self.schema
                )
        testataDocumentoTable.create(checkfirst=True)

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass
