# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012
#    by Promotux di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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
#from promogest.lib.migrate import *
from promogest.Environment import *

try:
    t_testata_documento_scadenza = Table('testata_documento_scadenza',
                  params['metadata'],
                  schema=params['schema'],
                  autoload=True)
except:
    from data.testataDocumentoScadenza import t_testata_documento_scadenza

from promogest.dao.Dao import Dao
from promogest.dao.DaoUtils import get_columns

class TestataDocumentoScadenza(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "idTestataDocumento":
            dic = {k: t_testata_documento_scadenza.c.id_testata_documento == v}
        elif k == "numeroScadenza":
            dic = {k: t_testata_documento_scadenza.c.numero_scadenza == v}
        return dic[k]

#colonne = get_columns(tesdocsca)

#if "id_banca" not in colonne:
    #col = Column('id_banca', Integer, nullable=True)
    ## ForeignKey(bancaFK, onupdate="CASCADE", ondelete="RESTRICT"),
    #col.create(tesdocsca)

#if "note_per_primanota" not in colonne:
    #col = Column('note_per_primanota', String(400), nullable=True)
    #col.create(tesdocsca)

std_mapper = mapper(TestataDocumentoScadenza,
                    t_testata_documento_scadenza,
                    properties={},
                    order_by=t_testata_documento_scadenza.c.id)
