# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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
from Dao import Dao

try:
    t_informazionifatturazionedocumento = Table('informazioni_fatturazione_documento',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    azTable = Table('testata_documento', params['metadata'], autoload=True, schema=params['schema'])
    if params["tipo_db"] == "sqlite":
        testata_documentoFK = 'testata_documento.id'
    else:
        testata_documentoFK =params['schema']+'.testata_documento.id'

    t_informazionifatturazionedocumento = Table('informazioni_fatturazione_documento', params['metadata'],
            Column('id_fattura',Integer,ForeignKey(testata_documentoFK),primary_key=True),
            Column('id_ddt',Integer,ForeignKey(testata_documentoFK,),primary_key=True,nullable=False),
            schema=params["schema"]
            )
    t_informazionifatturazionedocumento.create(checkfirst=True)

class InformazioniFatturazioneDocumento(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == "id_fattura":
            dic= {k:t_informazionifatturazionedocumento.c.id_fattura ==v}
        elif k == 'id_ddt':
            dic = {k:t_informazionifatturazionedocumento.c.id_ddt==v}
        return  dic[k]


std_mapper = mapper(InformazioniFatturazioneDocumento, t_informazionifatturazionedocumento,properties={
        }, order_by=t_informazionifatturazionedocumento.c.id_fattura)
