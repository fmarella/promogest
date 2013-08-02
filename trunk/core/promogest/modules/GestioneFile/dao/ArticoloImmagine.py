# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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
try:
    t_articolo_immagine=Table('articolo_immagine',
                params['metadata'],
                schema = params['schema'],
                autoload=True)
except:
    from data.articoloImmagine import t_articolo_immagine


from promogest.dao.Dao import Dao
from promogest.modules.GestioneFile.dao.Immagine import ImageFile, t_immagine
from promogest.dao.Articolo import Articolo, t_articolo





class ArticoloImmagine(Dao):
    """ ArticoloImmagine class database functions  """

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id_immagine':
            dic = {k:t_articolo_immagine.c.id_immagine == v}
        elif k == 'idArticolo':
            dic = {k:t_articolo_immagine.c.id_articolo == v}
        elif k == 'denominazione':
            dic = {k:and_(t_articolo_immagine.id_articolo==t_articolo.id,t_immagine.ilike("%"+v+"%"))}
        return  dic[k]

std_mapper = mapper(ArticoloImmagine, t_articolo_immagine, properties={
                 'immagine': relation(ImageFile, backref='artima',cascade="all, delete"),
                 'articolo': relation(Articolo, backref='artima'),
                }, order_by=t_articolo_immagine.c.id_immagine)
