# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from promogest.dao.Dao import Dao, Base


class Action(Base, Dao):
    try:
        __table__ = Table('action', params['metadata'],
                                    schema=params['mainSchema'],
                                    autoload=True,
                                    autoload_with=engine)
    except:
        __table__ = Table('action', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('denominazione_breve', String(25), nullable=False),
            Column('denominazione', String(200), nullable=False),
                schema=params["mainSchema"]
                        )

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k =="denominazione":
            dic= {k: Action.__table__.c.denominazione.ilike("%"+v+"%")}
        elif k == "denominazione_breve":
            dic= {k: Action.__table__.c.denominazione_breve ==v}
        return  dic[k]

    def delete(self):
        return


#s= select([Action.__table__.c.id]).execute().fetchall()
#azioni  = Action.__table__.insert()
#if (16,) not in s:
    #azioni.execute(id=16, denominazione_breve = "WEB-LOGIN", denominazione = "Accesso semplice alla piattaforma WEB")
#if (17,) not in s:
    #azioni.execute(id=17, denominazione_breve = "WEB-ADMIN", denominazione = "Accesso completo alla piattaforma WEB")
#if (18,) not in s:
    #azioni.execute(id=18, denominazione_breve = "GEST-COMMESSE", denominazione = "Accesso completo gestione commesse")
#if (19,) not in s:
    #azioni.execute(id=19, denominazione_breve = "CANCELLAZIONE", denominazione = "Può cancellare dati dal Database")
#if (20,) not in s:
    #azioni.execute(id=20, denominazione_breve = "CMS", denominazione = "Può scrivere e modificare i contenuti")
