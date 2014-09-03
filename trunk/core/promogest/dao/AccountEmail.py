# -*- coding: utf-8 -*-

#    Copyright (C) 2013 by Francesco Marella <francesco.marella@anche.no>

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
from promogest.Environment import params, session, azienda, \
        delete_pickle
from promogest.dao.Dao import Dao
from promogest.dao.Azienda import Azienda

try:
    t_account_email = Table('account_email',
                            params['metadata'],
                            schema=params['schema'],
                            autoload=True)
except:
    from data.accountEmail import t_account_email


def reimposta_preferito(newDao):
    daos = AccountEmail().select(complexFilter=(and_(not_(AccountEmail.id==newDao.id),
                                                AccountEmail.id_azienda==newDao.id_azienda,
                                                AccountEmail.preferito==True)),
                                                batchSize=None)
    if daos:
        daos[0].preferito = False

class AccountEmail(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def persist(self):
        if self.preferito == True:
            reimposta_preferito(self)
        session.add(self)
        session.commit()

    def filter_values(self, k, v):
        if k == 'idAzienda':
            dic = {k: t_account_email.c.id_azienda==v}
        elif k == 'denominazione':
            dic = {k: and_(t_account_email.c.id_azienda==Azienda.schemaa,
                           t_account_email.c.denominazione.ilike("%" + v + "%"))}
        elif k == 'indirizzo':
            dic = {k: and_(t_account_email.c.id_azienda==Azienda.schemaa,
                           t_account_email.c.indirizzo.ilike("%" + v + "%"))}
        elif k == 'preferito':
            dic = {k: t_account_email.c.preferito == True}
        return dic[k]

std_mapper = mapper(AccountEmail, t_account_email)
