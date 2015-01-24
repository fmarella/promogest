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
from promogest.dao.Dao import Dao, Base
from promogest.dao.Azienda import Azienda
from promogest.dao.daoContatti.Contatto import Contatto
from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
from promogest.dao.daoContatti.ContattoCategoriaContatto import ContattoCategoriaContatto


#try:
#    t_contatto_azienda=Table('contatto_azienda',
#        params['metadata'],
#        schema = params['schema'],
#        autoload=True)
#except:
#    from data.contattoAzienda import t_contatto_azienda


class ContattoAzienda(Base, Dao):
    __table__ = Table('contatto_azienda', params["metadata"],
        Column('id',Integer,primary_key=True),
        Column('tipo_contatto',String(50),primary_key=True),
        Column('schema_azienda',String(100),ForeignKey(fk_prefix_main+'azienda.schemaa',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False),
        ForeignKeyConstraint(['id', 'tipo_contatto'],[fk_prefix+'contatto.id', fk_prefix+'contatto.tipo_contatto'],onupdate="CASCADE", ondelete="CASCADE"),
        CheckConstraint("tipo_contatto = 'azienda'"),
        #extend_existing=True,
        schema=params["schema"]
        )
    __mapper_args__ = {
        'polymorphic_identity':'contatto_azienda',
    }

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
        a =  params["session"].query(Azienda).with_parent(self).filter(self.schema_azienda==Azienda.schemaa).all()
        if not a:
            return a
        else:
            return a[0].ragione_sociale or a[0].denominazione
    appartenenza = property(_appartenenza)


    def filter_values(self,k,v):
        dic= {  'idCategoria' : None,
                'schemaAzienda' : t_contatto_azienda.c.schema_azienda == v,
                'cognomeNome' : or_(t_contatto.c.cognome.ilike("%"+v+"%"),t_contatto.c.nome.ilike("%"+v+"%")),
                'ruolo': t_contatto.c.ruolo.ilike("%"+v+"%"),
                'descrizione': t_contatto.c.descrizione.ilike("%"+v+"%"),
                'recapito': and_(t_contatto.c.id == RecapitoContatto.id_contatto,RecapitoContatto.recapito.ilike("%"+v+"%")),
                'tipoRecapito': and_(t_contatto.c.id == RecapitoContatto.id_contatto,RecapitoContatto.tipo_recapito.contains(v)),
            }
        return dic[k]

#std_mapper = mapper(ContattoAzienda, join(t_contatto, t_contatto_azienda),
                #properties={
                #'id':[t_contatto.c.id, t_contatto_azienda.c.id],
                #'tipo_contatto':[t_contatto.c.tipo_contatto, t_contatto_azienda.c.tipo_contatto],
                ##"azienda":relation(Azienda, backref="contatto_azienda")
                #},
                #order_by=t_contatto_azienda.c.id)
