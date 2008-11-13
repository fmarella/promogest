# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


#def create()
if hasattr(conf, 'PromoWear'):
    if conf.PromoWear.primoavvio=="yes":
        """ tabelle schema principale """

        #creo tabella anno abbigliamento in schema principale e ci metto i dati di default
        annoAbbigliamentoTable = Table('anno_abbigliamento', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('denominazione',String(50),nullable=False),
                            schema=params['mainSchema'])
        annoAbbigliamentoTable.create(checkfirst=True)
        s= select([annoAbbigliamentoTable.c.denominazione]).execute().fetchall()
        if (u'2008',) not in s or s==[]:
            tipo = annoAbbigliamentoTable.insert()
            tipo.execute(denominazione='2008')
            tipo.execute(denominazione='2009')
            tipo.execute(denominazione='2010')
            tipo.execute(denominazione='2011')
            tipo.execute(denominazione='2012')
            tipo.execute(denominazione='2013')

        #creo tabella genere_abbigliamento e ci metto i valori di default
        genereAbbigliamentoTable = Table('genere_abbigliamento', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('denominazione',String(50),nullable=False),
                            schema=params['mainSchema'])
        genereAbbigliamentoTable.create(checkfirst=True)
        s= select([genereAbbigliamentoTable.c.denominazione]).execute().fetchall()
        if (u'Unisex',) not in s or s==[]:
            tipo = genereAbbigliamentoTable.insert()
            tipo.execute(denominazione='Unisex')
            tipo.execute(denominazione='Uomo')
            tipo.execute(denominazione='Donna')
            tipo.execute(denominazione='Bambino')

        stagioneAbbigliamentoTable = Table('stagione_abbigliamento', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('denominazione',String(50),nullable=False),
                            schema=params['mainSchema'])
        stagioneAbbigliamentoTable.create(checkfirst=True)
        s= select([stagioneAbbigliamentoTable.c.denominazione]).execute().fetchall()
        if (u'Primavera - Estate',) not in s or s==[]:
            tipo = genereAbbigliamentoTable.insert()
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
        s= select([coloreTable.c.denominazione]).execute().fetchall()
        if (u'n/a',) not in s or s==[]:
            tipo = coloreTable.insert()
            tipo.execute(denominazione='n/a', denominazione_breve='n/a')

        #tabella GRUPPO TAGLIA
        gruppoTagliaTable = Table('gruppo_taglia', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione', 'denominazione_breve'),
                schema=params["schema"])
        gruppoTagliaTable.create(checkfirst=True)
        s= select([gruppoTagliaTable.c.denominazione]).execute().fetchall()
        if (u'n/a',) not in s or s==[]:
            tipo = gruppoTagliaTable.insert()
            tipo.execute(denominazione='n/a', denominazione_breve='n/a')

        #tabella TAGLIA
        tagliaTable = Table('taglia', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('denominazione_breve',String(20),nullable=False),
                Column('denominazione',String(200),nullable=False),
                UniqueConstraint('denominazione_breve'),
                schema=params["schema"])
        tagliaTable.create(checkfirst=True)
        s= select([tagliaTable.c.denominazione]).execute().fetchall()
        if (u'n/a',) not in s or s==[]:
            tipo = tagliaTable.insert()
            tipo.execute(denominazione='n/a', denominazione_breve='n/a')

        #tabella TAGLIA
        gruppoTagliaTagliaTable = Table('gruppo_taglia_taglia', params['metadata'],
                Column('id_gruppo_taglia',Integer,ForeignKey(params['schema']+'.gruppo_taglia.id',onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
                Column('id_taglia',Integer,ForeignKey(params['schema']+'.taglia.id',onupdate="CASCADE",ondelete="RESTRICT"),primary_key=True),
                Column('ordine',Integer,nullable=False),
                schema=params["schema"])
        gruppoTagliaTagliaTable.create(checkfirst=True)
        s= select([gruppoTagliaTagliaTable.c.ordine]).execute().fetchall()
        if (1,) not in s or s==[]:
            tipo = gruppoTagliaTagliaTable.insert()
            tipo.execute(id_gruppo_taglia=1, id_taglia=1, ordine=1)

        #tabella articolo taglia colore
        articolo=Table('articolo', params['metadata'],schema = params['schema'],autoload=True)
        articoloTagliaColoreTable = Table('articolo_taglia_colore', params['metadata'],
                    Column('id_articolo',Integer,ForeignKey(params['schema']+'.articolo.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
                    Column('id_articolo_padre',Integer,ForeignKey(params['schema']+'.articolo.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_gruppo_taglia',Integer,ForeignKey(params['schema']+'.gruppo_taglia.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_taglia',Integer,ForeignKey(params['schema']+'.taglia.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_colore',Integer,ForeignKey(params['schema']+'.colore.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_anno',Integer,ForeignKey(params['mainSchema']+'.anno_abbigliamento.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_stagione',Integer,ForeignKey(params['mainSchema']+'.stagione_abbigliamento.id',onupdate="CASCADE",ondelete="CASCADE")),
                    Column('id_genere',Integer,ForeignKey(params['mainSchema']+'.genere_abbigliamento.id',onupdate="CASCADE",ondelete="CASCADE")),
                    UniqueConstraint('id_articolo_padre', 'id_gruppo_taglia', "id_taglia", "id_colore"),
                    ForeignKeyConstraint(['id_gruppo_taglia', 'id_taglia'],[params['schema']+'.gruppo_taglia_taglia.id_gruppo_taglia',params['schema']+'.gruppo_taglia_taglia.id_taglia']),
                    CheckConstraint("(( id_taglia IS NOT NULL ) AND ( id_colore IS NOT NULL ) AND ( id_gruppo_taglia IS NOT NULL ) AND ( id_articolo_padre IS NOT NULL )) OR (( id_taglia IS NULL ) AND ( id_colore IS NULL ) AND ( id_gruppo_taglia IS NOT NULL ) AND ( id_articolo_padre IS NULL ))"),
                    schema=params['schema'])
        articoloTagliaColoreTable.create(checkfirst=True)

        conf.PromoWear.primoavvio = "no"
        conf.save()
