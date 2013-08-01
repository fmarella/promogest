# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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
#from migrate.changeset.constraint import PrimaryKeyConstraint
from Dao import Dao


try:
    t_listino_complesso_articolo_prevalente=Table('listino_complesso_articolo_prevalente',
                                        params['metadata'],
                                        schema = params['schema'],
                                        autoload=True)
except:
    from data.listinoComplessoArticoloPrevalente import t_listino_complesso_articolo_prevalente

class ListinoComplessoArticoloPrevalente(Dao):
    """  """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idListinoComplesso':
            dic= {k : t_listino_complesso_articolo_prevalente.c.id_listino_complesso ==v}
        elif k == 'idListino':
            dic = {k:t_listino_complesso_articolo_prevalente.c.id_listino==v}
        elif k == 'idArticolo':
            dic = {k:t_listino_complesso_articolo_prevalente.c.id_articolo ==v}
        elif k == 'dataListinoArticolo':
            dic = {k:t_listino_complesso_articolo_prevalente.c.data_listino_articolo==v}
        return  dic[k]


std_mapper = mapper(ListinoComplessoArticoloPrevalente,
                    t_listino_complesso_articolo_prevalente,
                    properties={},
                    order_by=t_listino_complesso_articolo_prevalente.c.id_listino_complesso)

#for pk in t_listino_complesso_articolo_prevalente.primary_key:
    #if "id_listino_complesso" == pk.name and params["tipo_db"] != "sqlite":
        ##print "DEVO OPERARE", pk
        #cons = PrimaryKeyConstraint(t_listino_complesso_articolo_prevalente.c.id_listino_complesso)
        #cons.drop(cascade=True)
        #cons = PrimaryKeyConstraint(t_listino_complesso_articolo_prevalente.c.id)
        ##cons.drop(cascade=True)
        #cons.create()
