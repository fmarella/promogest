# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012,2011 by Promotux
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

from sqlalchemy import Table, or_
from sqlalchemy.orm import join, relation, mapper
from promogest.Environment import params

try:
    t_contatto_magazzino=Table('contatto_magazzino',
        params['metadata'],
        schema = params['schema'],
        autoload=True)
except:
    from data.contattoMagazzino import t_contatto_magazzino

from promogest.dao.Dao import Dao
from promogest.dao.Magazzino import Magazzino
from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto, t_recapito
from promogest.dao.daoContatti.Contatto import t_contatto
from promogest.dao.daoContatti.ContattoCategoriaContatto import ContattoCategoriaContatto

class ContattoMagazzino(Dao):

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
        self.__dbCategorieContatto = ContattoCategoriaContatto().select(id=self.id)

        self.__categorieContatto = self.__dbCategorieContatto[:]
        return self.__categorieContatto

    def _setCategorieContatto(self, value):
        self.__categorieContatto = value

    categorieContatto = property(_getCategorieContatto, _setCategorieContatto)

    def _appartenenza(self):
        a =  params["session"].query(Magazzino).with_parent(self).filter(self.id_magazzino==Magazzino.id).all()
        if not a:
            return a
        else:
            return a[0].denominazione
    appartenenza = property(_appartenenza)

    def filter_values(self,k,v):
        if k == 'idCategoria':
            dic = {k:and_(ContattoCategoriaContatto.id_contatto==t_contatto.c.id, ContattoCategoriaContatto.id_categoria_contatto==v)}
        elif k == 'idMagazzino':
            dic = {k : t_contatto_magazzino.c.id_magazzino == v}
        elif k == 'idMagazzinoList':
            dic = {k : t_contatto_magazzino.c.id_magazzino.in_(v)}
        elif k == 'cognomeNome':
            dic = {k : or_(t_contatto.c.cognome.ilike("%"+v+"%"),t_contatto.c.nome.ilike("%"+v+"%"))}
        elif k == 'ruolo':
            dic = {k : t_contatto.c.ruolo.ilike("%"+v+"%")}
        elif k == "recapito":
            dic={k:and_(contattocliente.c.id==t_recapito.c.id_contatto,recapito.c.recapito.ilike("%"+v+"%"))}
        elif k == "tipoRecapito":
            dic={k:and_(contattocliente.c.id==t_recapito.c.id_contatto,t_recapito.c.tipo_recapito ==v)}
        elif k =='descrizione':
            dic = {k : t_contatto.c.descrizione.ilike("%"+v+"%")}
        #'recapito':
        #'tipoRecapito':
        return dic[k]

std_mapper = mapper(ContattoMagazzino, join(t_contatto, t_contatto_magazzino),
            properties={
               'id':[t_contatto.c.id, t_contatto_magazzino.c.id],
                'tipo_contatto':[t_contatto.c.tipo_contatto, t_contatto_magazzino.c.tipo_contatto],
                "magazzino":relation(Magazzino, backref="contatto_magazzino")},
                order_by=t_contatto_magazzino.c.id)
