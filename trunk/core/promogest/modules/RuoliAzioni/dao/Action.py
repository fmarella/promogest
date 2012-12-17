# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012,2011 by Promotux
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


try:
    t_action=Table('action',
            params['metadata'],
            schema = params['mainSchema'],
            autoload=True)
except:
    if tipodb == "sqlite":
        t_action = Table('action', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('denominazione_breve', String(25), nullable=False),
            Column('denominazione', String(200), nullable=False),
            schema=params["mainSchema"],
            useexisting=True)
        t_action.create(checkfirst=True)
        s= select([t_action.c.denominazione_breve]).execute().fetchall()
        if (u'LOGIN',) not in s or s==[]:
            azioni  = t_action.insert()
            azioni.execute(denominazione_breve="LOGIN", denominazione="Puo' effettuare il login nell'applicazione")
            azioni.execute(denominazione_breve="DOCUMENTI", denominazione="Puo' accedere alla sezione documenti")
            azioni.execute(denominazione_breve="SALVA", denominazione="Puo' effettuare degli inserimenti nell'applicazione")
            azioni.execute(denominazione_breve="MODIFICA", denominazione="Puo' effettuare delle modifiche ai dati nel Database")
            azioni.execute(denominazione_breve="INSERIMENTO", denominazione="Puo' effettuare degli inserimenti nel database")
            azioni.execute(denominazione_breve="PARAMETRI", denominazione="Gestione parametri ")
            azioni.execute(denominazione_breve="RUOLI", denominazione="Gestione Ruoli")
            azioni.execute(denominazione_breve="ARTICOLI", denominazione="Gestione articoli")
            azioni.execute(denominazione_breve="LISTINI", denominazione="Accesso alla sezione Listini")
            azioni.execute(denominazione_breve="DETTAGLIO", denominazione="Accesso al modulo al dettaglio")
            azioni.execute(denominazione_breve="ANAGRAFICHE", denominazione="Accesso alla sezione Anagrafiche del Programma")
            azioni.execute(denominazione_breve="MAGAZZINI", denominazione="Accesso alla sezione Magazzini")
            azioni.execute(denominazione_breve="PROMEMORIA", denominazione="Accesso alla sezione promemoria")
            azioni.execute(denominazione_breve="CONFIGURAZIONE", denominazione="Puo' effettuare modifiche alla configurazione")
            azioni.execute(denominazione_breve="PRIMANOTA", denominazione="Accesso alla sezione prima nota cassa")


class Action(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k =="denominazione":
            dic= {k: t_action.c.denominazione.ilike("%"+v+"%")}
        elif k == "denominazione_breve":
            dic= {k: t_action.c.denominazione_breve ==v}
        return  dic[k]

std_mapper = mapper(Action, t_action, order_by=t_action.c.id)

#pn = Action().select(denominazione_breve = "PRIMANOTA")
#if not pn:
    #a = Action()
    #a.denominazione_breve = "PRIMANOTA"
    #a.denominazione =  "Accesso alla sezione prima nota cassa"
    #a.persist()
