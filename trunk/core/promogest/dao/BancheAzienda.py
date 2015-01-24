# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>
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

from promogest.dao.Dao import Dao, Base
from promogest.dao.Azienda import Azienda
from promogest.dao.Banca import Banca

def gen_banche_azienda():
    daos = []
    if azienda:
        daos = BancheAzienda().select(complexFilter=(and_(BancheAzienda.id_azienda==azienda)), batchSize=None)
    else:
        daos = BancheAzienda().select(batchSize=None)
    for dao in daos:
        if dao.banca:
            if dao.banca.agenzia:
                yield (dao.banca, dao.banca.id, ("{0} ({1})\nNum. conto: {2}".format(dao.banca.denominazione, dao.banca.agenzia, dao.numero_conto)))
            else:
                yield (dao.banca, dao.banca.id, ("{0}\nNum. conto: {1}".format(dao.banca.denominazione, dao.numero_conto)))

def reimposta_banca_predefinita(newDao):
    daos = BancheAzienda().select(complexFilter=(and_(not_(BancheAzienda.id==newDao.id), BancheAzienda.id_azienda==newDao.id_azienda, BancheAzienda.banca_predefinita==True)), batchSize=None)
    if daos:
        daos[0].banca_predefinita = False

class BancheAzienda(Base, Dao):
    try:
        __table__ = Table('banche_azienda',
                                params['metadata'],
                                schema=params['schema'],
                                autoload=True,
                                )
    except:
        from data.bancheAzienda import t_banche_azienda
        __table__ = t_banche_azienda

    banca = relationship("Banca", primaryjoin=(__table__.c.id_banca==Banca.__table__.c.id),
                                    foreign_keys=[Banca.__table__.c.id],
                                    uselist=False)

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    @property
    def denominazione_banca(self):
        banca = Banca().getRecord(id=self.id_banca)
        denominazione = ''
        if banca:
            if banca.agenzia:
                denominazione = "{0} ({1})".format(banca.denominazione, banca.agenzia)
            else:
                denominazione = "{0}".format(banca.denominazione)
        return denominazione

    def persist(self):
        if self.banca_predefinita == True:
            reimposta_banca_predefinita(self)
        session.add(self)
        session.commit()

    def filter_values(self, k, v):
        if k == 'idAzienda':
            dic = {k: BancheAzienda.__table__.c.id_azienda==v}
        elif k == 'numeroConto':
            dic = {k: and_(BancheAzienda.__table__.c.id_azienda==Azienda.schemaa,
                            BancheAzienda.__table__.c.numero_conto.ilike("%" + v + "%"))}
        return dic[k]
