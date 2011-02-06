# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
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
from promogest.dao.Dao import Dao
from migrate import *


try:
    rigacommessa=Table('riga_commessa',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    testatacommessaTable = Table('testata_commessa', params['metadata'], autoload=True, schema=params['schema'])


    if params["tipo_db"] == "sqlite":
        testatacommessaFK ='testata_commessa.id'

    else:
        testatacommessaFK = params['schema']+'.testata_commessa.id'

    rigacommessa = Table('riga_commessa', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('numero', Integer, nullable=False),
            Column('denominazione', String(300), nullable=False),
            Column('id_testata_commessa', Integer,ForeignKey(testatacommessaFK,onupdate="CASCADE",ondelete="CASCADE")),
#            Column('numero', Integer, nullable=False),
            Column('data_registrazione', DateTime, nullable=True),
            Column('dao_class', String(100), nullable=True),
            Column('note',Text,nullable=True),
            Column('id_dao', Integer, nullable=True),
            schema=params["schema"],
            useexisting=True)
    rigacommessa.create(checkfirst=True)


class RigaCommessa(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "id":
            dic= {k:rigacommessa.c.id ==v}
        elif k == 'idTestataCommessa':
            dic = {k:rigacommessa.c.id_testata_commessa==v}
#        elif k == 'numero':
#            dic = {k:rigacommessa.c.numero==v}
        elif k == 'daoClass':
            dic = {k:rigacommessa.c.dao_class==v}
        elif k == 'idDao':
            dic = {k:rigacommessa.c.id_dao==v}
        return  dic[k]


std_mapper = mapper(RigaCommessa,rigacommessa,
                properties={}, order_by=rigacommessa.c.id)
