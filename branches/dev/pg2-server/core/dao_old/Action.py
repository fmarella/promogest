# -*- coding: utf-8 -*-

# Promogest - Janas
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>


from sqlalchemy import *
from sqlalchemy.orm import *
from core.Environment import *
from Dao import Dao

actionTable = Table('action', params['metadata'],
    Column('id', Integer, primary_key=True),
    Column('denominazione_breve', String(25), nullable=False),
    Column('denominazione', String(200), nullable=False),
    schema = params['mainSchema'],
    )
actionTable.create(checkfirst=True)
s= select([actionTable.c.denominazione_breve]).execute().fetchall()
if (u'LOGIN',) not in s or s==[]:
    azioni  = actionTable.insert()
    azioni.execute(denominazione_breve = "LOGIN", denominazione = "Puo' effettuare il login nell'applicazione")
    azioni.execute(denominazione_breve = "SITEADMIN", denominazione = "Puo' accedere alla sezione documenti")
    azioni.execute(denominazione_breve = "CANCELLARE", denominazione = "Puo' effettuare degli inserimenti nell'applicazione")
    azioni.execute(denominazione_breve = "MODIFICA", denominazione = "Puo' effettuare delle modifiche ai dati nel Database")
    azioni.execute(denominazione_breve = "INSERIMENTO", denominazione = "Puo' effettuare degli inserimenti nel database")
    azioni.execute(denominazione_breve = "CONFIGURAZIONE", denominazione = "Puo' effettuare modifiche alla configurazione")
    azioni.execute(denominazione_breve = "DMZ", denominazione = "Puo' effettuare modifiche alla configurazione")

class Action(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {  'denominazione' : action.c.denominazione.ilike("%"+v+"%")}
        return  dic[k]

action=Table('action',
            params['metadata'],
            schema = params['mainSchema'],
            autoload=True)

std_mapper = mapper(Action, action, order_by=action.c.id)