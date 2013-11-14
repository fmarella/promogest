# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 2011by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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
from promogest.dao.Dao import Dao

t_regione=Table('regione', params['metadata'],schema = params['mainSchema'],autoload=True)



class Regioni(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione':t_regione.c.denominazione == v,
                }
        return  dic[k]

std_mapper = mapper(Regioni, t_regione,order_by=t_regione.c.denominazione)


#f = Regioni().select(denominazione="Piemonte")
#if not f:
    #for p in regis:
        #a = Regioni()
        #a.codice=p[0]
        #a.denominazione = p[1]
        #session.add(a)
    #session.commit()
