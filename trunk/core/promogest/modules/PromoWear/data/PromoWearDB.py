# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

        #creo tabella anno abbigliamento in schema principale e ci metto i dati di default
        annoAbbigliamentoTable = Table('anno_abbigliamento', params['metadata'],
                            Column('id', Integer, primary_key=True),
                            Column('denominazione', String(50), nullable=False),
                            schema=params['mainSchema'])
        annoAbbigliamentoTable.create(checkfirst=True)
        s= select([annoAbbigliamentoTable.c.denominazione]).execute().fetchall()
        if (u'2008', ) not in s or s==[]:
            tipo = annoAbbigliamentoTable.insert()
            tipo.execute(denominazione='2008')
            tipo.execute(denominazione='2009')
            tipo.execute(denominazione='2010')
            tipo.execute(denominazione='2011')
            tipo.execute(denominazione='2012')
            tipo.execute(denominazione='2013')

        #creo tabella genere_abbigliamento e ci metto i valori di default
        genereAbbigliamentoTable = Table('genere_abbigliamento', params['metadata'],
                            Column('id', Integer, primary_key=True),
                            Column('denominazione', String(50), nullable=False),
                            schema=params['mainSchema'])
        genereAbbigliamentoTable.create(checkfirst=True)
        s= select([genereAbbigliamentoTable.c.denominazione]).execute().fetchall()
        if (u'Unisex', ) not in s or s==[]:
            tipo = genereAbbigliamentoTable.insert()
            tipo.execute(denominazione='Unisex')
            tipo.execute(denominazione='Uomo')
            tipo.execute(denominazione='Donna')
            tipo.execute(denominazione='Bambino')

        stagioneAbbigliamentoTable = Table('stagione_abbigliamento', params['metadata'],
                            Column('id', Integer, primary_key=True),
                            Column('denominazione', String(50), nullable=False),
                            schema=params['mainSchema'])
        stagioneAbbigliamentoTable.create(checkfirst=True)
        s= select([stagioneAbbigliamentoTable.c.denominazione]).execute().fetchall()
        if (u'Primavera - Estate',) not in s or s==[]:
            tipo = stagioneAbbigliamentoTable.insert()
            tipo.execute(denominazione='Primavera - Estate')
            tipo.execute(denominazione='Autunno - Inverno')

        """ tabelle specifiche dello schema azienda """

        # TABELLA COLORE
        coloreTable = Table('colore', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione', 'denominazione_breve'),
                schema=params["schema"])
        coloreTable.create(checkfirst=True)
#        s= select([coloreTable.c.denominazione]).execute().fetchall()
#        if (u'n/a',) not in s or s==[]:
#            tipo = coloreTable.insert()
#            tipo.execute(denominazione='n/a', denominazione_breve='n/a')


        #tabella GRUPPO TAGLIA
        gruppoTagliaTable = Table('gruppo_taglia', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione', 'denominazione_breve'),
                schema=params["schema"])
        gruppoTagliaTable.create(checkfirst=True)
#        s= select([gruppoTagliaTable.c.denominazione]).execute().fetchall()
#        if (u'n/a',) not in s or s==[]:
#            tipo = gruppoTagliaTable.insert()
#            tipo.execute(denominazione='n/a', denominazione_breve='n/a')

        #tabella TAGLIA
        tagliaTable = Table('taglia', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione_breve'),
                schema=params["schema"])
        tagliaTable.create(checkfirst=True)
#        s= select([tagliaTable.c.denominazione]).execute().fetchall()
#        if (u'n/a',) not in s or s==[]:
#            tipo = tagliaTable.insert()
#            tipo.execute(denominazione='n/a', denominazione_breve='n/a')

        #taglia=Table('taglia', params['metadata'],schema = params['schema'],autoload=True)
        #gruppotaglia=Table('gruppo_taglia', params['metadata'],schema = params['schema'],autoload=True)

        if tipodb == "sqlite":
            gruppoTagliaFK = 'gruppo_taglia.id'
            tagliaFK = 'taglia.id'
        else:
            gruppoTagliaFK = params['schema']+'.gruppo_taglia.id'
            tagliaFK = params['schema']+'.taglia.id'


        gruppoTagliaTagliaTable = Table('gruppo_taglia_taglia', params['metadata'],
                Column('id_gruppo_taglia',Integer,ForeignKey(gruppoTagliaFK,onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
                Column('id_taglia',Integer,ForeignKey(tagliaFK,onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
                Column('ordine',Integer,nullable=False),
                schema=params["schema"])
        gruppoTagliaTagliaTable.create(checkfirst=True)
#        s= select([gruppoTagliaTagliaTable.c.ordine]).execute().fetchall()
#        if (1,) not in s or s==[]:
#            tipo = gruppoTagliaTagliaTable.insert()
#            tipo.execute(id_gruppo_taglia=1, id_taglia=1, ordine=1)

        # TABELLA modello
        modelloTable = Table('modello', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione', 'denominazione_breve'),
                schema=params["schema"])
        modelloTable.create(checkfirst=True)
#        s= select([modelloTable.c.denominazione]).execute().fetchall()
#        if (u'n/a',) not in s or s==[]:
#            tipo = modelloTable.insert()
#            tipo.execute(denominazione='n/a', denominazione_breve='n/a')


        if tipodb == "sqlite":
            articoloFK = 'articolo.id'
            gruppoTagliaFK = 'gruppo_taglia.id'
            tagliaFK = 'taglia.id'
            coloreFK = 'colore.id'
            annoFK = 'anno_abbigliamento.id'
            stagioneabbigliamentoFK = 'stagione_abbigliamento.id'
            genereabbigliamentoFK = 'genere_abbigliamento.id'
            modelloFK = 'modello.id'
            gruppoTTFK1 = 'gruppo_taglia_taglia.id_gruppo_taglia'
            gruppoTTFK2 = 'gruppo_taglia_taglia.id_taglia'
        else:
            articoloFK = params['schema']+'.articolo.id'
            gruppoTagliaFK = params['schema']+'.gruppo_taglia.id'
            tagliaFK = params['schema']+'.taglia.id'
            coloreFK = params['schema']+'.colore.id'
            annoFK = params['mainSchema']+'.anno_abbigliamento.id'
            stagioneabbigliamentoFK = params['mainSchema']+'.stagione_abbigliamento.id'
            genereabbigliamentoFK = params['mainSchema']+'.genere_abbigliamento.id'
            modelloFK = params['schema']+'.modello.id'
            gruppoTTFK1 = params['schema']+'.gruppo_taglia_taglia.id_gruppo_taglia'
            gruppoTTFK2 = params['schema']+'.gruppo_taglia_taglia.id_taglia'
            articolo=Table('articolo',params['metadata'],schema = params['schema'],autoload=True)


        articoloTagliaColoreTable = Table('articolo_taglia_colore', params['metadata'],
                    Column('id_articolo',Integer,ForeignKey(articoloFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                    Column('id_articolo_padre',Integer,ForeignKey(articoloFK,onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_gruppo_taglia',Integer,ForeignKey(gruppoTagliaFK,onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_taglia',Integer,ForeignKey(tagliaFK,onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_colore',Integer,ForeignKey(coloreFK,onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_anno',Integer,ForeignKey(annoFK,onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_stagione',Integer,ForeignKey(stagioneabbigliamentoFK,onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_genere',Integer,ForeignKey(genereabbigliamentoFK,onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_modello',Integer,ForeignKey(modelloFK,onupdate="CASCADE",ondelete="CASCADE")),
                    UniqueConstraint('id_articolo_padre', 'id_gruppo_taglia', "id_taglia", "id_colore"),
                    ForeignKeyConstraint(['id_gruppo_taglia', 'id_taglia'],[gruppoTTFK1,gruppoTTFK2]),
                    #CheckConstraint("(( id_taglia IS NOT NULL ) AND ( id_colore IS NOT NULL ) AND ( id_gruppo_taglia IS NOT NULL ) AND ( id_articolo_padre IS NOT NULL )) OR (( id_taglia IS NULL ) AND ( id_colore IS NULL ) AND ( id_gruppo_taglia IS NOT NULL ) AND ( id_articolo_padre IS NULL ))"),
                    schema=params['schema'])
        articoloTagliaColoreTable.create(checkfirst=True)

        conf.PromoWear.primoavvio = "no"
        conf.save()
