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
from promogest.dao.TipoRichiesta import TipoRichiesta, t_tipo_richiesta
from promogest.dao.PersonaGiuridica import PersonaGiuridica_ , t_persona_giuridica

try:
    t_chiamata = Table('chiamata', params['metadata'],
                         schema=params['schema'], autoload=True)
except:
    params["session"].close() # Questo comando chiude la sessione appesa
                              # e permette la creazione della tabella
    t_chiamata = Table('chiamata',
        params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('id_articolo', Integer,
               ForeignKey(fk_prefix + 'articolo.id',
                          onupdate='CASCADE', ondelete='CASCADE'),nullable=True),
        Column('id_chiamante', Integer,
               ForeignKey(fk_prefix + 'persona_giuridica.id',
                          onupdate='CASCADE', ondelete='CASCADE'),nullable=True),
        Column('inizio_chiamata', DateTime, nullable=True),
        Column('fine_chiamata', DateTime, nullable=True),
        Column('data_appuntamento', DateTime, nullable=True),
        Column('durata_apuntamento', Integer, nullable=True),
        Column('id_tipo_richiesta', Integer,
               ForeignKey(fk_prefix + 'tipo_richiesta.id',
                          onupdate='CASCADE', ondelete='CASCADE'),nullable=True),
        Column('id_incaricato', Integer,
               ForeignKey(fk_prefix + 'persona_giuridica.id',
                          onupdate='CASCADE', ondelete='CASCADE'),nullable=True),
        Column('note', Text, nullable=True),

        schema=params['schema'],
        useexisting=True,
        )

    t_chiamata.create(checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()

class Chiamata(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'id':
            dic = {k: t_chiamata.c.id==v}
        elif k == 'idArticolo':
            dic = {k: t_chiamata.c.id_articolo==v}
        elif k == 'idChiamante':
            dic = {k: t_chiamata.c.id_chiamante==v}
        #elif k == 'numeroSerie':
            #dic = {k: t_serv_csa.c.numero_serie.ilike("%"+v+"%")}
        return dic[k]

    @property
    def tipo_richiesta(self):
        if self.tiporichiesta:
            return self.tiporichiesta.denominazione
        else:
            return _('tipo richiesta indeterminato')


std_mapper = mapper(Chiamata, t_chiamata,   properties={

        "tiporichiesta":relation(TipoRichiesta,
            primaryjoin=t_chiamata.c.id_tipo_richiesta== t_tipo_richiesta.c.id,
            backref="chiamata"),
        "incaricato":relation(PersonaGiuridica_,
            primaryjoin=t_chiamata.c.id_cliente== t_persona_giuridica.c.id,
            backref="chiamata"),
        "chiamante":relation(PersonaGiuridica_,
            primaryjoin=t_chiamata.c.id_incaricato== t_persona_giuridica.c.id,
            backref="chiamata"),
                    },   order_by=t_chiamata.c.id)
