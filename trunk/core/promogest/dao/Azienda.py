# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

from sqlalchemy import Table
from sqlalchemy.orm import mapper, deferred
from promogest.Environment import params
from Dao import Dao


class Azienda(Dao):

    def __init__(self,campo=[], req=None):
        Dao.__init__(self,campo=campo, entity=self)

    def filter_values(self, k, v):
        if k == "schemaa":
            dic = { 'schemaa': azienda_table.c.schemaa==v}
        elif k == "denominazione":
            dic = { k: azienda_table.c.denominazione.ilike("%"+v+"%")}
        return dic[k]

azienda_table = Table('azienda',
                 params['metadata'],
                 autoload=True,
                 schema=params['mainSchema'])

std_mapper = mapper(Azienda, azienda_table,
properties={
    #'ragione_sociale':deferred(azienda_table.c.ragione_sociale),
    'sede_operativa_localita':deferred(azienda_table.c.sede_operativa_localita, group='ragione_sociale'),
    'sede_operativa_indirizzo':deferred(azienda_table.c.sede_operativa_indirizzo, group='ragione_sociale'),
    'sede_operativa_numero':deferred(azienda_table.c.sede_operativa_numero, group='ragione_sociale'),
    'sede_operativa_provincia':deferred(azienda_table.c.sede_operativa_provincia, group='ragione_sociale'),
    'sede_operativa_cap':deferred(azienda_table.c.sede_operativa_cap, group='ragione_sociale'),
    'sede_legale_localita':deferred(azienda_table.c.sede_legale_localita, group='ragione_sociale'),
    'sede_legale_indirizzo':deferred(azienda_table.c.sede_legale_indirizzo, group='ragione_sociale'),
    'sede_legale_numero':deferred(azienda_table.c.sede_legale_numero, group='ragione_sociale'),
    'sede_legale_provincia':deferred(azienda_table.c.sede_legale_provincia, group='ragione_sociale'),
    'sede_legale_cap':deferred(azienda_table.c.sede_legale_cap, group='ragione_sociale'),
    'partita_iva':deferred(azienda_table.c.partita_iva, group='ragione_sociale'),
    'codice_fiscale':deferred(azienda_table.c.codice_fiscale, group='ragione_sociale'),
    'iscrizione_cciaa_data':deferred(azienda_table.c.iscrizione_cciaa_data, group='ragione_sociale'),
    'iscrizione_cciaa_numero':deferred(azienda_table.c.iscrizione_cciaa_numero, group='ragione_sociale'),
    'iscrizione_tribunale_data':deferred(azienda_table.c.iscrizione_tribunale_data, group='ragione_sociale'),
    'iscrizione_tribunale_numero':deferred(azienda_table.c.iscrizione_tribunale_numero, group='ragione_sociale'),
    'codice_rea':deferred(azienda_table.c.codice_rea, group='ragione_sociale'),
    'matricola_inps':deferred(azienda_table.c.matricola_inps, group='ragione_sociale'),
    'numero_conto':deferred(azienda_table.c.numero_conto, group='ragione_sociale'),
    'iban':deferred(azienda_table.c.iban, group='ragione_sociale'),
    'cin':deferred(azienda_table.c.cin, group='ragione_sociale'),
    'abi':deferred(azienda_table.c.abi, group='ragione_sociale'),
    'cab':deferred(azienda_table.c.cab, group='ragione_sociale'),
    'percorso_immagine':deferred(azienda_table.c.percorso_immagine, group='ragione_sociale'),
},
order_by=azienda_table.c.schemaa)
