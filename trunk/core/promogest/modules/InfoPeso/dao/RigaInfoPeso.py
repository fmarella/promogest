# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
from promogest.modules.InfoPeso.dao.TipoTrattamento import TipoTrattamento

try:
    rigainfopeso=Table('riga_info_peso',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    testatacommessaTable = Table('testata_info_peso', params['metadata'], autoload=True, schema=params['schema'])


    if params["tipo_db"] == "sqlite":
        testatainfopesoFK ='testata_info_peso.id'
        tipotrattamentoFK ='tipo_trattamento.id'

    else:
        testatainfopesoFK = params['schema']+'.testata_info_peso.id'
        tipotrattamentoFK = params['schema']+'.tipo_trattamento.id'

    rigainfopeso = Table('riga_info_peso', params["metadata"],
            Column('id', Integer, primary_key=True),
            Column('numero', Integer, nullable=True),
            Column('id_testata_info_peso', Integer,ForeignKey(testatainfopesoFK,onupdate="CASCADE",ondelete="CASCADE")),
            Column('id_tipo_trattamento', Integer,ForeignKey(tipotrattamentoFK,onupdate="CASCADE",ondelete="RESTRICT")),
            Column('data_registrazione', DateTime, nullable=True),
            Column('note',Text,nullable=True),
            Column('peso', Numeric(16,4), nullable=True),
            Column('massa_grassa', Numeric(16,4), nullable=True),
            Column('massa_magra_e_acqua', Numeric(16,4), nullable=True),
            Column('acqua', Numeric(16,4), nullable=True),
            schema=params["schema"],
            useexisting=True)
    rigainfopeso.create(checkfirst=True)


class RigaInfoPeso(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "id":
            dic= {k:rigainfopeso.c.id ==v}
        elif k == 'idTestataInfoPeso':
            dic = {k:rigainfopeso.c.id_testata_info_peso==v}
        return  dic[k]

    def _tipoTrattamento(self):
        a = TipoTrattamento().getRecord(id=self.id_tipo_trattamento)
        if a:
            return a.denominazione
        else:
            return "STANDARD"


    tipotrattamento = property(_tipoTrattamento)

std_mapper = mapper(RigaInfoPeso,rigainfopeso,
                properties={}, order_by=rigainfopeso.c.data_registrazione.desc())
