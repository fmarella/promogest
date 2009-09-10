# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
#from promogest.dao.Dao import Dao

#def create()
if hasattr(conf, 'VenditaDettaglio'):
    #if conf.VenditaDettaglio.primoavvio=="yes":

    testataMovimentoTable = Table('testata_movimento', params['metadata'], autoload=True, schema=params['schema'])
    testataScontrinoTable = Table('testata_scontrino', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('data_inserimento',DateTime,PassiveDefault(func.now()),nullable=False),
                Column('totale_scontrino',Numeric(16,4),nullable=False),
                Column('totale_contanti',Numeric(16,4),nullable=False),
                Column('totale_assegni',Numeric(16,4),nullable=False),
                Column('totale_carta_credito',Numeric(16,4),nullable=False),
                #chiavi esterne
                Column('id_testata_movimento',Integer,ForeignKey(params['schema']+'.testata_movimento.id', onupdate="CASCADE", ondelete="RESTRICT")),
                schema=params['schema']
                )
    testataScontrinoTable.create(checkfirst=True)

    #testataScontrinoTable = Table('testata_scontrino', params['metadata'], autoload=True, schema=params['schema'])
    articoloTable = Table('articolo', params['metadata'], autoload=True, schema=params['schema'])

    rigaScontrinoTable = Table('riga_scontrino', params['metadata'],
            Column('id',Integer,primary_key=True),
            Column('prezzo',Numeric(16,4),nullable=True),
            Column('prezzo_scontato',Numeric(16,4),nullable=True),
            Column('quantita',Numeric(16,4),nullable=False),
            Column('descrizione',String(200),nullable=False),
            #chiavi esterne
            Column('id_testata_scontrino',Integer,ForeignKey(params['schema'] +'.testata_scontrino.id', onupdate="CASCADE", ondelete="CASCADE"),nullable=True),
            Column('id_articolo',Integer, ForeignKey(params['schema'] +'.articolo.id', onupdate="CASCADE", ondelete="RESTRICT"),nullable=False),
            schema=params['schema']
            )
    rigaScontrinoTable.create(checkfirst=True)

    #rigaDocumentoTable = Table('riga_scontrino', params['metadata'], autoload=True, schema=params['schema'])
    rigaDotoTable = Table('sconto', params['metadata'], autoload=True, schema=params['schema'])

    scontoRigaScontrinoTable = Table('sconto_riga_scontrino', params['metadata'],
            Column('id',Integer,ForeignKey(params['schema'] +'.sconto.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_riga_scontrino',Integer,ForeignKey(params['schema']+'.riga_scontrino.id',onupdate="CASCADE",ondelete="CASCADE")),
            schema=params['schema'])
    scontoRigaScontrinoTable.create(checkfirst=True)

    chiusuraFiscaleTable = Table('chiusura_fiscale', params['metadata'],
                Column('id',Integer,primary_key=True),
                Column('data_chiusura',DateTime, unique=True, nullable=False),
                schema=params['schema']
                )
    chiusuraFiscaleTable.create(checkfirst=True)

        #se tutto è andato bene ..... posso settare la variabile primoavvio su False
        #conf.VenditaDettaglio.primoavvio = "no"
        #conf.save()

    testatascontrinoTable = Table('testata_scontrino', params['metadata'], autoload=True, schema=params['schema'])
    testataDoctoTable = Table('sconto', params['metadata'], autoload=True, schema=params['schema'])
    scontoTestataScontrinoTable = Table('sconto_testata_scontrino', params['metadata'],
            Column('id',Integer,ForeignKey(params['schema']+'.sconto.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_testata_scontrino',Integer,ForeignKey(params['schema']+'.testata_scontrino.id',onupdate="CASCADE",ondelete="CASCADE")),
            schema=params['schema']
            )
    scontoTestataScontrinoTable.create(checkfirst=True)
