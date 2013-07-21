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
from sqlalchemy.orm import *

class ActionDb(object):

    def __init__(self, schema = None, mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.mainSchema = mainSchema
        self.debug = debug

    def create(self):
        actionTable = Table('action', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('denominazione_breve', String(25), nullable=False),
            Column('denominazione', String(200), nullable=False),
            schema=self.mainSchema
            )
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
            azioni.execute(denominazione_breve = "PRIMANOTA", denominazione = "Accesso prima nota cassa")



    def data(self):
        actionTable = Table('action',self.metadata, autoload=True)
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
        azioni.execute(denominazione_breve = "PRIMANOTA", denominazione = "Accesso prima nota cassa")
