# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from promogest.Environment import params
from Dao import Dao

class Setting(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=='keys':
            dic= {  k : settingg.c.key.ilike("%"+v+"%")}
        elif k == 'description':
            dic = {k:settingg.c.description.ilike("%"+v+"%")}
        elif k == 'value':
            dic = {k:settingg.c.value == v}
        return  dic[k]

settingg=Table('setting',params['metadata'],schema = params['schema'],autoload=True)

s= select([settingg.c.key]).execute().fetchall()
if (u'Fattura pro-forma.registro',) not in s or s==[]:
    settinggg  = settingg.insert()
    settinggg.execute(key = "Fattura pro-forma.registro", description = "Registro associato a Fattura pro-forma", value= "registro_fattura_pro-forma")
    settinggg.execute(key = "registro_fattura_pro-forma.rotazione", description = "Tipologia di rotazione registro associato a Fattura pro-forma ", value= "annuale")

if (u'Ordine a magazzino.registro',) not in s or s==[]:
    settinggg  = settingg.insert()
    settinggg.execute(key = "Ordine a magazzino.registro", description = "Registro associato a Ordine a magazzino", value= "registro_ordine_a_magazzino")
    settinggg.execute(key = "registro_ordine_a_magazzino.rotazione", description = "Tipologia di rotazione registro associato a Ordine a magazzino ", value= "annuale")

if (u'Ordine beni strumentali.registro',) not in s or s==[]:
    settinggg  = settingg.insert()
    settinggg.execute(key = "Ordine beni strumentali.registro", description = "Registro associato a Ordine beni strumentali", value= "registro_ordine_beni_strumentali")
    settinggg.execute(key = "registro_ordine_beni_strumentali.rotazione", description = "Tipologia di rotazione registro associato a Ordine beni strumentali ", value= "annuale")

if (u'Preventivo dettaglio.registro',) not in s or s==[]:
    settinggg  = settingg.insert()
    settinggg.execute(key = "Preventivo dettaglio.registro", description = "Registro associato a Preventivo dettaglio", value= "registro_preventivo")


std_mapper = mapper(Setting, settingg, order_by=settingg.c.key)
