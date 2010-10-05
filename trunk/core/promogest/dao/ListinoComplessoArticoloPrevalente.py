# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from sqlalchemy.orm import mapper, join,relation
from promogest.Environment import params
from Listino import Listino
from ListinoArticolo import ListinoArticolo
from Dao import Dao

class ListinoComplessoArticoloPrevalente(Dao):
    """  """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idListinoComplesso':
            dic= {k : listinocomplessoarticoloprevalente.c.id_listino_complesso ==v}
        elif k == 'idListino':
            dic = {k:listinocomplessoarticoloprevalente.c.id_listino==v}
        elif k == 'idArticolo':
            dic = {k:listinocomplessoarticoloprevalente.c.id_articolo ==v}
        elif k == 'dataListinoArticolo':
            dic = {k:listinocomplessoarticoloprevalente.c.data_listino_articolo==v}
        return  dic[k]


listinocomplessoarticoloprevalente=Table('listino_complesso_articolo_prevalente',
                                        params['metadata'],
                                        schema = params['schema'],
                                        autoload=True)

std_mapper = mapper(ListinoComplessoArticoloPrevalente,listinocomplessoarticoloprevalente, properties={
                                            },
                    order_by=listinocomplessoarticoloprevalente.c.id_listino_complesso)
