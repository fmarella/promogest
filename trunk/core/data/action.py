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

t_action = Table('action', params["metadata"],
    Column('id', Integer, primary_key=True),
    Column('denominazione_breve', String(25), nullable=False),
    Column('denominazione', String(200), nullable=False),
    schema=params["mainSchema"],
    extend_existing=True
    )
t_action.create(checkfirst=True)


s= select([t_action.c.id]).execute().fetchall()
azioni  = t_action.insert()

if (1,) not in s:
    azioni.execute(id=1, denominazione_breve = "LOGIN", denominazione = "Puo' effettuare il login nell'applicazione")
if (2,) not in s:
    azioni.execute(id=2, denominazione_breve = "DOCUMENTI", denominazione = "Puo' accedere alla sezione documenti")
if (3,) not in s:
    azioni.execute(id=3, denominazione_breve = "SALVA", denominazione = "Puo' effettuare degli inserimenti nell'applicazione")
if (4,) not in s:
    azioni.execute(id=4, denominazione_breve = "MODIFICA", denominazione = "Puo' effettuare delle modifiche ai dati nel Database")
if (5,) not in s:
    azioni.execute(id=5, denominazione_breve = "INSERIMENTO", denominazione = "Puo' effettuare degli inserimenti nel database")
if (6,) not in s:
    azioni.execute(id=6, denominazione_breve = "PARAMETRI", denominazione = "Gestione parametri ")
if (7,) not in s:
    azioni.execute(id=7, denominazione_breve = "RUOLI", denominazione = "Gestione Ruoli")
if (8,) not in s:
    azioni.execute(id=8, denominazione_breve = "ARTICOLI", denominazione = "Gestione articoli")
if (9,) not in s:
    azioni.execute(id=9, denominazione_breve = "LISTINI", denominazione = "Accesso alla sezione Listini")
if (10,) not in s:
    azioni.execute(id=10, denominazione_breve = "DETTAGLIO", denominazione = "Accesso al modulo al dettaglio")
if (11,) not in s:
    azioni.execute(id=11, denominazione_breve = "ANAGRAFICHE", denominazione = "Accesso alla sezione Anagrafiche del Programma")
if (12,) not in s:
    azioni.execute(id=12, denominazione_breve = "MAGAZZINI", denominazione = "Accesso alla sezione Magazzini")
if (13,) not in s:
    azioni.execute(id=13, denominazione_breve = "PROMEMORIA", denominazione = "Accesso alla sezione promemoria")
if (14,) not in s:
    azioni.execute(id=14, denominazione_breve = "CONFIGURAZIONE", denominazione = "Puo' effettuare modifiche alla configurazione")
if (15,) not in s:
    azioni.execute(id=15, denominazione_breve = "PRIMANOTA", denominazione = "Accesso prima nota cassa")
if (16,) not in s:
    azioni.execute(id=16, denominazione_breve = "WEB-LOGIN", denominazione = "Accesso semplice alla piattaforma WEB")
if (17,) not in s:
    azioni.execute(id=17, denominazione_breve = "WEB-ADMIN", denominazione = "Accesso completo alla piattaforma WEB")
