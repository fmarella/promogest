# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012,2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/
#    Copyright (C) 2013 Francesco Marella <francesco.marella@anche.no>

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
from promogest.Environment import *
from promogest.dao.Dao import Dao

try:
    t_tipo_recapito = Table('tipo_recapito',
                        params['metadata'],
                        schema = params['mainSchema'],
                        autoload=True)
except:
    from data.tiporecapito import t_tipo_recapito


class TipoRecapito(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= { 'denominazione' : T_tipo_recapito.c.denominazione.ilike("%"+v+"%") }
        return  dic[k]


std_mapper = mapper(TipoRecapito, t_tipo_recapito, order_by=t_tipo_recapito.c.denominazione)

recapiti = TipoRecapito().select()
t = False
for recapito in recapiti:
    if recapito.denominazione == 'Email PEC':
        t = True
        break
if not t:
    tr = TipoRecapito()
    tr.denominazione = "Email PEC"
    tr.persist()
