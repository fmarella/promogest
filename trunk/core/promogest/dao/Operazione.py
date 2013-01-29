# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

#    This file is part of Promogest. ( http://www.promogest.me )

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

class Operazione(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= { k: operazione.c.denominazione.ilike("%"+v+"%")}
        elif k== 'denominazioneEM':
            dic= { k: operazione.c.denominazione == (v).strip()}
        elif k=="tipoOperazione":
            dic = {k:operazione.c.tipo_operazione==v}
        elif k=="segno":
            dic = {k: operazione.c.segno ==v}
        elif k=="tipoPersonaGiuridica":
            dic = {k: operazione.c.tipo_persona_giuridica ==v}
        return  dic[k]

operazione=Table('operazione',params['metadata'],schema = params['mainSchema'],autoload=True)

s= select([operazione.c.denominazione]).execute().fetchall()
if (u'Fattura pro-forma',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Fattura pro-forma", fonte_valore = "vendita_senza_iva",
    tipo_persona_giuridica="cliente", tipo_operazione="documento")

if (u'Ordine a magazzino',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Ordine a magazzino", fonte_valore = "acquisto_senza_iva",
    tipo_persona_giuridica="fornitore",tipo_operazione="documento")

if (u'Carico da composizione kit',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Carico da composizione kit", fonte_valore = "acquisto_senza_iva",
    tipo_operazione="movimento", segno="+")

if (u'Scarico Scomposizione kit',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Scarico Scomposizione kit", fonte_valore = "vendita_senza_iva",
    tipo_operazione="movimento", segno="-")

if (u'Trasferimento merce magazzino',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Trasferimento merce magazzino", fonte_valore = "acquisto_senza_iva",
    tipo_operazione="movimento",tipo_persona_giuridica="magazzino", segno="=")

if (u'Ordine beni strumentali',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Ordine beni strumentali", fonte_valore = "acquisto_senza_iva",
    tipo_persona_giuridica="fornitore",tipo_operazione="documento")

if (u'Preventivo dettaglio',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Preventivo dettaglio", fonte_valore = "vendita_iva",
    tipo_persona_giuridica="cliente",tipo_operazione="documento")

if (u'Buono visione merce',) not in s or s==[]:
    ope = operazione.insert()
    ope.execute(denominazione='Buono visione merce', segno='-', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente' )

#    setting.execute(key = "registro_fattura_proforma.rotazione", description = "Tipologia di rotazione registro associato a Fattura proforma ", value= "annuale")
def addOpDirette():
    if (u'Ordine da cliente diretto',) not in s or s==[]:
        ope = operazione.insert()
        ope.execute(denominazione='Ordine da cliente diretto', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente',tipo_operazione="documento" )
    if (u'DDT vendita diretto',) not in s or s==[]:
        ope = operazione.insert()
        ope.execute(denominazione='DDT vendita diretto', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='fornitore',tipo_operazione="documento" )
    if (u'Fattura vendita diretta',) not in s or s==[]:
        ope = operazione.insert()
        ope.execute(denominazione='Fattura vendita diretta', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente',tipo_operazione="documento" )


std_mapper = mapper(Operazione, operazione, order_by=operazione.c.denominazione)
