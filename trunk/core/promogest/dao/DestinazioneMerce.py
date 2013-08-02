# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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
from promogest.lib.migrate import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

try:
    t_destinazione_merce=Table('destinazione_merce',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    from data.destinazioneMerce import t_destinazione_merce

class DestinazioneMerce(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=='idCliente':
            dic= {k:t_destinazione_merce.c.id_cliente==v}
        elif k == 'denominazione':
            dic ={k:t_destinazione_merce.c.denominazione.ilike("%"+v+"%")}
        elif k== 'indirizzo':
            dic = {k:t_destinazione_merce.c.indirizzo.ilike("%"+v+"%")}
        elif k=='localita':
            dic = {k:t_destinazione_merce.c.localita.ilike("%"+v+"%")}
        elif k == 'provincia':
            dic = {k:t_destinazione_merce.c.provincia.ilike("%"+v+"%")}
        return  dic[k]

#if 'codice' not in [c.name for c in t_destinazione_merce.columns]:
    #col = Column('codice', String(30))
    #col.create(t_destinazione_merce, populate_default=True)

std_mapper = mapper(DestinazioneMerce,t_destinazione_merce, order_by=t_destinazione_merce.c.id)
