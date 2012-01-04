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
from promogest.dao.Articolo import Articolo

class AssociazioneArticoli(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)


    def filter_values(self,k,v):
        if k == "id":
            dic= {k:associazionearticolo.c.id ==v}
        elif k=="nodo":
            dic= {k:None}
            #dic= {k:associazionearticolo.c.nodo ==v}
        return  dic[k]

associazionearticolo=Table('associazione_articolo', params['metadata'],
                                                    schema = params['schema'],
                                                    autoload=True)

articolo = Table('articolo', params['metadata'],schema = params['schema'],autoload=True)

#j = join(associazionearticolo, articolo)

std_mapper = mapper(AssociazioneArticoli, associazionearticolo, properties={
                "arto_padre":relation(Articolo,primaryjoin=
                    associazionearticolo.c.id_padre==Articolo.id, backref="asso_art_padre"),
                "arto_figlio":relation(Articolo,primaryjoin=
                    associazionearticolo.c.id_figlio==Articolo.id, backref="asso_art_figlio")},
                                            order_by=associazionearticolo.c.posizione)

