# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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
from promogest.dao.Banca import Banca

class RigaPrimaNota(Base, Dao):
    try:
        __table__ = Table('riga_prima_nota',
                            params['metadata'],
                            schema=params['schema'],
                            autoload=True)
    except:
        from data.rigaPrimaNota import t_riga_prima_nota
        __table__ = t_riga_prima_nota

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "id":
            dic = {k: RigaPrimaNota.__table__.c.id == v}
        elif k == 'idTestataDocumento':
            dic = {k: RigaPrimaNota.__table__.c.id_testata_documento == v}
        elif k == 'segno':
            dic = {k: RigaPrimaNota.__table__.c.segno == v}
        elif k == 'tipo':
            dic = {k: RigaPrimaNota.__table__.c.tipo == v}
        elif k == 'idBanca':
            dic = {k: RigaPrimaNota.__table__.c.id_banca == v}
        elif k == 'idTestataPrimaNota':
            dic = {k: RigaPrimaNota.__table__.c.id_testata_prima_nota == v}
        return dic[k]

    @property
    def banca(self):
        bn = Banca().getRecord(id=self.id_banca)
        if bn:
            return bn.denominazione
        else:
            return ''


if tipodb=="sqlite":
    a = session.query(Banca.id).all()
    b = session.query(RigaPrimaNota.id_banca).all()
    fixit =  list(set(b)-set(a))
    print "fixt-riga-prima-nota-banca", fixit
    for f in fixit:
        if f[0] != "None" and f[0] != None:
            aa = RigaPrimaNota().select(idBanca=f[0], batchSize=None)
            for z in aa:
                z.id_banca = None
                session.add(z)
    session.commit()
