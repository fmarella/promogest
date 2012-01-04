# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>

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

class DivisoreNoleggio(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)


    def filter_values(self,k,v):
        if k =='idDivisoreNoleggio':
            dic= {k:divisorenoleggio.c.id_articolo ==v}
        elif k == "idValue":
            dic = {k:divisorenoleggio.c.value ==v}
        return  dic[k]

divisorenoleggio=Table('divisore_noleggio',params['metadata'],schema = params['schema'],autoload=True)

std_mapper = mapper(DivisoreNoleggio, divisorenoleggio, order_by=divisorenoleggio.c.value)
