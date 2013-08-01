# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

try:
    t_operazione=Table('operazione',params['metadata'],schema = params['mainSchema'],autoload=True)
except:
    from data.operazione import t_operazione


class Operazione(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= { k: t_operazione.c.denominazione.ilike("%"+v+"%")}
        elif k== 'denominazioneEM':
            dic= { k: t_operazione.c.denominazione == (v).strip()}
        elif k=="tipoOperazione":
            dic = {k:t_operazione.c.tipo_operazione==v}
        elif k=="segno":
            dic = {k: t_operazione.c.segno ==v}
        elif k=="tipoPersonaGiuridica":
            dic = {k: t_operazione.c.tipo_persona_giuridica ==v}
        return  dic[k]

def addOpDirette():
    s= select([t_operazione.c.denominazione]).execute().fetchall()
    if (u'Ordine da cliente diretto',) not in s or s==[]:
        ope = operazione.insert()
        ope.execute(denominazione='Ordine da cliente diretto', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente',tipo_operazione="documento" )
    if (u'DDT vendita diretto',) not in s or s==[]:
        ope = operazione.insert()
        ope.execute(denominazione='DDT vendita diretto', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='fornitore',tipo_operazione="documento" )
    if (u'Fattura vendita diretta',) not in s or s==[]:
        ope = operazione.insert()
        ope.execute(denominazione='Fattura vendita diretta', fonte_valore='vendita_senza_iva', tipo_persona_giuridica='cliente',tipo_operazione="documento" )


std_mapper = mapper(Operazione, t_operazione, order_by=t_operazione.c.denominazione)

#from promogest.dao.CachedDaosDict import cache_objj
#cache_objj.add(Operazione, use_key='denominazione')
#cache_obj = cache_objj
