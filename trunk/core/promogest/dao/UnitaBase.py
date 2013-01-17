# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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

class UnitaBase(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)
        #self.addMC()

    def filter_values(self,k,v):
        dic= {'denominazione' : unitabase.c.denominazione ==v}
        return  dic[k]

    #def addMC(self):
        #mc = self.select(denominazione ="Metri Cubi")
        #if not mc:
            #self.denominazione_breve = "mc"
            #self.denominazione = "Metri Cubi"
            #self.persist()
        #gr = self.select(denominazione ="Grammi")
        #if not gr:
            #self.denominazione_breve = "gr"
            #self.denominazione = "Grammi"
            #self.persist()
        #ml = self.select(denominazione ="Millilitri")
        #if not ml:
            #self.denominazione_breve = "ml"
            #self.denominazione = "Millilitri"
            #self.persist()
        #q = self.select(denominazione ="Quintali")
        #if not q:
            #self.denominazione_breve = "q"
            #self.denominazione = "Quintali"
            #self.persist()

unitabase=Table('unita_base',
                params['metadata'],
                schema = params['mainSchema'],
                autoload=True)

s= select([unitabase.c.denominazione_breve]).execute().fetchall()
if (u'mc',) not in s or s==[]:
    o = unitabase.insert()
    o.execute(denominazione = "Metri Cubi",denominazione_breve="mc")
if (u'gr',) not in s or s==[]:
    o = unitabase.insert()
    o.execute(denominazione = "Grammi",denominazione_breve="gr")
if (u'ml',) not in s or s==[]:
    o = unitabase.insert()
    o.execute(denominazione = "Millilitri",denominazione_breve="ml")
if (u'q',) not in s or s==[]:
    o = unitabase.insert()
    o.execute(denominazione = "Quintali",denominazione_breve="q")
if (u't',) not in s or s==[]:
    o = unitabase.insert()
    o.execute(denominazione = "Tonnellate",denominazione_breve="t")



std_mapper = mapper(UnitaBase,unitabase)
