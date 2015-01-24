# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from promogest.dao.Dao import Dao, Base
from promogest.modules.PromoWear.dao.Taglia import Taglia

class GruppoTagliaTaglia(Base, Dao):
    try:
        __table__ = Table('gruppo_taglia_taglia',
           params['metadata'],
           schema = params['schema'],
           autoload=True)
    except:
        __table__ = Table('gruppo_taglia_taglia', params['metadata'],
                Column('id_gruppo_taglia',Integer,
                            ForeignKey(fk_prefix + "gruppo_taglia.id",
                                    onupdate="CASCADE",
                                    ondelete="RESTRICT"),
                            primary_key=True),
                Column('id_taglia',Integer,
                            ForeignKey(fk_prefix + "taglia.id",
                                    onupdate="CASCADE",
                                    ondelete="RESTRICT"),
                            primary_key=True),
                Column('ordine',Integer,nullable=False),
                schema=params["schema"])

    TAG = relationship("Taglia",backref="GTTTAG")

    __mapper_args__ = {
        'order_by' : "ordine"
    }

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == 'idGruppoTaglia':
            dic= {k: GruppoTagliaTaglia.__table__.c.id_gruppo_taglia ==v}
        elif k == 'idTaglia':
            dic= {k: GruppoTagliaTaglia.__table__.c.id_taglia ==v}
        return  dic[k]

    @property
    def denominazione_breve_gruppo_taglia(self):
        if self.GTTGT: return self.GTTGT.denominazione_breve or ""

    @property
    def denominazione_gruppo_taglia(self):
        if self.GTTGT: return self.GTTGT.denominazione or ""

    @property
    def denominazione_breve_taglia(self):
        if self.TAG: return self.TAG.denominazione_breve or ""

    @property
    def denominazione_taglia(self):
        if self.TAG: return self.TAG.denominazione or ""
