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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params
#from Listino import Listino
from migrate.changeset.constraint import PrimaryKeyConstraint
from Dao import Dao



sconto=Table('sconto', params['metadata'],schema = params['schema'],autoload=True)
listinoTable = Table('listino', params['metadata'], autoload=True, schema=params['schema'])
try:
    listinocomplessolistino=Table('listino_complesso_listino',params['metadata'],schema = params['schema'],autoload=True)
except:
    if params["tipo_db"] == "sqlite":
        listinoFK = 'listino.id'
    else:
        listinoFK = params['schema']+'.listino.id'
    listinocomplessolistino = Table('listino_complesso_listino',params['metadata'],
                Column('id_listino_complesso',Integer, primary_key=True),
                Column('id_listino', Integer,ForeignKey(listinoFK,onupdate="CASCADE",ondelete="CASCADE"), primary_key=True),
                schema=params['schema'])
    listinocomplessolistino.create(checkfirst=True)

class ListinoComplessoListino(Dao):
    """  """
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idListinoComplesso':
            dic= {k : listinocomplessolistino.c.id_listino_complesso ==v}
        elif k == 'idListino':
            dic = {k:listinocomplessolistino.c.id_listino==v}
        return  dic[k]

    def _listino(self):
        if self.listino: return self.listino.denominazione
        else: return ""
    listino_denominazione= property(_listino)


std_mapper = mapper(ListinoComplessoListino,listinocomplessolistino, properties={
                                            },
                    order_by=listinocomplessolistino.c.id_listino_complesso)

print "PK Listino complesso listino", len(listinocomplessolistino.primary_key)

if len(listinocomplessolistino.primary_key) ==1 and params["tipo_db"] != "sqlite":
    cons = PrimaryKeyConstraint(listinocomplessolistino.c.id_listino, listinocomplessolistino.c.id_listino_complesso)
    cons.drop(cascade=True)
    cons.create()

