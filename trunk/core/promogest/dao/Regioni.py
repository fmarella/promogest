# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 2011by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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
from Dao import Dao

try:
    regioni=Table('regione', params['metadata'],schema = params['mainSchema'],autoload=True)

except:
    regioni  = Table('regione', params["metadata"],
            Column('id',Integer,primary_key=True),
            Column('denominazione',String(100)),
            Column('codice',Integer),
            schema = params['mainSchema'])

    regioni.create(checkfirst=True)
    s= select([regioni.c.denominazione]).execute().fetchall()
    if (u'Piemonte',) not in s or s ==[]:
        tipo = regioni.insert()
        tipo.execute(codice = "01", denominazione='Piemonte')
        tipo.execute(codice = "02", denominazione="Valle D'Aosta")
        tipo.execute(codice = "03", denominazione="Lombardia")
        tipo.execute(codice = "04", denominazione="Trentino Alto Adige")
        tipo.execute(codice = "05", denominazione="Veneto")
        tipo.execute(codice = "06", denominazione="Friuli Venezia Giulia")
        tipo.execute(codice = "07", denominazione="Liguria")
        tipo.execute(codice = "08", denominazione="Emilia Romagna")
        tipo.execute(codice = "09", denominazione="Toscana")
        tipo.execute(codice = "10", denominazione="Umbria")
        tipo.execute(codice = "11", denominazione="Marche")
        tipo.execute(codice = "12", denominazione="Lazio")
        tipo.execute(codice = "13", denominazione="Abruzzo")
        tipo.execute(codice = "14", denominazione="Molise")
        tipo.execute(codice = "15", denominazione="Campania")
        tipo.execute(codice = "16", denominazione="Puglia")
        tipo.execute(codice = "17", denominazione="Basilicata")
        tipo.execute(codice = "18", denominazione="Calabria")
        tipo.execute(codice = "19", denominazione="Sicilia")
        tipo.execute(codice = "20", denominazione="Sardegna")

class Regioni(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione':regioni.c.denominazione == v,
                }
        return  dic[k]

std_mapper = mapper(Regioni, regioni,order_by=regioni.c.denominazione)
