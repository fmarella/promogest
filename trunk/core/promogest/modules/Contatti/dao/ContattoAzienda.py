# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010,2011 by Promotux
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
from promogest.dao.Azienda import Azienda
from promogest.modules.Contatti.dao.RecapitoContatto import RecapitoContatto
from promogest.modules.Contatti.dao.ContattoCategoriaContatto import ContattoCategoriaContatto

class ContattoAzienda(Dao):

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
                'schemaAzienda' : contattoazienda.c.schema_azienda == v,
                'cognomeNome' : or_(contatto.c.cognome.ilike("%"+v+"%"),contatto.c.nome.ilike("%"+v+"%")),
                'ruolo': contatto.c.ruolo.ilike("%"+v+"%"),
                'descrizione': contatto.c.descrizione.ilike("%"+v+"%"),
                'recapito': and_(contatto.c.id == RecapitoContatto.id_contatto,RecapitoContatto.recapito.ilike("%"+v+"%")),
                'tipoRecapito': and_(contatto.c.id == RecapitoContatto.id_contatto,RecapitoContatto.tipo_recapito.contains(v)),
            }
        return dic[k]


contatto=Table('contatto',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

contattoazienda=Table('contatto_azienda',
        params['metadata'],
        schema = params['schema'],
        autoload=True)

j = join(contatto, contattoazienda)
std_mapper = mapper(ContattoAzienda, j,properties={
                'id':[contatto.c.id, contattoazienda.c.id],
                'tipo_contatto':[contatto.c.tipo_contatto, contattoazienda.c.tipo_contatto],
                "azienda":relation(Azienda, backref="contatto_azienda")
                },
                order_by=contatto.c.id)
