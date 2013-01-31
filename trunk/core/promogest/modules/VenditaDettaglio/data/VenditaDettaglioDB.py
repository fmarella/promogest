# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013  by Promotux
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
from promogest.lib.utils import setconf
from promogest.dao.Magazzino import Magazzino
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.CCardType import c_card_type
from promogest.modules.VenditaDettaglio.dao.Pos import pos

if fk_prefix +'testata_scontrino' not in params['metadata'].tables:
    testataScontrinoTable = Table('testata_scontrino', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('data_inserimento',DateTime,DefaultClause(func.now()),nullable=False),
                Column('totale_scontrino',Numeric(16,4),nullable=False),
                Column('totale_contanti',Numeric(16,4),nullable=False),
                Column('totale_assegni',Numeric(16,4),nullable=False),
                Column('totale_carta_credito',Numeric(16,4),nullable=False),
                Column('id_magazzino',Integer,ForeignKey(fk_prefix + "magazzino.id", onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_pos',Integer,ForeignKey(fk_prefix +"pos.id", onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_ccardtype',Integer,ForeignKey(fk_prefix +"credit_card_type.id", onupdate="CASCADE", ondelete="RESTRICT")),
                Column('id_user',Integer),
                Column('id_testata_movimento',Integer,ForeignKey(fk_prefix + "testata_movimento.id", onupdate="CASCADE", ondelete="RESTRICT")),
                schema=params['schema'],
                useexisting =True
                )
    testataScontrinoTable.create(checkfirst=True)

if fk_prefix +'riga_scontrino' not in params['metadata'].tables:
    rigaScontrinoTable = Table('riga_scontrino', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('prezzo',Numeric(16,4),nullable=True),
            Column('prezzo_scontato',Numeric(16,4),nullable=True),
            Column('quantita',Numeric(16,4),nullable=False),
            Column('descrizione',String(200),nullable=False),
            Column('id_testata_scontrino',Integer,ForeignKey(fk_prefix +"testata_scontrino.id", onupdate="CASCADE", ondelete="CASCADE"),nullable=True),
            Column('id_articolo',Integer, ForeignKey(fk_prefix +"articolo.id", onupdate="CASCADE", ondelete="RESTRICT"),nullable=False),
            schema=params['schema'],
            useexisting =True
            )
    rigaScontrinoTable.create(checkfirst=True)

if fk_prefix +'sconto_scontrino' not in params['metadata'].tables :
    scontoScontrinoTable= Table('sconto_scontrino', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('valore',Numeric(16,4),nullable=True),
                Column('tipo_sconto',String(50),nullable=False),
                CheckConstraint( "tipo_sconto = 'valore' or tipo_sconto = 'percentuale'" ),
                schema = params['schema'],
                useexisting =True
            )
    scontoScontrinoTable.create(checkfirst=True)

if fk_prefix +'sconto_riga_scontrino' not in params['metadata'].tables:
    scontoRigaScontrinoTable = Table('sconto_riga_scontrino', params['metadata'],
            Column('id',Integer,ForeignKey(fk_prefix +"sconto_scontrino.id",onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_riga_scontrino',Integer,ForeignKey(fk_prefix +"riga_scontrino.id",onupdate="CASCADE",ondelete="CASCADE")),
            schema=params['schema'],
            useexisting =True)
    scontoRigaScontrinoTable.create(checkfirst=True)

if fk_prefix +'sconto_testata_scontrino' not in params['metadata'].tables:
    scontoTestataScontrinoTable = Table('sconto_testata_scontrino', params['metadata'],
            Column('id',Integer,ForeignKey(fk_prefix+"sconto_scontrino.id",onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_testata_scontrino',Integer,ForeignKey(fk_prefix+"testata_scontrino.id",onupdate="CASCADE",ondelete="CASCADE")),
            schema=params['schema'],
           useexisting =True
            )
    scontoTestataScontrinoTable.create(checkfirst=True)

if fk_prefix +'testata_scontrino_cliente' not in params['metadata'].tables:
    testataScontrinoClienteTable = Table('testata_scontrino_cliente', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('id_testata_scontrino',Integer,ForeignKey(fk_prefix +"testata_scontrino.id",onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_cliente',Integer,ForeignKey(fk_prefix+"cliente.id",onupdate="CASCADE",ondelete="CASCADE")),
            schema=params['schema'],
            useexisting =True
            )
    testataScontrinoClienteTable.create(checkfirst=True)
