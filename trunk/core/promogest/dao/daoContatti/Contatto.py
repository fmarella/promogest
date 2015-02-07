# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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
from promogest.lib.utils import getCategorieContatto, getRecapitiContatto
from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
from promogest.dao.daoContatti.ContattoCategoriaContatto import ContattoCategoriaContatto


class Contatto(Base, Dao):

    try:
        __table__ = Table('contatto',
            params['metadata'],
            schema = params['schema'] ,
            autoload=True,
            autoload_with=engine)
    except:
        from data.contatto import t_contatto
        __table__ = t_contatto

    recapito = relationship("RecapitoContatto", backref=backref('contatto'),cascade="all, delete")
    contatto_cat_cont = relationship("ContattoCategoriaContatto", backref=backref("contatto"), cascade="all, delete")

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def _getRecapitiContatto(self):
        self.__dbRecapitiContatto = getRecapitiContatto(id=self.id)
        self.__recapitiContatto = self.__dbRecapitiContatto[:]
        return self.__recapitiContatto

    def _setRecapitiContatto(self, value):
        self.__recapitiContatto = value

    recapiti = property(_getRecapitiContatto, _setRecapitiContatto)

    def _getCategorieContatto(self):
        self.__dbCategorieContatto = getCategorieContatto(id=self.id)
        self.__categorieContatto = self.__dbCategorieContatto[:]
        return self.__categorieContatto

    def _setCategorieContatto(self, value):
        self.__categorieContatto = value

    categorieContatto = property(_getCategorieContatto, _setCategorieContatto)

    def _appartenenza(self):
        appa = ""
        a =None
        if self.tipo_contatto=="cliente" and self.contatto_cliente :
            from promogest.dao.Cliente import Cliente
            a =  params["session"].query(Cliente).filter(self.contatto_cliente[0].id_cliente==Cliente.id).all()
        if a:
            appa = "Rif."
            if a[0].ragione_sociale:
                appa = appa +" "+a[0].ragione_sociale
            if a[0].cognome:
                appa = appa+" " +a[0].cognome
            if a[0].nome:
                appa = appa+" "+a[0].nome
        return appa
    appartenenza = property(_appartenenza)


    #FIXME: verificare TUTTI i filtri Contatto!!!
    def filter_values(self,k,v):
        if k == 'cognomeNome':
            dic = {k:or_(Contatto.__table__.c.cognome.ilike("%"+v+"%"),Contatto.__table__.c.nome.ilike("%"+v+"%"))}
        elif k == 'id':
            dic = {k:Contatto.__table__.c.id == v}
        elif k == 'ruolo':
            dic = {k:Contatto.__table__.c.ruolo.ilike("%"+v+"%")}
        elif k=='descrizione':
            dic = {k:Contatto.__table__.c.descrizione.ilike("%"+v+"%")}
        elif k =='recapito':
            dic = {k:and_(Contatto.__table__.c.id == RecapitoContatto.id_contatto,RecapitoContatto.recapito.ilike("%"+v+"%")) }
        elif k == 'tipoRecapito':
            dic = {k:and_(Contatto.__table__.c.id == RecapitoContatto.id_contatto,RecapitoContatto.tipo_recapito.contains(v))}
        elif k == 'idCategoria':
            dic = {k:and_(Contatto.__table__.c.id == ContattoCategoriaContatto.id_contatto, ContattoCategoriaContatto.id_categoria_contatto == v)}
        return dic[k]

    def delete(self, multiple=False, record = True):
        cleanRecapitoContatto = RecapitoContatto().select(idContatto=self.id)
        for recapito in cleanRecapitoContatto:
            recapito.delete()
        cleanContattoCategoriaContatto = ContattoCategoriaContatto()\
                                                        .select(idContatto=self.id,
                                                        batchSize=None)
        for contatto in cleanContattoCategoriaContatto:
            contatto.delete()
        params['session'].delete(self)
        params['session'].commit()



if tipodb=="sqlite":
    a = session.query(Contatto.id).all()
    b = session.query(RecapitoContatto.id_contatto).all()
    fixit =  list(set(b)-set(a))
    print("fixt-contatto", fixit)
    for f in fixit:
        aa = RecapitoContatto().select(idContatto=f[0], batchSize=None)
        for a in aa:
            session.delete(a)
    session.commit()
