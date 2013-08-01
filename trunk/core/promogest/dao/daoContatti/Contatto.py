# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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
from promogest.dao.Dao import Dao
from promogest.lib.utils import getCategorieContatto, getRecapitiContatto
from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
from promogest.dao.daoContatti.ContattoCategoriaContatto import ContattoCategoriaContatto


try:
    t_contatto=Table('contatto',
        params['metadata'],
        schema = params['schema'] if tipo_eng=="postgresql" else None,
        autoload=True)
except:
    from data.contatto import t_contatto


class Contatto(Dao):

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
            dic = {k:or_(t_contatto.c.cognome.ilike("%"+v+"%"),t_contatto.c.nome.ilike("%"+v+"%"))}
        elif k == 'id':
            dic = {k:t_contatto.c.id == v}
        elif k == 'ruolo':
            dic = {k:t_contatto.c.ruolo.ilike("%"+v+"%")}
        elif k=='descrizione':
            dic = {k:t_contatto.c.descrizione.ilike("%"+v+"%")}
        elif k =='recapito':
            dic = {k:and_(t_contatto.c.id == RecapitoContatto.id_contatto,RecapitoContatto.recapito.ilike("%"+v+"%")) }
        elif k == 'tipoRecapito':
            dic = {k:and_(t_contatto.c.id == RecapitoContatto.id_contatto,RecapitoContatto.tipo_recapito.contains(v))}
        elif k == 'idCategoria':
            dic = {k:and_(t_contatto.c.id == ContattoCategoriaContatto.id_contatto, ContattoCategoriaContatto.id_categoria_contatto == v)}
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


std_mapper=mapper(Contatto, t_contatto,properties={
    'recapito' : relation(RecapitoContatto, backref=backref('contatto'),cascade="all, delete"),
    "contatto_cat_cont": relation(ContattoCategoriaContatto, backref=backref("contatto"), cascade="all, delete"),
    }, order_by=t_contatto.c.id)
