# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao, Base


class TipoRecapito(Base, Dao):

    try:
        __table__ = Table('tipo_recapito',
                            params['metadata'],
                            schema = params['mainSchema'],
                            autoload=True,
                            autoload_with=engine)
    except:
        from data.tiporecapito import t_tipo_recapito
        __table__ = t_tipo_recapito

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= { 'denominazione' : TipoRecapito.__table__.c.denominazione.ilike("%"+v+"%") }
        return  dic[k]

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
