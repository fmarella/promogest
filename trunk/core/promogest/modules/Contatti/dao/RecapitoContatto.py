# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010,2011 by Promotux
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
from promogest.modules.Contatti.dao.TipoRecapito import TipoRecapito
from promogest.dao.Dao import Dao

class RecapitoContatto(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        if k =="id":
            dic= {k:recapito.c.id_contatto==v}
        elif k =="idContatto":
            dic = {k:recapito.c.id_contatto==v}
        elif k =="tipoRecapito":
            dic = {k:recapito.c.tipo_recapito==v}
        return  dic[k]

recapito=Table('recapito',
        params['metadata'],
        autoload=True,
        schema = params['schema'])

std_mapper = mapper(RecapitoContatto, recapito,properties={
    'tipo_reca':relation(TipoRecapito, backref='recapito')
    }, order_by=recapito.c.id)
