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
from promogest.dao.Cliente import Cliente
from promogest.dao.daoContatti.Contatto import Contatto
from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
from promogest.dao.daoContatti.ContattoCategoriaContatto import ContattoCategoriaContatto


from data.contatto import t_contatto
from data.contattoCliente import t_contatto_cliente
c_cc = join(t_contatto, t_contatto_cliente)

class ContattoCliente(Base, Dao):
    __table__ = c_cc
    id = column_property(t_contatto.c.id, t_contatto_cliente.c.id)
    tipo_contatto = column_property(t_contatto.c.tipo_contatto, t_contatto_cliente.c.tipo_contatto)
    cliente = relationship("Cliente", backref=backref("contatto_cliente",cascade="all,delete"))
    cc = relationship("Contatto", backref=backref("contatto_cliente", cascade="all, delete"))

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def _getRecapitiContatto(self):
        self.__dbRecapitiContatto = RecapitoContatto().select(id=self.id)
        self.__recapitiContatto = self.__dbRecapitiContatto[:]
        return self.__recapitiContatto

    def _setRecapitiContatto(self, value):
        self.__recapitiContatto = value

    recapiti = property(_getRecapitiContatto, _setRecapitiContatto)


    def _getCategorieContatto(self):
        self.__dbCategorieContatto = ContattoCategoriaContatto().select(id=self.id,
                                                        orderBy=ContattoCategoriaContatto.id_contatto)

        self.__categorieContatto = self.__dbCategorieContatto[:]
        return self.__categorieContatto

    def _setCategorieContatto(self, value):
        self.__categorieContatto = value

    categorieContatto = property(_getCategorieContatto, _setCategorieContatto)

    def _appartenenza(self):
        appa = ""
        a =  params["session"].query(Cliente).with_parent(self).filter(self.id_cliente==Cliente.id).all()
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


    def filter_values(self,k,v):
        if k == 'idCategoria':
            dic = {k:and_(ContattoCategoriaContatto.id_contatto==t_contatto.c.id, ContattoCategoriaContatto.id_categoria_contatto==v)}
        elif k == 'idCliente':
            dic = {k: t_contatto_cliente.c.id_cliente == v}
        elif k == "idClienteList":
            dic = {k: t_contatto_cliente.c.id_cliente.in_(v)}
        elif k == 'cognomeNome':
            dic = {k:or_(Contatto.__table__.c.cognome.ilike("%"+v+"%"),Contatto.__table__.c.nome.ilike("%"+v+"%"))}
        elif k == 'ruolo':
            dic = {k:Contatto.__table__.c.ruolo.ilike("%"+v+"%")}
        elif k == "recapito":
            dic={k:and_(ContattoCliente.__table__.c.id==RecapitoContatto.__table__.c.id_contatto,t_recapito.c.recapito.ilike("%"+v+"%"))}
        elif k == "tipoRecapito":
            dic={k:and_(ContattoCliente.__table__.c.id==RecapitoContatto.__table__.c.id_contatto,t_recapito.c.tipo_recapito ==v)}
        elif k=='descrizione':
            dic = {k:Contatto.__table__.c.descrizione.ilike("%"+v+"%")}
        return dic[k]
