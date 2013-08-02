# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>

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
from promogest.dao.Articolo import Articolo, t_articolo
from promogest.dao.PersonaGiuridica import PersonaGiuridica_, t_persona_giuridica
from promogest.modules.Provvigione.dao.Provvigione import Provvigione, t_provvigione
from promogest.lib.migrate import *


try:
    t_provv_pg_az_art = Table('provv_pg_az_art', params['metadata'],
                         schema=params['schema'], autoload=True)
except:

    t_provv_pg_az_art = Table(
        'provv_pg_az_art',
        params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('id_articolo', Integer,
                ForeignKey(fk_prefix + 'articolo.id',
                    onupdate='CASCADE', ondelete='CASCADE')),
        Column('id_persona_giuridica_from', Integer,
                ForeignKey(fk_prefix + 'persona_giuridica.id',
                    onupdate='CASCADE', ondelete='CASCADE')),
        Column('id_persona_giuridica_to', Integer,
                ForeignKey(fk_prefix + 'persona_giuridica.id',
                    onupdate='CASCADE', ondelete='CASCADE')),
        Column('schemaa_azienda', String(100),
                ForeignKey(fk_prefix_main +'azienda.schemaa',
                    onupdate='CASCADE', ondelete='CASCADE')),
        Column('id_provvigione', Integer,
                ForeignKey(fk_prefix + 'provvigione.id',
                    onupdate='CASCADE', ondelete='CASCADE')),
        schema=params['schema'],
        useexisting=True,
        )
    t_provv_pg_az_art.create(checkfirst=True)


class ProvvPgAzArt(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'id':
            dic = {k: t_provv_pg_az_art.c.id == v}
        elif k == 'id_persona_giuridica_to':
            dic = {k: t_provv_pg_az_art.c.id_persona_giuridica_to == v}
        elif k == 'id_persona_giuridica_from':
            dic = {k: t_provv_pg_az_art.c.id_persona_giuridica_from == v}
        elif k == 'id_provvigione':
            dic = {k: t_provv_pg_az_art.c.id_provvigione == v}
        return dic[k]


std_mapper = mapper(ProvvPgAzArt, t_provv_pg_az_art,   properties={
        "provv":relation(Provvigione,
            primaryjoin=t_provv_pg_az_art.c.id_provvigione == t_provvigione.c.id,
            backref="provv_pg_az_art",
            cascade="all, delete"),
        "arti":relation(Articolo,
            primaryjoin=t_provv_pg_az_art.c.id_articolo== t_articolo.c.id,
            backref="provv_pg_az_art"),
        "pg_from":relation(PersonaGiuridica_,
            primaryjoin=t_provv_pg_az_art.c.id_persona_giuridica_from== t_persona_giuridica.c.id,
            backref="provv_pg_az_art_from"),
        "pg_to":relation(PersonaGiuridica_,
            primaryjoin=t_provv_pg_az_art.c.id_persona_giuridica_to== t_persona_giuridica.c.id,
            backref="provv_pg_az_art_to"),
#        "azi:"relation(Azienda,
#            primaryjoin=t_provv_pg_az_art.c.id_schemaa_azienza== t_azienda.c.denominazione,
#            backref="provv_pg_az_art_to"),
            },
                    order_by=t_provv_pg_az_art.c.id)
