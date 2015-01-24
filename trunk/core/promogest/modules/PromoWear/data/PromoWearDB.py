# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from promogest.dao.Dao import Dao



if hasattr(conf, 'PromoWear'):
    if conf.PromoWear.primoavvio=="yes":
        """ tabelle schema principale """

        #TABELLA ANNO ABBIGLIAMENTO
        annoAbbigliamentoTable = Table('anno_abbigliamento', params['metadata'],
                            Column('id', Integer, primary_key=True),
                            Column('denominazione', String(50), nullable=False),
                            schema=params['mainSchema'])
        annoAbbigliamentoTable.create(checkfirst=True)


        #TABELLA GENERE ABBIGLIAMENTO
        genereAbbigliamentoTable = Table('genere_abbigliamento', params['metadata'],
                            Column('id', Integer, primary_key=True),
                            Column('denominazione', String(50), nullable=False),
                            schema=params['mainSchema'])
        genereAbbigliamentoTable.create(checkfirst=True)

        #TABELLA STAGIONE ABBIGLIAMENTO
        stagioneAbbigliamentoTable = Table('stagione_abbigliamento', params['metadata'],
                            Column('id', Integer, primary_key=True),
                            Column('denominazione', String(50), nullable=False),
                            schema=params['mainSchema'])
        stagioneAbbigliamentoTable.create(checkfirst=True)

        # TABELLA COLORE
        coloreTable = Table('colore', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione', 'denominazione_breve'),
                schema=params["schema"])
        coloreTable.create(checkfirst=True)

        #tabella GRUPPO TAGLIA
        gruppoTagliaTable = Table('gruppo_taglia', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione', 'denominazione_breve'),
                schema=params["schema"])
        gruppoTagliaTable.create(checkfirst=True)


        #TABELLA taglia
        tagliaTable = Table('taglia', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione_breve'),
                schema=params["schema"])
        tagliaTable.create(checkfirst=True)

        #TABELLA gruppo taglia
        gruppoTagliaTagliaTable = Table('gruppo_taglia_taglia', params['metadata'],
                Column('id_gruppo_taglia',Integer,
                            ForeignKey(fk_prefix + "gruppo_taglia.id",
                                    onupdate="CASCADE",
                                    ondelete="RESTRICT"),
                            primary_key=True),
                Column('id_taglia',Integer,
                            ForeignKey(fk_prefix + "taglia.id",
                                    onupdate="CASCADE",
                                    ondelete="RESTRICT"),
                            primary_key=True),
                Column('ordine',Integer,nullable=False),
                schema=params["schema"])
        gruppoTagliaTagliaTable.create(checkfirst=True)

        # TABELLA modello
        modelloTable = Table('modello', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione', 'denominazione_breve'),
                schema=params["schema"])
        modelloTable.create(checkfirst=True)

        #TABELLA ARTICOLO TAGLIA COLORE
        articoloTagliaColoreTable = Table('articolo_taglia_colore', params['metadata'],
                    Column('id_articolo',Integer,ForeignKey(fk_prefix+"articolo.id",onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                    Column('id_articolo_padre',Integer,ForeignKey(fk_prefix+"articolo.id",onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_gruppo_taglia',Integer,ForeignKey(fk_prefix+'gruppo_taglia.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_taglia',Integer,ForeignKey(fk_prefix+"taglia.id",onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_colore',Integer,ForeignKey(fk_prefix+"colore.id",onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_anno',Integer,ForeignKey(fk_prefix_main+"anno_abbigliamento.id",onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_stagione',Integer,ForeignKey(fk_prefix+'stagione_abbigliamento.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_genere',Integer,ForeignKey(fk_prefix+'genere_abbigliamento.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_modello',Integer,ForeignKey(fk_prefix+'modello.id',onupdate="CASCADE",ondelete="CASCADE")),
                    UniqueConstraint('id_articolo_padre', 'id_gruppo_taglia', "id_taglia", "id_colore"),
                    ForeignKeyConstraint(['id_gruppo_taglia', 'id_taglia'],[fk_prefix+'gruppo_taglia_taglia.id_gruppo_taglia',fk_prefix+'gruppo_taglia_taglia.id_taglia']),
                    schema=params['schema'])
        articoloTagliaColoreTable.create(checkfirst=True)

        conf.PromoWear.primoavvio = "no"
        conf.PromoWear.mod_enable = "yes"
        conf.save()
