#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005-2012 by Promotux Informatica - http://www.promotux.it/
#
# Authors: Francesco Meloni  <francesco@promotux.it>
#          Francesco Marella <francesco.marella@gmail.com>
#
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
from migrate import *

class PersonaGiuridica_(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idUser':
            dic = {k: t_persona_giuridica.c.id_user == v}
        return  dic[k]

t_persona_giuridica = Table('persona_giuridica',
                params['metadata'],
                schema=params['schema'],
                autoload=True)

if "note" not in [c.name for c in t_persona_giuridica.columns]:
    col = Column('note', String)
    col.create(t_persona_giuridica)

std_mapper = mapper(PersonaGiuridica_,
        t_persona_giuridica,
        order_by=t_persona_giuridica.c.id)

from promogest.dao.PersonaGiuridicaPersonaGiuridica import PersonaGiuridicaPersonaGiuridica
