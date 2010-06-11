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

actionTable = Table('action', meta,
    Column('id', Integer, primary_key=True),
    Column('denominazione_breve', String(25), nullable=False),
    Column('denominazione', String(200), nullable=False),
    schema=MAINSCHEMA,useexisting=True)

actionTable.create(checkfirst=True)
s= select([actionTable.c.denominazione_breve]).execute().fetchall()
if (u'LOGIN',) not in s or s==[]:
    azioni  = actionTable.insert()
    azioni.execute(denominazione_breve = "LOGIN", denominazione = "Puo' effettuare il login nell'applicazione")
    azioni.execute(denominazione_breve = "DOCUMENTI", denominazione = "Puo' accedere alla sezione documenti")
    azioni.execute(denominazione_breve = "SALVA", denominazione = "Puo' effettuare degli inserimenti nell'applicazione")
    azioni.execute(denominazione_breve = "MODIFICA", denominazione = "Puo' effettuare delle modifiche ai dati nel Database")
    azioni.execute(denominazione_breve = "INSERIMENTO", denominazione = "Puo' effettuare degli inserimenti nel database")
    azioni.execute(denominazione_breve = "PARAMETRI", denominazione = "Gestione parametri ")
    azioni.execute(denominazione_breve = "RUOLI", denominazione = "Gestione Ruoli")
    azioni.execute(denominazione_breve = "ARTICOLI", denominazione = "Gestione articoli")
    azioni.execute(denominazione_breve = "LISTINI", denominazione = "Accesso alla sezione Listini")
    azioni.execute(denominazione_breve = "DETTAGLIO", denominazione = "Accesso al modulo al dettaglio")
    azioni.execute(denominazione_breve = "ANAGRAFICHE", denominazione = "Accesso alla sezione Anagrafiche del Programma")
    azioni.execute(denominazione_breve = "MAGAZZINI", denominazione = "Accesso alla sezione Magazzini")
    azioni.execute(denominazione_breve = "PROMEMORIA", denominazione = "Accesso alla sezione promemoria")
    azioni.execute(denominazione_breve = "CONFIGURAZIONE", denominazione = "Puo' effettuare modifiche alla configurazione")


roleTable = Table('role', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String(50), nullable=False),
        Column('descrizione', String(250), nullable=False),
        Column('id_listino', Integer),
        Column('active', Boolean, default=0),
        schema=MAINSCHEMA,useexisting=True)

roleTable.create(checkfirst=True)
s= select([roleTable.c.name]).execute().fetchall()
if (u'Admin',) not in s or s ==[]:
    ruoli = roleTable.insert()
    ruoli.execute(name = "Admin", descrizione = "Gestore del promogest", active = True)
    ruoli.execute(name = "Magazzino", descrizione = "Gestione magazzino", active = True)
    ruoli.execute(name = "Venditore", descrizione = "Addetto alla vendita", active = True)
    ruoli.execute(name = "Fatturazione", descrizione = "Fatturazione", active = True)

roleTable = Table('role',meta, autoload=True, schema=MAINSCHEMA)
actionTable = Table('action',meta, autoload=True, schema=MAINSCHEMA)

roleactionTable = Table('roleaction', meta,
        Column('id_role', Integer, ForeignKey(MAINSCHEMA+'.role.id'),primary_key=True),
        Column('id_action', Integer, ForeignKey(MAINSCHEMA+'.action.id'),primary_key=True),
        schema=MAINSCHEMA,useexisting=True
        )
roleactionTable.create(checkfirst=True)
s= select([roleactionTable.c.id_role]).execute().fetchall()
if (1,) not in s or s ==[]:
    ruolieazioni = roleactionTable.insert()
    for i in range(1,15):
        ruolieazioni.execute(id_role = 1, id_action =i)

userTable = Table('utente',meta, autoload=True, schema=MAINSCHEMA)
roleTable = Table('role',meta, autoload=True, schema=MAINSCHEMA)
userroleTable = Table('userrole', meta,
        Column('id_role', Integer, ForeignKey(MAINSCHEMA+'.role.id'),primary_key=True),
        Column('id_user', Integer, ForeignKey(MAINSCHEMA+'.utente.id'),primary_key=True),
        schema=MAINSCHEMA,useexisting=True
        )
userroleTable.create(checkfirst=True)
s= select([userroleTable.c.id_role]).execute().fetchall()
if (1,) not in s or s ==[]:
    userruoli = userroleTable.insert()
    userruoli.execute(id_role = 1, id_user =1)

        #se tutto è andato bene ..... posso settare la variabile primoavvio su False
        #conf.RuoliAzioni.primoavvio = "no"
        #conf.save()

