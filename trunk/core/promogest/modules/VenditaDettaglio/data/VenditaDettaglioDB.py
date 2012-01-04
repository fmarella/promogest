# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012  by Promotux
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
from promogest.ui.utils import setconf
#from promogest.dao.Dao import Dao


posTable = Table('pos', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('denominazione', String(200), nullable=False ),
        Column('denominazione_breve', String(10), nullable=False),
        schema=params['schema'], useexisting =True
        )
posTable.create(checkfirst=True)

magazzinoTable = Table('magazzino', params['metadata'], autoload=True, schema=params['schema'])
testataMovimentoTable = Table('testata_movimento', params['metadata'], autoload=True, schema=params['schema'])
ccdTypeTable = Table('credit_card_type', params['metadata'], autoload=True, schema=params['schema'])

if tipodb=="sqlite":
    magazzinoFK = 'magazzino.id'
    posFK = "pos.id"
    cctFK = 'credit_card_type.id'
    testataMovimentoFK = 'testata_movimento.id'
    testataScontrinoFK = 'testata_scontrino.id'
    articoloFK = 'articolo.id'
    scontoscontrinoFK = 'sconto_scontrino.id'
    rigascontrinoFK = 'riga_scontrino.id'
else:
    magazzinoFK = params['schema']+'.magazzino.id'
    posFK = params['schema']+'.pos.id'
    cctFK = params['schema']+'.credit_card_type.id'
    testataMovimentoFK = params['schema']+'.testata_movimento.id'
    testataScontrinoFK = params['schema'] +'.testata_scontrino.id'
    articoloFK = params['schema'] +'.articolo.id'
    scontoscontrinoFK = params['schema'] +'.sconto_scontrino.id'
    rigascontrinoFK = params['schema']+'.riga_scontrino.id'


testataScontrinoTable = Table('testata_scontrino', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('data_inserimento',DateTime,DefaultClause(func.now()),nullable=False),
            Column('totale_scontrino',Numeric(16,4),nullable=False),
            Column('totale_contanti',Numeric(16,4),nullable=False),
            Column('totale_assegni',Numeric(16,4),nullable=False),
            Column('totale_carta_credito',Numeric(16,4),nullable=False),
            #chiavi esterne
            Column('id_magazzino',Integer,ForeignKey(magazzinoFK, onupdate="CASCADE", ondelete="RESTRICT")),
            Column('id_pos',Integer,ForeignKey(posFK, onupdate="CASCADE", ondelete="RESTRICT")),
            Column('id_ccardtype',Integer,ForeignKey(cctFK, onupdate="CASCADE", ondelete="RESTRICT")),
            Column('id_user',Integer),
            Column('id_testata_movimento',Integer,ForeignKey(testataMovimentoFK, onupdate="CASCADE", ondelete="RESTRICT")),
            schema=params['schema'],
#                useexisting =True
            )
testataScontrinoTable.create(checkfirst=True)

articoloTable = Table('articolo', params['metadata'], autoload=True, schema=params['schema'])

rigaScontrinoTable = Table('riga_scontrino', params['metadata'],
        Column('id',Integer,primary_key=True),
        Column('prezzo',Numeric(16,4),nullable=True),
        Column('prezzo_scontato',Numeric(16,4),nullable=True),
        Column('quantita',Numeric(16,4),nullable=False),
        Column('descrizione',String(200),nullable=False),
        #chiavi esterne
        Column('id_testata_scontrino',Integer,ForeignKey(testataScontrinoFK, onupdate="CASCADE", ondelete="CASCADE"),nullable=True),
        Column('id_articolo',Integer, ForeignKey(articoloFK, onupdate="CASCADE", ondelete="RESTRICT"),nullable=False),
        schema=params['schema']
        )
rigaScontrinoTable.create(checkfirst=True)

scontoScontrinoTable= Table('sconto_scontrino', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('valore',Numeric(16,4),nullable=True),
            Column('tipo_sconto',String(50),nullable=False),
            CheckConstraint( "tipo_sconto = 'valore' or tipo_sconto = 'percentuale'" ),
            schema = params['schema']
        )
scontoScontrinoTable.create(checkfirst=True)

#rigaDotoTable = Table('sconto_scontrino', params['metadata'], autoload=True, schema=params['schema'])

scontoRigaScontrinoTable = Table('sconto_riga_scontrino', params['metadata'],
        Column('id',Integer,ForeignKey(scontoscontrinoFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
        Column('id_riga_scontrino',Integer,ForeignKey(rigascontrinoFK,onupdate="CASCADE",ondelete="CASCADE")),
        schema=params['schema'])
scontoRigaScontrinoTable.create(checkfirst=True)

chiusuraFiscaleTable = Table('chiusura_fiscale', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('data_chiusura',DateTime,nullable=False),
            Column('id_magazzino',Integer,ForeignKey(magazzinoFK, onupdate="CASCADE", ondelete="RESTRICT")),
            Column('id_pos',Integer,ForeignKey(posFK, onupdate="CASCADE", ondelete="RESTRICT")),
            schema=params['schema']
            )
chiusuraFiscaleTable.create(checkfirst=True)

#    testatascontrinoTable = Table('testata_scontrino', params['metadata'], autoload=True, schema=params['schema'])
testataDoctoTable = Table('sconto_scontrino', params['metadata'], autoload=True, schema=params['schema'])
scontoTestataScontrinoTable = Table('sconto_testata_scontrino', params['metadata'],
        Column('id',Integer,ForeignKey(scontoscontrinoFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
        Column('id_testata_scontrino',Integer,ForeignKey(testataScontrinoFK,onupdate="CASCADE",ondelete="CASCADE")),
        schema=params['schema']
        )
scontoTestataScontrinoTable.create(checkfirst=True)

clienteTable = Table('cliente', params['metadata'], autoload=True, schema=params['schema'])
if tipodb=="sqlite":
    testataScontrinoFK = 'testata_scontrino.id'
    clienteFK = 'cliente.id'
else:
    testataScontrinoFK = params['schema'] +'.testata_scontrino.id'
    clienteFK = params['schema'] +'.cliente.id'
testataScontrinoClienteTable = Table('testata_scontrino_cliente', params['metadata'],
        Column('id',Integer,primary_key=True),
        Column('id_testata_scontrino',Integer,ForeignKey(testataScontrinoFK,onupdate="CASCADE",ondelete="CASCADE")),
        Column('id_cliente',Integer,ForeignKey(clienteFK,onupdate="CASCADE",ondelete="CASCADE")),
        schema=params['schema']
        )
testataScontrinoClienteTable.create(checkfirst=True)
