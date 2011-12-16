# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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


try:
    variazionelistino=Table('variazione_listino',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
except:
        listinoTable = Table('listino', params["metadata"], autoload=True, schema=params["schema"])

        if params["schema"]:
            listinoFK = params["schema"]+'.listino.id'
        else:
            listinoFK = 'listino.id'

        variazionelistino = Table('variazione_listino', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('denominazione', String(200), nullable=False),
            Column('data_inizio', DateTime, nullable=True),
            Column('data_fine', DateTime, nullable=True),
            Column('id_listino', Integer,ForeignKey(listinoFK,onupdate="CASCADE",ondelete="CASCADE")),
            Column('valore', String(50), nullable=True),
            Column('tipo', String(50), nullable=True),
            Column('segno', String(1), nullable=True),
            Column('priorita', Boolean, nullable=False),
            schema=params["schema"],
            useexisting=True)
        variazionelistino.create(checkfirst=True)

class VariazioneListino(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= {k:variazionelistino.c.denominazione.ilike("%"+v+"%")}
        elif k == 'daDataInizio':
            dic = {k:variazionelistino.c.data_inizio >= v}
        elif k== 'aDataInizio':
            dic = {k:variazionelistino.c.data_inizio <= v}
        elif k == 'daDataFine':
            dic = {k:variazionelistino.c.data_fine >= v}
        elif k== 'aDataFine':
            dic = {k:variazionelistino.c.data_fine <= v}
        elif k== 'idListino':
            dic = {k:variazionelistino.c.id_listino == v}
        elif k== 'priorita':
            dic = {k:variazionelistino.c.priorita == v}
        elif k== 'tipo':
            dic = {k:variazionelistino.c.tipo == v}
        return  dic[k]

std_mapper = mapper(VariazioneListino, variazionelistino, order_by=variazionelistino.c.id)