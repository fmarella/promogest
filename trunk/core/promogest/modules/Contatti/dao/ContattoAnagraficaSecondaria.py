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

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao
from promogest.dao.AnagraficaSecondaria import AnagraficaSecondaria_
from promogest.modules.Contatti.dao.RecapitoContatto import RecapitoContatto
from promogest.modules.Contatti.dao.ContattoCategoriaContatto import ContattoCategoriaContatto


recapito=Table('recapito',
    params['metadata'],
    autoload=True,
    schema = params['schema'])

contatto=Table('contatto',
    params['metadata'],
    schema = params['schema'],
    autoload=True)

azTable = Table('anagrafica_secondaria',
    params['metadata'],
    autoload=True,
    schema = params['schema'])

try:
    contattoanagraficasecondaria=Table('contatto_anagraficasecondaria',
        params['metadata'],
        schema = params['schema'],
        autoload=True)
except:

    if params["tipo_db"] == "sqlite":
        contattoFKid ='contatto.id'
        anagraficasecondariaFK = 'anagrafica_secondaria.id'
        contattoFKtipocontatto = 'contatto.tipo_contatto'
    else:
        contattoFKid = params['schema'] +'.contatto.id'
        anagraficasecondariaFK = params['schema'] +'.anagrafica_secondaria.id'
        contattoFKtipocontatto = params['schema'] +'.contatto.tipo_contatto'


    contattoanagraficasecondaria = Table('contatto_anagraficasecondaria',
        params['metadata'],
        Column('id',Integer,primary_key=True),
        Column('tipo_contatto',String(50),primary_key=True),
        Column('id_anagraficasecondaria',Integer,ForeignKey(anagraficasecondariaFK,onupdate="CASCADE",ondelete="RESTRICT"),nullable=False),
        ForeignKeyConstraint(['id', 'tipo_contatto'],[contattoFKid, contattoFKtipocontatto],onupdate="CASCADE", ondelete="CASCADE"),
        #CheckConstraint("tipo_contatto = 'fornitore'"),
        schema = params['schema']
            )
    contattoanagraficasecondaria.create(checkfirst=True)

class ContattoAnagraficaSecondaria(Dao):

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)


    def _getRecapitiContatto(self):
        self.__dbRecapitiContatto = RecapitoContatto().\
                                            select(id=self.id,batchSize=None)
        self.__recapitiContatto = self.__dbRecapitiContatto[:]
        return self.__recapitiContatto

    def _setRecapitiContatto(self, value):
        self.__recapitiContatto = value

    recapiti = property(_getRecapitiContatto, _setRecapitiContatto)


    def _getCategorieContatto(self):
        self.__dbCategorieContatto = ContattoCategoriaContatto().\
                                            select(id=self.id,batchSize=None)
        self.__categorieContatto = self.__dbCategorieContatto[:]
        return self.__categorieContatto

    def _setCategorieContatto(self, value):
        self.__categorieContatto = value

    categorieContatto = property(_getCategorieContatto, _setCategorieContatto)

    #def _appartenenza(self):
        #a =  params["session"].query(Fornitore).with_parent(self).\
                            #filter(self.id_fornitore==Fornitore.id).all()
        #if not a:
            #return a
        #else:
            #return a[0].ragione_sociale or a[0].cognome or a[0].nome
    #appartenenza = property(_appartenenza)


    #FIXME: sistemare questo filtro
    def filter_values(self, k,v):
        if k == 'idCategoria':
            dic = {k:and_(ContattoCategoriaContatto.id_contatto==contatto.c.id, ContattoCategoriaContatto.id_categoria_contatto==v)}
        elif k == 'idAnagraficaSecondaria':
            dic = {k:contattoanagraficasecondaria.c.id_anagraficasecondaria == v}
        elif k == 'idAnagraficaSecondariaList':
            dic = {k:contattoanagraficasecondaria.c.id_anagraficasecondaria.in_(v)}
        elif k == 'cognomeNome':
            dic = {k:or_(contatto.c.cognome.ilike("%"+v+"%"),contatto.c.nome.ilike("%"+v+"%"))}
        elif k == 'ruolo':
            dic = {k:contatto.c.ruolo.ilike("%"+v+"%")}
        elif k == "recapito":
            dic={k:and_(contattoanagraficasecondaria.c.id==recapito.c.id_contatto,recapito.c.recapito.ilike("%"+v+"%"))}
        elif k == "tipoRecapito":
            dic={k:and_(contattoanagraficasecondaria.c.id==recapito.c.id_contatto,recapito.c.tipo_recapito ==v)}
        elif k=='descrizione':
            dic = {k:contatto.c.descrizione.ilike("%"+v+"%")}
            #'recapito':
            #'tipoRecapito':
        return  dic[k]

j = join(contatto, contattoanagraficasecondaria)

std_mapper = mapper(ContattoAnagraficaSecondaria, j,properties={
        'id':[contatto.c.id, contattoanagraficasecondaria.c.id],
        'tipo_contatto':[contatto.c.tipo_contatto, contattoanagraficasecondaria.c.tipo_contatto],
        "anagraficasecondaria":relation(AnagraficaSecondaria_, backref="contatto_anagraficasecondaria")})
