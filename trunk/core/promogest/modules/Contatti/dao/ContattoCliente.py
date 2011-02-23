# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010,2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    This file is part of Promogest. http://www.promogest.me

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
from promogest.Environment import params
from promogest.dao.Dao import Dao
from promogest.dao.Cliente import Cliente
from promogest.modules.Contatti.dao.Contatto import Contatto
from promogest.modules.Contatti.dao.RecapitoContatto import RecapitoContatto
from promogest.modules.Contatti.dao.ContattoCategoriaContatto import ContattoCategoriaContatto

class ContattoCliente(Dao):

    def __init__(self, arg=None):
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
            dic = {k:and_(ContattoCategoriaContatto.id_contatto==contatto.c.id, ContattoCategoriaContatto.id_categoria_contatto==v)}
        elif k == 'idCliente':
            dic = {k:contattocliente.c.id_cliente == v}
        elif k == "idClienteList":
            dic = {k:contattocliente.c.id_cliente.in_(v)}
        elif k == 'cognomeNome':
            dic = {k:or_(contatto.c.cognome.ilike("%"+v+"%"),contatto.c.nome.ilike("%"+v+"%"))}
        elif k == 'ruolo':
            dic = {k:contatto.c.ruolo.ilike("%"+v+"%")}
        elif k == "recapito":
            dic={k:and_(contattocliente.c.id==recapito.c.id_contatto,recapito.c.recapito.ilike("%"+v+"%"))}
        elif k == "tipoRecapito":
            dic={k:and_(contattocliente.c.id==recapito.c.id_contatto,recapito.c.tipo_recapito ==v)}
        elif k=='descrizione':
            dic = {k:contatto.c.descrizione.ilike("%"+v+"%")}

        #FIXME: #'recapito'
        #FIXME : #'tipoRecapito':
        return dic[k]

recapito=Table('recapito',params['metadata'],autoload=True,schema = params['schema'])
contatto=Table('contatto', params['metadata'],schema = params['schema'], autoload=True)
contattocliente=Table('contatto_cliente', params['metadata'],schema = params['schema'], autoload=True)

j = join(contatto, contattocliente)

std_mapper = mapper(ContattoCliente, j,properties={
                'id':[contatto.c.id, contattocliente.c.id],
                "cc" : relation(Contatto, backref="contatto_cliente"),
                'tipo_contatto':[contatto.c.tipo_contatto, contattocliente.c.tipo_contatto],
                "cliente":relation(Cliente, backref="contatto_cliente")
                }, order_by=contattocliente.c.id)
