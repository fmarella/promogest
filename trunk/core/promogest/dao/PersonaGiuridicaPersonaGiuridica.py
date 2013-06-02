# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    This file is part of Promogest. http://www.promogest.me

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
from promogest.Environment import params
#from Listino import Listino
from migrate.changeset.constraint import PrimaryKeyConstraint
from Dao import Dao


pg=Table('persona_giuridica', params['metadata'],schema = params['schema'],autoload=True)

try:
    personagiuridica_personagiuridica=Table('personagiuridica_personagiuridica',
        params['metadata'],
        schema = params['schema'],
        autoload=True)
except:
    if params["tipo_db"] == "sqlite":
        pgFK = 'persona_giuridica.id'
    else:
        pgFK = params['schema']+'.persona_giuridica.id'

    personagiuridica_personagiuridica = Table('personagiuridica_personagiuridica',
        params['metadata'],
        Column('id_persona_giuridica', Integer,
                ForeignKey(pgFK, onupdate="CASCADE", ondelete="CASCADE"),
                primary_key=True),
        Column('id_persona_giuridica_abbinata', Integer,
                ForeignKey(pgFK, onupdate="CASCADE", ondelete="CASCADE"),
                primary_key=True,
                nullable=False),
        Column('note', Text, nullable=True),
        schema=params['schema'])
    personagiuridica_personagiuridica.create(checkfirst=True)

class PersonaGiuridicaPersonaGiuridica(Dao):
    """  """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idPersonaGiuridica':
            dic= {k : personagiuridica_personagiuridica.c.id_persona_giuridica == v}
        elif k == 'idPersonaGiuridicaAbbinata':
            dic = {k:personagiuridica_personagiuridica.c.id_persona_giuridica_abbinata == v}
        return  dic[k]


std_mapper = mapper(PersonaGiuridicaPersonaGiuridica,
    personagiuridica_personagiuridica, properties={},
    order_by=personagiuridica_personagiuridica.c.id_persona_giuridica_abbinata)
