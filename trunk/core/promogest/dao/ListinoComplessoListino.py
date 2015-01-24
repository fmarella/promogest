# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    This file is part of Promogest. http://www.promogest.me

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


class ListinoComplessoListino(Base, Dao):
    """  """
    try:
        __table__ = Table('listino_complesso_listino',params['metadata'],schema = params['schema'],autoload=True)
    except:
        from data.listinoComplessoListino import t_listino_complesso_listino
        __table__ = t_listino_complesso_listino

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idListinoComplesso':
            dic= {k : ListinoComplessoListino.__table__.c.id_listino_complesso ==v}
        elif k == 'idListino':
            dic = {k:ListinoComplessoListino.__table__.c.id_listino==v}
        return  dic[k]

    @property
    def listino_denominazione(self):
        if self.listino: return self.listino.denominazione
        else: return ""
