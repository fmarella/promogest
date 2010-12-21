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
from promogest.Environment import *
from Dao import Dao

class Operazione(Dao):

    def __init__(self, arg=None):
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
    ope.execute(denominazione = "Fattura pro-forma", fonte_valore = "vendita_senza_iva", tipo_persona_giuridica="cliente", tipo_operazione="documento")

if (u'Ordine a magazzino',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Ordine a magazzino", fonte_valore = "acquisto_senza_iva",
    tipo_persona_giuridica="fornitore",tipo_operazione="documento")

if (u'Ordine beni strumentali',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Ordine beni strumentali", fonte_valore = "acquisto_senza_iva",
    tipo_persona_giuridica="fornitore",tipo_operazione="documento")

if (u'Preventivo dettaglio',) not in s or s==[]:
    ope  = operazione.insert()
    ope.execute(denominazione = "Preventivo dettaglio", fonte_valore = "vendita_iva",
    tipo_persona_giuridica="cliente",tipo_operazione="documento")

#    setting.execute(key = "registro_fattura_proforma.rotazione", description = "Tipologia di rotazione registro associato a Fattura proforma ", value= "annuale")


std_mapper = mapper(Operazione, operazione, order_by=operazione.c.denominazione)
