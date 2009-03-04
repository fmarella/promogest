#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

"""ATTENZIONE questo script va spostato dalla cartella data del modulo RuoleAzioni
    alla cartella radice dei sorgenti ( dove si trova il create_db per capirci
    e lanciato da li dopo aver correttamente impostato i valori sottostanti
"""
MAINSCHEMA = "promogest2"
SCHEMA = "aaaaa" # da passare anche come primo parametri al lancio del comando
USER = "promoadmin"
PASSWORD = "admin"
HOST = "localhost"
PORT = 5432
DATABASE = "promogest_db"
VERSIONE_DB = "0.9.10"

db = create_engine('postgres://'+USER + ':' + PASSWORD +'@'+ HOST +':'+ str(PORT) +'/'+ DATABASE,
                    encoding='utf-8',
                    convert_unicode=True )
db.echo = True
meta = MetaData(db)
session = create_session(db)

app_table = Table('app_log', meta,
        Column('id', Integer, primary_key=True),
        Column('id_utente', Integer),
        Column('utentedb', String(100), nullable=False),
        Column('schema_azienda', String(100), nullable=False),
        Column('level', String(1)),
        Column('object', PickleType, nullable=True),
        Column('message', String(1000), nullable=True),
        Column('value', Integer, nullable=True),
        Column('registration_date', DateTime),
        schema=MAINSCHEMA)

app_table.create(checkfirst=True)

primy_keyTable = Table('chiavi_primarie_log', meta,
        Column('id', Integer, primary_key=True),
        Column('pk_integer', Integer, nullable=True),
        Column('pk_string', String(300), nullable=True),
        Column('pk_datetime', DateTime,nullable=True),
        Column('id_application_log2', Integer,ForeignKey(params['mainSchema']+'.app_log.id',onupdate="CASCADE",ondelete="CASCADE"), nullable=False),
        schema=MAINSCHEMA)
primy_keyTable.create(checkfirst=True)

        #se tutto è andato bene ..... posso settare la variabile primoavvio su False
        #conf.RuoliAzioni.primoavvio = "no"
        #conf.save()

