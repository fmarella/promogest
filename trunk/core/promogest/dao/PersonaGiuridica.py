#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005-2015 by Promotux Informatica - http://www.promotux.it/
#
# Authors: Francesco Meloni  <francesco@promotux.it>
#          Francesco Marella <francesco.marella@anche.no>
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
from promogest.dao.Dao import Dao, Base

class PersonaGiuridica_(Base, Dao):

    try:
        __table__ = Table('persona_giuridica',
                    params['metadata'],
                    schema=params['schema'],
                    autoload=True,
                    autoload_with=engine)
    except:
        from data.personaGiuridica import t_persona_giuridica
        __table__ = t_persona_giuridica

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'idUser':
            dic = {k: PersonaGiuridica_.__table__.c.id_user == v}
        return  dic[k]

try:
    PersonaGiuridica_.__table__.c.note
except:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.add_column('persona_giuridica', Column('note', Text))
    delete_pickle()
try:
    PersonaGiuridica_.__table__.c.cancellato
except:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    op = Operations(ctx)
    op.add_column('persona_giuridica',Column('cancellato', Boolean, default=False))
    delete_pickle()
