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

t_articolo= Table('articolo', params["metadata"],
    Column('id', Integer, primary_key=True),
    Column('codice', String(50), nullable=False, unique=True),
    Column('denominazione', String(600), nullable=False),
    Column('id_aliquota_iva', Integer, ForeignKey(fk_prefix+"aliquota_iva.id" ,onupdate="CASCADE",ondelete="RESTRICT")),
    Column('id_famiglia_articolo', Integer, ForeignKey(fk_prefix+'famiglia_articolo.id',onupdate="CASCADE",ondelete="RESTRICT")),
    Column('id_categoria_articolo', Integer, ForeignKey(fk_prefix+'categoria_articolo.id',onupdate="CASCADE",ondelete="RESTRICT")),
    Column('id_immagine', Integer,ForeignKey(fk_prefix+'image.id',onupdate="CASCADE",ondelete="RESTRICT")),
    Column('id_unita_base', Integer, ForeignKey(fk_prefix_main+"unita_base.id",onupdate="CASCADE",ondelete="RESTRICT")),
    Column('id_stato_articolo', Integer, ForeignKey(fk_prefix_main+'stato_articolo.id',onupdate="CASCADE",ondelete="RESTRICT")),
    Column('produttore', String(150), nullable=True),
    Column('unita_dimensioni', String(20), nullable=True),
    Column('lunghezza', Float, nullable=True),
    Column('larghezza', Float, nullable=True),
    Column('altezza', Float, nullable=True),
    Column('unita_volume', String(20), nullable=True),
    Column('volume', String(20), nullable=True),
    Column('unita_peso', String(20), nullable=True),
    Column('peso_lordo', Float, nullable=True),
    Column('id_imballaggio', Integer, ForeignKey(fk_prefix+'imballaggio.id',onupdate="CASCADE",ondelete="RESTRICT")),
    Column('peso_imballaggio', Float, nullable=True),
    Column('stampa_etichetta', Boolean, default=0),
    Column('codice_etichetta', String(50), nullable=True),
    Column('descrizione_etichetta', String(200), nullable=True),
    Column('stampa_listino', Boolean, default=0),
    Column('descrizione_listino', String(1000), nullable=True),
    Column('aggiornamento_listino_auto', Boolean, default=0),
    Column('timestamp_variazione', DateTime, nullable=True),
    Column('note', Text, nullable=True),
    Column('contenuto', Text, nullable=True),
    Column('cancellato', Boolean, nullable=True, default=False),
    Column('sospeso', Boolean, nullable=True, default=False),
    Column('quantita_minima',Float),
    schema=params["schema"],
    extend_existing=True
        )
t_articolo.create(checkfirst=True)
