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

import datetime
from sqlalchemy import *
from promogest.Environment import *

t_testata_documento = Table('testata_documento', params["metadata"],
    Column('id', Integer, primary_key=True),
    Column('numero', Integer, nullable=False),
    Column('parte', Integer, nullable=True, default=1),
    Column('operazione', String(100),ForeignKey(fk_prefix_main+'operazione.denominazione',onupdate="CASCADE",ondelete="RESTRICT"), nullable=False),
    Column('registro_numerazione', String(50), nullable=False),
    Column('note_interne', Text, nullable=True),
    Column('note_pie_pagina', String(800), nullable=True),
    Column('data_documento',DateTime, nullable=True),
    Column('data_inserimento',DateTime,ColumnDefault(datetime.datetime.now), nullable=True),
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
    Column('id_cliente', Integer,ForeignKey(fk_prefix+'cliente.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    Column('id_fornitore', Integer,ForeignKey(fk_prefix+'fornitore.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    Column('id_destinazione_merce', Integer,ForeignKey(fk_prefix+'destinazione_merce.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    Column('id_pagamento', Integer,ForeignKey(fk_prefix+'pagamento.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    Column('id_banca', Integer,ForeignKey(fk_prefix+'banca.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    Column('id_aliquota_iva_esenzione', Integer,ForeignKey(fk_prefix+'aliquota_iva.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    Column('id_vettore', Integer,ForeignKey(fk_prefix+'vettore.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    Column('id_agente', Integer,ForeignKey(fk_prefix+'agente.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    Column('id_primo_riferimento', Integer,ForeignKey(fk_prefix+'testata_documento.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    Column('id_secondo_riferimento', Integer,ForeignKey(fk_prefix+'testata_documento.id',onupdate="CASCADE",ondelete="RESTRICT"), nullable=True),
    CheckConstraint("parte < 5  AND parte >= 1"),
    CheckConstraint("id_cliente IS NULL AND id_fornitore IS NOT NULL  OR id_cliente IS NOT NULL AND id_fornitore IS NULL"),
    CheckConstraint("incaricato_trasporto = 'destinatario'  AND id_vettore IS NULL  OR incaricato_trasporto = 'mittente'  AND  id_vettore IS NULL  OR incaricato_trasporto = 'vettore'  AND  id_vettore IS NOT NULL"),
    CheckConstraint("applicazione_sconti = 'scalare'  OR applicazione_sconti = 'non scalare'"),
    UniqueConstraint('parte', 'numero', 'data_documento','id_primo_riferimento', 'id_secondo_riferimento'),
    schema=params["schema"]
        )
t_testata_documento.create(checkfirst=True)
