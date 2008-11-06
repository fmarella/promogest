# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao


if hasattr(conf, 'SuMisura'):
    if conf.SuMisura.primoavvio=="yes":
        rigaTable = Table('riga', params['metadata'], autoload=True, schema=params['schema'])
        misurapezzoTable = Table('misura_pezzo', params['metadata'],
                    Column('id',Integer,primary_key=True),
                    Column('altezza',Numeric(16,4),nullable=False),
                    Column('larghezza',Numeric(16,4),nullable=False),
                    Column('moltiplicatore',Numeric(16,4),nullable=False),
                    #chiavi esterne
                    Column('id_riga',Integer,ForeignKey(params['schema']+'.riga.id', onupdate="CASCADE", ondelete="RESTRICT")),
                    UniqueConstraint('id_riga'),
                    schema=params['schema'])
        misurapezzoTable.create(checkfirst=True)
        print "HO CREATO LA TABELLA MISURA PEZZO NECESSARIA PER IL MODULO SuMisura DEL PROMOGEST2"
        #se tutto è andato bene ..... posso settare la variabile primoavvio su False
        conf.SuMisura.primoavvio = "no"
        conf.save()
