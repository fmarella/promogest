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
from migrate import *
from promogest.modules.CSA.dao.LuogoInstallazione import LuogoInstallazione
#from promogest.dao.Articolo import Articolo, t_articolo
#from promogest.dao.Cliente import Cliente, t_cliente
#from promogest.modules.CSA.dao.TipoApparecchio import TipoApparecchio
#from promogest.modules.GestioneCommesse.dao.TestataCommessa import TestataCommessa,t_testatacommessa

try:
    t_serv_csa = Table('servizio_csa', params['metadata'],
                         schema=params['schema'], autoload=True)
except:
    params["session"].close() # Questo comando chiude la sessione appesa
                              # e permette la creazione della tabella
    t_serv_csa = Table('servizio_csa',
        params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('id_articolo', Integer,
               ForeignKey(fk_prefix + 'articolo.id',
                          onupdate='CASCADE', ondelete='CASCADE'),nullable=True),
        Column('id_cliente', Integer,
               ForeignKey(fk_prefix + 'cliente.id',
                          onupdate='CASCADE', ondelete='CASCADE'),nullable=True),
        Column('numero_serie', String(200), nullable=True),
        Column('combustibile', String(200), nullable=True),
        Column('data_avviamento', DateTime, nullable=True),
        Column('tenuta_libretto', Boolean, default=False, nullable=False),

        Column('id_luogo_installazione', Integer,
               ForeignKey(fk_prefix + 'luogo_installazione.id',
                          onupdate='CASCADE', ondelete='CASCADE'),nullable=True),
        Column('id_persona_giuridica', Integer,
               ForeignKey(fk_prefix + 'persona_giuridica.id',
                          onupdate='CASCADE', ondelete='CASCADE'),nullable=True),
        Column('manutenzione', String(100), nullable=True),
        Column('cadenza', String(1000), nullable=True),
        schema=params['schema'],
        useexisting=True,
        )


    t_serv_csa.create(checkfirst=True)


class ServCSA(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'id':
            dic = {k: t_articolo_csa.c.id==v}
        elif k == 'id_articolo':
            dic = {k: t_articolo_csa.c.id_articolo==v}
        return dic[k]


std_mapper = mapper(ServCSA, t_serv_csa,   properties={

        #"arti":relation(Articolo,
            #primaryjoin=t_serv_csa.c.id_articolo== t_articolo.c.id,
            #backref="serv_csa"),
        #"CLI":relation(Cliente,
            #primaryjoin=t_serv_csa.c.id_cliente== t_cliente.c.id,
            #backref="serv_csa"),


                    },   order_by=t_serv_csa.c.id)
