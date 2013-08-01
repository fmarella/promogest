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

t_setting = Table('setting', params["metadata"],
        Column('key',String(100),primary_key=True, nullable=False),
        Column('description',String(300),nullable=False),
        Column('value',String(100),nullable=False),
        schema=params["schema"]
        )
t_setting.create(checkfirst=True)


s= select([t_setting.c.key]).execute().fetchall()
if (u'Fattura differita vendita.registro',) not in s or s ==[]:
    tipo = t_setting.insert()
    tipo.execute(key='Movimento.registro', value='registro_movimenti',description='Registro associato ai movimenti' )
    tipo.execute(key='registro_movimenti.rotazione', value='annuale',description='Tipologia di rotazione del registro_movimenti' )
    tipo.execute(key='Fattura vendita.registro', value='registro_fattura_vendita',description='Registro associato alle fatture vendita' )
    tipo.execute(key='registro_fattura_vendita.rotazione', value='annuale',description='Tipologia di rotazione del registro_fattura_vendita' )
    tipo.execute(key='Fattura acquisto.registro', value='registro_fattura_acquisto',description='Registro associato alle fatture acquisto' )
    tipo.execute(key='registro_fattura_acquisto.rotazione', value='annuale',description='Tipologia di rotazione del registro_fattura_acquisto' )
    tipo.execute(key='DDT vendita.registro', value='registro_ddt_vendita',description='Registro associato ai DDT vendita' )
    tipo.execute(key='registro_ddt_vendita.rotazione', value='annuale',description='Tipologia di rotazione del registro_ddt_vendita' )
    tipo.execute(key='DDT acquisto.registro', value='registro_ddt_acquisto',description='Registro associato ai DDT acquisto' )
    tipo.execute(key='registro_ddt_acquisto.rotazione', value='annuale',description='Tipologia di rotazione del registro_ddt_acquisto' )
    tipo.execute(key='DDT reso a fornitore.registro', value='registro_ddt_reso_a_fornitore',description='Registro associato a DDT reso a  fornitore' )
    tipo.execute(key='registro_ddt_reso_a_fornitore.rotazione', value='annuale',description='Tipologia di rotazione del registro_ddt_reso_a_fornitore' )
    tipo.execute(key='DDT reso da cliente.registro', value='registro_ddt_reso_da_cliente',description='Registro associato a DDT reso da cliente' )
    tipo.execute(key='registro_ddt_reso_da_cliente.rotazione', value='annuale',description='Tipologia di rotazione di DDT reso da cliente' )
    tipo.execute(key='Nota di credito a cliente.registro', value='registro_nota_credito_a_cliente',description='Registro associato a Nota di credito cliente' )
    tipo.execute(key='registro_nota_credito_a_cliente.rotazione', value='annuale',description='Tipologia di rotazione del registro nota di credito a cliente' )
    tipo.execute(key='Nota di credito da fornitore.registro', value='registro_nota_credito_da_fornitore ',description='Registro associato alle note di credito da fornitore' )
    tipo.execute(key='registro_nota_credito_da_fornitore.rotazione', value='annuale',description='Tipologia di rotazione di nota di credito da fornitore' )
    tipo.execute(key='Fattura accompagnatoria.registro', value='registro_fattura_accompagnatoria',description='Registro associato alle fatture accompagnatorie' )
    tipo.execute(key='registro_fattura_accompagnatoria.rotazione', value='annuale',description='Tipologia di rotazione del registro fattura accompagnatoria' )
    tipo.execute(key='Preventivo.registro', value='registro_preventivo',description='Registro associato ai preventivi' )
    tipo.execute(key='registro_preventivo.rotazione', value='annuale',description='Tipologia di rotazione del registro preventivo' )
    tipo.execute(key='Ordine da cliente.registro', value='registro_ordine_da_cliente',description='Registro associato a ordine da cliente' )
    tipo.execute(key='registro_ordine_da_cliente.rotazione', value='annuale',description='Tipologia di rotazione del registro ordine da cliente' )
    tipo.execute(key='Ordine a fornitore.registro', value='registro_ordine_a_fornitore',description='Registro associato agli ordini a fornitore' )
    tipo.execute(key='registro_ordine_a_fornitore.rotazione', value='annuale',description='Tipologia di rotazione del registro agli ordini a fornitore' )
    tipo.execute(key='Vendita dettaglio.registro', value='registro_vendita_dettaglio',description='Registro associato a vendita al dettaglio' )
    tipo.execute(key='registro_vendita_dettaglio.rotazione', value='annuale',description='Tipologia di rotazione del registro vendita al dettaglio' )
    tipo.execute(key='Fattura differita vendita.registro', value='registro_fattura_differita_vendita',description='Registro associato a fattura differita vendita' )
    tipo.execute(key='registro_fattura_differita_vendita.rotazione', value='annuale',description='Tipologia di rotazione del registro fattura differita vendita' )
    tipo.execute(key='Fattura differita acquisto.registro', value='registro_vendita_dettaglio',description='Registro associato a fattura differita acquisto' )
    tipo.execute(key='registro_fattura_differita_acquisto.rotazione', value='annuale',description='Tipologia di rotazione del registro fattura differita acquisto' )
    tipo.execute(key='update_db_version', value='0.9.10',description='versione aggiornamento database' )


if (u'Fattura pro-forma.registro',) not in s or s==[]:
    t_settingg  = t_setting.insert()
    t_settingg.execute(key = "Fattura pro-forma.registro", description = "Registro associato a Fattura pro-forma", value= "registro_fattura_pro-forma")
    t_settingg.execute(key = "registro_fattura_pro-forma.rotazione", description = "Tipologia di rotazione registro associato a Fattura pro-forma ", value= "annuale")
if (u'Ordine a magazzino.registro',) not in s or s==[]:
    t_settingg  = t_setting.insert()
    t_settingg.execute(key = "Ordine a magazzino.registro", description = "Registro associato a Ordine a magazzino", value= "registro_ordine_a_magazzino")
    t_settingg.execute(key = "registro_ordine_a_magazzino.rotazione", description = "Tipologia di rotazione registro associato a Ordine a magazzino ", value= "annuale")
if (u'Carico da composizione kit.registro',) not in s or s==[]:
    t_settingg  = t_setting.insert()
    t_settingg.execute(key = "Carico da composizione kit.registro", description = "Registro associato a Carico da composizione kit", value= "registro_carico_da_composizione_kit")
    t_settingg.execute(key = "carico_da_composizione_kit.rotazione", description = "Tipologia di rotazione registro associato a Carico da composizione kit", value= "annuale")
if (u'Scarico Scomposizione kit.registro',) not in s or s==[]:
    t_settingg  = t_setting.insert()
    t_settingg.execute(key = "Scarico Scomposizione kit.registro", description = "Registro associato a Scarico Scomposizione kit", value= "registro_scarico_scomposizione_kit")
    t_settingg.execute(key = "scarico_scomposizione_kit.rotazione", description = "Tipologia di rotazione registro associato a Scarico Scomposizione kit", value= "annuale")

if (u'Trasferimento merce magazzino.registro',) not in s or s==[]:
    t_settingg  = t_setting.insert()
    t_settingg.execute(key = "Trasferimento merce magazzino.registro", description = "Registro associato a Trasferimento merce magazzino", value= "trasferimento_merce_magazzino")
    t_settingg.execute(key = "trasferimento_merce_magazzino.rotazione", description = "Tipologia di rotazione registro associato a Trasferimento merce magazzino", value= "annuale")


if (u'Ordine beni strumentali.registro',) not in s or s==[]:
    t_settingg  = t_setting.insert()
    t_settingg.execute(key = "Ordine beni strumentali.registro", description = "Registro associato a Ordine beni strumentali", value= "registro_ordine_beni_strumentali")
    t_settingg.execute(key = "registro_ordine_beni_strumentali.rotazione", description = "Tipologia di rotazione registro associato a Ordine beni strumentali ", value= "annuale")

if (u'Preventivo dettaglio.registro',) not in s or s==[]:
    t_settingg  = t_setting.insert()
    t_settingg.execute(key = "Preventivo dettaglio.registro", description = "Registro associato a Preventivo dettaglio", value= "registro_preventivo")

if (u'registro_preventivo_dettaglio.rotazione',) not in s or s==[]:
    t_settingg  = t_setting.insert()
    t_settingg.execute(key = "registro_preventivo_dettaglio.rotazione", description = "Tipologia di rotazione registro associato a preventivo dettaglio ", value= "annuale")
