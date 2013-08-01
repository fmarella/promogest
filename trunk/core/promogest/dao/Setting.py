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
from promogest.Environment import params
from promogest.dao.Dao import Dao


try:
    t_setting=Table('setting',params['metadata'],schema = params['schema'],autoload=True)
except:
    from data.setting import t_setting


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
            dic= {  k : t_setting.c.key.ilike("%"+v+"%")}
        elif k == 'description':
            dic = {k:t_setting.c.description.ilike("%"+v+"%")}
        elif k == 'value':
            dic = {k:t_setting.c.value == v}
        return  dic[k]

def addregistriDiretti():
    s= select([t_setting.c.key]).execute().fetchall()
    if (u'registro_ordine_da_cliente_diretto.rotazione',) not in s or s==[]:
        t_settingg  = t_setting.insert()
        t_settingg.execute(key = "Ordine da cliente diretto.registro", description = "ordine da cliente diretto", value= "registro_ordine_da_cliente_diretto")
        t_settingg.execute(key = "registro_ordine_da_cliente_diretto.rotazione", description = "registro_ordine_da_cliente_diretto.rotazione ", value= "annuale")
    if (u'registro_ddt_vendita_diretto.rotazione',) not in s or s==[]:
        t_settingg  = t_setting.insert()
        t_settingg.execute(key = "DDT vendita diretto.registro", description = "DDT vendita diretto", value= "registro_ddt_vendita_diretto")
        t_settingg.execute(key = "registro_ddt_vendita_diretto.rotazione", description = "registro_ddt_vendita_diretto.rotazione ", value= "annuale")
    if (u'registro_fattura_vendita_diretta.rotazione',) not in s or s==[]:
        t_settingg  = t_setting.insert()
        t_settingg.execute(key = "Fattura vendita diretta.registro", description = "Fattura vendita diretta", value= "registro_fattura_vendita_diretta")
        t_settingg.execute(key = "registro_fattura_vendita_diretta.rotazione", description = "registro_fattura_vendita_diretta.rotazione ", value= "annuale")


std_mapper = mapper(Setting, t_setting, order_by=t_setting.c.key)
