# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
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
from sqlalchemy.orm import mapper, join
import promogest.dao.Dao
from promogest.dao.Dao import Dao
from promogest.Environment import *
from promogest.dao.Promemoria import Promemoria
#from promogest.modules.SchedaLavorazione.dao.SchedaOrdinazione import SchedaOrdinazione

class PromemoriaSchedaOrdinazione(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=="id" or k=="idPromemoria":
            dic= {k : promemoriaschedaordinazione.c.id ==v}
        elif k=="idScheda":
            dic={k:promemoriaschedaordinazione.c.id_scheda ==v}
        return  dic[k]

promemoriaschedaordinazione=Table('promemoria_schede_ordinazioni',
                                    params['metadata'],
                                    schema = params['schema'],
                                    autoload=True)

promemoria=Table('promemoria', params['metadata'], schema = params['schema'], autoload=True)

j = join(promemoriaschedaordinazione, promemoria)

std_mapper = mapper(PromemoriaSchedaOrdinazione, j, properties={
            'id':[promemoria.c.id, promemoriaschedaordinazione.c.id],
                    },
                                order_by=promemoriaschedaordinazione.c.id)
