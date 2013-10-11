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


t_operazione = Table('operazione', params["metadata"],
        Column('denominazione', String(100), primary_key=True),
        Column('segno', String(3), nullable=True),
        Column('fonte_valore', String(50), nullable=True),
        Column('tipo_persona_giuridica', String(50), nullable=True),
        Column('tipo_operazione', String(50), nullable=True),
        schema=params["mainSchema"]
        )
t_operazione.create(checkfirst=True)


s = select([t_operazione.c.denominazione]).execute().fetchall()
if (u'Fattura vendita',) not in s or s == []:
    tipo = t_operazione.insert()
    tipo.execute(denominazione='Fattura vendita', segno='-', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )
    tipo.execute(denominazione='Fattura acquisto', segno='+', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore' )
    tipo.execute(denominazione='DDT vendita', segno='-', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )
    tipo.execute(denominazione='DDT acquisto', segno='+', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore' )
    tipo.execute(denominazione='DDT reso a fornitore', segno='-', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore' )
    tipo.execute(denominazione='DDT reso da cliente', segno='+', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )
    tipo.execute(denominazione='Nota di credito a cliente', segno='+', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )
    tipo.execute(denominazione='Nota di credito da fornitore', segno='-', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore')
    tipo.execute(denominazione='Scarico per uso interno', segno='-', fonte_valore='acquisto_senza_iva', tipo_operazione="movimento")
    tipo.execute(denominazione='Scarico per deterioramento o rottura', segno='-', fonte_valore='acquisto_senza_iva', tipo_operazione="movimento" )
    tipo.execute(denominazione='Scarico per omaggio', segno='-', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="movimento")
    tipo.execute(denominazione='Carico per inventario', segno='+', fonte_valore='acquisto_senza_iva', tipo_operazione="movimento" )
    tipo.execute(denominazione='Scarico venduto da cassa', segno='-', fonte_valore='vendita_iva', tipo_operazione="movimento" )
    tipo.execute(denominazione='Fattura accompagnatoria', segno='-', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="documento" )
    tipo.execute(denominazione='Preventivo', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="documento" )
    tipo.execute(denominazione='Ordine da cliente', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="documento" )
    tipo.execute(denominazione='Ordine a fornitore', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore', tipo_operazione="documento" )
    tipo.execute(denominazione='Vendita dettaglio', segno='-', fonte_valore='vendita_iva', tipo_persona_giuridica='cliente')
    tipo.execute(denominazione='Fattura differita vendita', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente', tipo_operazione="documento" )
    tipo.execute(denominazione='Fattura differita acquisto', fonte_valore='acquisto_senza_iva', tipo_persona_giuridica='fornitore', tipo_operazione="documento" )

    tipo.execute(denominazione = "Fattura pro-forma", fonte_valore = "vendita_senza_iva", tipo_persona_giuridica="cliente", tipo_operazione="documento")
    tipo.execute(denominazione = "Ordine a magazzino", fonte_valore = "acquisto_senza_iva", tipo_persona_giuridica="fornitore",tipo_operazione="documento")
    tipo.execute(denominazione = "Carico da composizione kit", fonte_valore = "acquisto_senza_iva", tipo_operazione="movimento", segno="+")
    tipo.execute(denominazione = "Scarico Scomposizione kit", fonte_valore = "vendita_senza_iva", tipo_operazione="movimento", segno="-")
    tipo.execute(denominazione = "Trasferimento merce magazzino", fonte_valore = "acquisto_senza_iva", tipo_operazione="movimento",tipo_persona_giuridica="magazzino", segno="=")
    tipo.execute(denominazione = "Ordine beni strumentali", fonte_valore = "acquisto_senza_iva", tipo_persona_giuridica="fornitore",tipo_operazione="documento")
    tipo.execute(denominazione = "Preventivo dettaglio", fonte_valore = "vendita_iva", tipo_persona_giuridica="cliente",tipo_operazione="documento")
    tipo.execute(denominazione='Buono visione merce', segno='-', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )
