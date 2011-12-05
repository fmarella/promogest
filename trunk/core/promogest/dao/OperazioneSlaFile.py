# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
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
from core.Environment import *
from core.dao.Dao import Dao

operazioneTable = Table('operazione', params['metadata'], autoload=True, schema=params['mainSchema'])
slafileTable = Table('sla_file', params['metadata'], autoload=True, schema=params['schema'])

try:
    operazioneslafile=Table('operazione_slafile',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    if tipo_db == "sqlite":
        operazioneFK = 'operazione.denominazione'
        slafileFK = 'sla_file.id'
    else:
        operazioneFK = params['mainSchema']+'.denominazione'
        slafileFK = params['schema']+'.sla_file.id'

    operazioneslafile = Table('operazione_slafile', params['metadata'],
            Column('denominazione_operazione',String(200),ForeignKey(operazioneFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_slafile',Integer,ForeignKey(slafileFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            schema=params['schema'])
    operazioneslafile.create(checkfirst=True)

class OperazioneSlaFile(Dao):
    """ RoleAction class database functions  """

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione_operazione':
            dic = {k:operazioneslafile.c.denominazione_operazione == v}
        elif k == 'id_slafile':
            dic = {k:operazioneslafile.c.id_slafile == v}
        return  dic[k]

std_mapper = mapper(OperazioneSlaFile, operazioneslafile, properties={
                }, order_by=operazioneslafile.c.denominazione_operazione)
