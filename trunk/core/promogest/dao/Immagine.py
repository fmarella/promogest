# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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
from promogest.dao.Dao import Dao


try:
    immagine =Table('immagine',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
except:
    try:
        immagine = Table('immagine', params['metadata'],
            Column('id', Integer, primary_key=True),
            Column('denominazione', String(200), nullable=False ),
            Column('altezza', Numeric(16,4), nullable=True),
            Column('larghezza', Numeric(16,4), nullable=True),
            Column('fingerprint', String(200), nullable=False ),
            Column('data', LargeBinary),
            schema=params['schema'],
            )
    except:
        immagine = Table('immagine', params['metadata'],
            Column('id', Integer, primary_key=True),
            Column('denominazione', String(200), nullable=False ),
            Column('altezza', Numeric(16,4), nullable=True),
            Column('larghezza', Numeric(16,4), nullable=True),
            Column('fingerprint', String(200), nullable=False ),
            Column('data', Binary),
            schema=params['schema'],
            )
immagine.create(checkfirst=True)


class ImageFile(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= { 'denominazione' : immagine.c.denominazione == v }
        return  dic[k]


std_mapper = mapper(ImageFile, immagine, order_by = immagine.c.id)
