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
from core.Environment import *
from core.dao.Modulo import Modulo
from Dao import Dao

moduloTable = Table('modulo', params["metadata"], autoload=True, schema=params["schema"])

if tipo_db == "sqlite":
    moduloFK= 'modulo.id'
else:
    moduloFK = params["schema"]+'.modulo.id'

videomoduloTable = Table('video_modulo', params["metadata"],
        Column('id', Integer, primary_key=True),
        Column('testo_alternativo', String(150), nullable=False),
        Column('imagepath',String(700), nullable=False),
        Column('numero',  Integer, nullable=False),
        Column('id_modulo',Integer ,ForeignKey(moduloFK,onupdate="CASCADE",ondelete="CASCADE"),nullable=False),
        schema=params["schema"]
        )
videomoduloTable.create(checkfirst=True)


class VideoModulo(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k,v):
        dic= {
            'idModulo':videomodulo.c.id_modulo == v,
                }
        return  dic[k]

videomodulo=Table('video_modulo', params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(VideoModulo, videomodulo)
