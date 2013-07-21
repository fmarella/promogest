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

class SettingDb(object):

    def __init__(self, schema = None,mainSchema=None, metadata=None, session=None,debug=False):
        self.metadata = metadata
        self.session_sl = session
        self.schema = schema
        self.mainSchema=mainSchema
        self.debug = debug

    def create(self):
        settingTable = Table('setting', self.metadata,
                Column('key',String(100),primary_key=True, nullable=False),
                Column('description',String(300),nullable=False),
                Column('value',String(100),nullable=False),
                schema=self.schema
                )
        settingTable.create(checkfirst=True)
        s= select([settingTable.c.key]).execute().fetchall()
        if (u'Fattura differita vendita.registro',) not in s or s ==[]:
            tipo = settingTable.insert()
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

    def update(self, req=None, arg=None):
        pass

    def alter(self, req=None, arg=None):
        pass

    def data(self, req=None, arg=None):
        pass
