# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from Dao import Dao
from promogest.ui.utils import getCategorieContatto, getRecapitiContatto
from RecapitoContatto import RecapitoContatto
from ContattoCategoriaContatto import ContattoCategoriaContatto

class Contatto(Dao):

    def __init__(self, arg=None):
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
                appa = appa+" "+a[0].nome" +a[0].nome
        return appa
    appartenenza = property(_appartenenza)


    #FIXME: verificare TUTTI i filtri Contatto!!!
    def filter_values(self,k,v):
        if k == 'cognomeNome':
            dic = {k:or_(contatto.c.cognome.ilike("%"+v+"%"),contatto.c.nome.ilike("%"+v+"%"))}
        elif k == 'id':
            dic = {k:contatto.c.id == v}
        elif k == 'ruolo':
            dic = {k:contatto.c.ruolo.ilike("%"+v+"%")}
        elif k=='descrizione':
            dic = {k:contatto.c.descrizione.ilike("%"+v+"%")}
        elif k =='recapito':
            dic = {k:and_(contatto.c.id == RecapitoContatto.id_contatto,RecapitoContatto.recapito.ilike("%"+v+"%")) }
        elif k == 'tipoRecapito':
            dic = {k:and_(contatto.c.id == RecapitoContatto.id_contatto,RecapitoContatto.tipo_recapito.contains(v))}
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
        #params["session"].refresh(self)
#        params["session"].clear()


contatto=Table('contatto',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

std_mapper=mapper(Contatto, contatto,properties={
    'recapito' : relation(RecapitoContatto, backref=backref('contatto')),
    "contatto_cat_cont": relation(ContattoCategoriaContatto,backref=backref("contatto")),
    }, order_by=contatto.c.id)
