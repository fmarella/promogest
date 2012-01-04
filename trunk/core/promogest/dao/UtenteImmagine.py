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

immagineTable = Table('immagine', params['metadata'], autoload=True, schema=params['schema'])
utenteTable = Table('utente', params['metadata'], autoload=True, schema=params['mainSchema'])

try:
    utenteimmagine=Table('utente_immagine',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    if params["tipo_db"] == "sqlite":
        immagineFK = 'immagine.id'
        utenteFK = 'utente.id'
    else:
        immagineFK = params['schema']+'.immagine.id'
        utenteFK = params['mainSchema']+'.utente.id'

    utenteimmagine = Table('utente_immagine', params['metadata'],
            Column('id_immagine',Integer,ForeignKey(immagineFK,onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
            Column('id_utente',Integer,primary_key=True),
            schema=params['schema'])
    utenteimmagine.create(checkfirst=True)

class UtenteImmagine(Dao):
    """ RoleAction class database functions  """

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_immagine':
            dic = {k:utenteimmagine.c.id_immagine == v}
        elif k == 'idUtente':
            dic = {k:utenteimmagine.c.id_utente == v}
        return  dic[k]

std_mapper = mapper(UtenteImmagine, utenteimmagine, properties={
                }, order_by=utenteimmagine.c.id_immagine)
