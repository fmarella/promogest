# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

if hasattr(conf, 'DistintaBase'):
    if conf.DistintaBase.primoavvio=="yes":
        """ tabelle schema principale """

        #CREATE TABLE associazioni_articoli(
            #id              BIGSERIAL   NOT NULL    PRIMARY KEY
            #,id_padre       BIGINT          NULL    REFERENCES articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
            #,id_figlio      BIGINT          NULL    REFERENCES articolo ( id ) ON UPDATE CASCADE ON DELETE RESTRICT
            #,posizione      INTEGER         NULL
            #-- sono tutti riferimenti esterni alla tabella articolo. Questa tabella associa
            #-- ad n articoli, n altri articoli della stessa tabella
            #,UNIQUE (id_padre,id_figlio));
        associazioneArticoloTable = Table('associazione_articolo', params['metadata'],
                            Column('id',Integer,primary_key=True),
                            Column('id_padre',Integer,ForeignKey(params['schema']+'.articolo.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=True),
                            Column('id_figlio',Integer,ForeignKey(params['schema']+'.articolo.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=True),
                            Column('quantita',Numeric),
                            Column('posizione',Integer,nullable=True),
                            UniqueConstraint('id_padre', 'id_figlio'),
                            schema=params['schema'])
        associazioneArticoloTable.create(checkfirst=True)

        conf.DistintaBase.primoavvio = "no"
        conf.save()