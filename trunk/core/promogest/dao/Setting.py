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
    """SCHEMA: cl | registro | registro da modificare | registro da assegnare

    esempio:
    cl|registro|Fattura differita vendita|registro_fattura_vendita

    tabella corrente:
         operazioni.registri | registri possibili

    DDT acquisto.registro | registro_ddt_acquisto
    DDT reso a fornitore.registro | registro_ddt_reso_a_fornitore
    DDT reso da cliente.registro | registro_ddt_reso_da_cliente
    DDT vendita.registro | registro_ddt_vendita
    Fattura accompagnatoria.registro | registro_fattura_accompagnatoria
    Fattura acquisto.registro | registro_fattura_acquisto
    Fattura differita acquisto.registro | registro_vendita_dettaglio
    Fattura differita vendita.registro | registro_fattura_differita_vendita
    Fattura vendita.registro | registro_fattura_vendita
    Movimento.registro | registro_movimenti
    Nota di credito a cliente.registro | registro_nota_credito_a_cliente
    Nota di credito da fornitore.registro | registro_nota_credito_da_fornitore
    Ordine a fornitore.registro | registro_ordine_a_fornitore
    Ordine da cliente.registro | registro_ordine_da_cliente
    Preventivo.registro | registro_preventivo
    Vendita dettaglio.registro | registro_vendita_dettaglio
    """
    def __init__(self, req=None):
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

if (u'Carico da composizione kit.registro',) not in s or s==[]:
    settinggg  = settingg.insert()
    settinggg.execute(key = "Carico da composizione kit.registro", description = "Registro associato a Carico da composizione kit", value= "registro_carico_da_composizione_kit")
    settinggg.execute(key = "carico_da_composizione_kit.rotazione", description = "Tipologia di rotazione registro associato a Carico da composizione kit", value= "annuale")

if (u'Trasferimento merce magazzino.registro',) not in s or s==[]:
    settinggg  = settingg.insert()
    settinggg.execute(key = "Trasferimento merce magazzino.registro", description = "Registro associato a Trasferimento merce magazzino", value= "trasferimento_merce_magazzino")
    settinggg.execute(key = "trasferimento_merce_magazzino.rotazione", description = "Tipologia di rotazione registro associato a Trasferimento merce magazzino", value= "annuale")


if (u'Ordine beni strumentali.registro',) not in s or s==[]:
    settinggg  = settingg.insert()
    settinggg.execute(key = "Ordine beni strumentali.registro", description = "Registro associato a Ordine beni strumentali", value= "registro_ordine_beni_strumentali")
    settinggg.execute(key = "registro_ordine_beni_strumentali.rotazione", description = "Tipologia di rotazione registro associato a Ordine beni strumentali ", value= "annuale")

if (u'Preventivo dettaglio.registro',) not in s or s==[]:
    settinggg  = settingg.insert()
    settinggg.execute(key = "Preventivo dettaglio.registro", description = "Registro associato a Preventivo dettaglio", value= "registro_preventivo")

if (u'registro_preventivo_dettaglio.rotazione',) not in s or s==[]:
    settinggg  = settingg.insert()
    settinggg.execute(key = "registro_preventivo_dettaglio.rotazione", description = "Tipologia di rotazione registro associato a preventivo dettaglio ", value= "annuale")

std_mapper = mapper(Setting, settingg, order_by=settingg.c.key)
